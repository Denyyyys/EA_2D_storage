# import libraries
from typing import List, Dict, Tuple, Callable
import random
import numpy as np

# import custom modules
import constants
from utility import get_available_positions_for_product, print_products_location, get_product_origin_by_id, \
	delete_product_from_products_location, add_product_to_product_location, Product_info, get_product

####################################
### Classes and custom types 	 ###
####################################

# class Product_info:
#     def __init__(self, width: int, height: int, id: str):
#         self.width = width
#         self.height = height
#         self.id = id



class Individual:
	def __init__(self, storage_width: int, storage_height: int, list_products: List[Product_info], enter_position: Tuple[int, int] = (0, 0)):
		if not is_enough_space(list_products, storage_width, storage_height):
			raise ValueError(constants.NOT_ENOUGH_SPACE_MSG)
		self.products_location = create_random_products_position(list_products, storage_width, storage_height)
		self.storage_width = storage_width
		self.storage_height = storage_height
		self.enter_position = enter_position
		self.list_products = list_products

	def __str__(self):
		return("1")
		print(f"cost: {get_cost(self)}")
		print_products_location(self)


Population = List[Individual]
Hyperparameters = {
	"mutation_probability": float,
	"mutation_power": int,
	"number_individuals": int,
	"max_iterations": int,
	"storage_width": int,
	"storage_height": int,
	"products": List[Product_info],
	"entry": Tuple[int, int]
}
####################################
### Functions for EA 			 ###
####################################
def is_enough_space(list_products: List[Product_info], storage_width: int, storage_height: int) -> bool:
	total_space = 0
	for product_info in list_products:
		total_space += product_info["width"] * product_info["height"]
	return total_space < storage_width*storage_height


def get_best_individual(population: Population) -> Individual:
    sorted_pop = sort_population(population)
    return sorted_pop[0]


def create_random_population(number_individuals: int, storage_width: int, storage_height: int, list_products: List[Product_info], enter_position: Tuple[int, int] = (0, 0)):
    population = [Individual(storage_width, storage_height, list_products, enter_position) for _ in range(number_individuals)]
    return population


def sort_population(population: Population):
    return sorted(population, key=get_cost)


def create_random_products_position(list_products: List[Product_info], storage_width: int, storage_height: int) -> List[List[List[str | int]]]:
	products_location = []
	products_location = [([[0] for _ in range(storage_width)]) for _ in range(storage_height)]
	for product in list_products:
		x_start_max, y_start_max = get_available_positions_for_product(
			storage_width,
			storage_height,
			product["width"],
			product["height"]
		)
		x = random.randint(0, x_start_max)
		y = random.randint(0, y_start_max)
		for i in range(y, y + product["height"]):
			for j in range(x, x + product["width"]):				
				products_location[i][j].append(product["id"])

	return products_location 



def mutation_by_one_side(population: List[Individual], mutation_power: int, mutation_probability: float) -> List[Individual]:
	## BB
	# wybiramy losowo produkt
	# implementacja zmiany położenia produktu tylko w jedną stronę
	for individual in population:
		rand_number = random.uniform(0, 1)
		available_positions = get_available_origin_positions(individual, mutation_power)
		for available_position in available_positions:
			if mutation_probability == 1 or rand_number < mutation_probability:
				curr_x, curr_y = get_product_origin_by_id(available_position.id, individual.products_location)
				next_origin_pos = get_next_pos_one_side(available_position.min_x_origin_pos, available_position.max_x_origin_pos,
                                     			 available_position.min_y_origin_pos, available_position.max_y_origin_pos, 
                                         		 curr_x, curr_y)
				product = get_product(available_position.id, individual)
				individual.products_location = delete_product_from_products_location(individual.products_location,available_position.id)

				individual.products_location = add_product_to_product_location(individual.products_location, product.width, product.height, product.id,next_origin_pos[0], next_origin_pos[1])		
  
  
	return population


def get_next_pos_one_side(min_x:int, max_x:int, min_y:int, max_y:int, curr_x:int, curr_y:int) -> Tuple(int):
	dirr = None # if 0 then mutation goes for y direction, if 1 - x direction  
	list_new_positions = []
	if (min_x == max_x) and (min_y == max_y):
		raise ValueError("Cannot mutate product, which size is size of factory")
	elif min_x == max_x:
		dirr = 0 
	elif min_y == max_y:
		dirr = 1
	elif min_x < max_x and min_y < max_y:
		dirr = random.randint(0, 1)
	else:
		raise ValueError("Your positions are wrong :/")

	if dirr == 0:
		list_new_positions = [(curr_x, i) for i in range(min_y, max_y+1)]
	else:
		list_new_positions = [(i, curr_y) for i in range(min_x, max_x+1)]

	filtered_list_new_positions = [item for item in list_new_positions if item != (curr_x, curr_y)]
 
	
	next_pos = random.choice(filtered_list_new_positions)
 
	return next_pos


  
        
def get_next_pos_two_sides(min_x, max_x, min_y, max_y, curr_x, curr_y):
    # tuple_array = [(a, b) for a in range(a_min, a_max + 1) for b in range(b_min, b_max + 1)]
	pass



def mutation_by_two_sides(population: List[Individual], mutation_power: int, mutation_probability: float) -> List[Individual]:
	## BB
	# wybiramy losowo produkt
	# implementacja zmiany położenia produktu w dwie strony

 
	return population 



def get_available_origin_positions(individual: Individual, mutation_power: int) -> List[Dict[str,Tuple[int, int]]]:
	product_origins = [] 
	for product in individual.list_products:
		product_start_x = None
		product_start_y = None
		product_origin_found = False
		for i in range(individual.storage_height):
			for j in range(individual.storage_width):				
				if (product["id"] in individual.products_location[i][j]):
					product_start_y = i
					product_start_x = j
					product_origin_found = True
					break
			if product_origin_found:
				break
		
		if not product_origin_found:
			raise ValueError(f'There is no product with id: {product["id"]} in storage')

		min_x_origin_pos = max(0, product_start_x - mutation_power)
		min_y_origin_pos = max(0, product_start_y - mutation_power)
		max_x_origin_pos = min(individual.storage_width - product["width"], product_start_x + mutation_power)
		max_y_origin_pos = min(individual.storage_height - product["height"], product_start_y + mutation_power)
		product_origins.append({"id": product["id"], "min_x_origin_pos": min_x_origin_pos,"max_x_origin_pos": max_x_origin_pos,"min_y_origin_pos": min_y_origin_pos, "max_y_origin_pos": max_y_origin_pos})
	return product_origins





def tournament_selection(population: Population):
	## BB
	return population


def roulet_selection(population: Population):
	## BB
	return population


def threshold_selection(population: Population):
	## BB
	return population


def get_cost(individual: Individual) -> float:
    cost = 0
    punishment = get_punishment(individual)
    return cost + punishment


def get_punishment(individual: Individual) -> float:
	punishment = get_punishment_overlap(individual) + get_punishment_cannot_enter(individual) + \
     get_punishment_blocked_free_space(individual) + get_punishment_blocked_products(individual)
	return punishment


def get_punishment_overlap(individual: Individual, cost = 400) -> float:
	## DF
	return 10


def get_punishment_cannot_enter(individual: Individual, cost = 400) -> float:
	## DF
	return 0


def get_punishment_blocked_free_space(individual: Individual, cost = 400) -> float:
	## DF
	return 0


def get_punishment_blocked_products(individual: Individual, cost_per_frame = 100) -> float:
	## DF
	return 0


def run_simulation(
	cost_individual_func: Callable[[Individual], float],
	get_best_individual: Callable[[Population], Individual],
	get_init_population: Callable[[int, int, int, List[Product_info], Tuple[int, int]], Population],
	selection_func: Callable[[Population], Population],
	mutation_func: Callable[[Population, int, float], Population],
	hyperparameters: Hyperparameters,
	succession_func: Callable[[Population], Population] = None):
    

	mutation_probability, mutation_power, number_individuals, max_iterations, storage_width, storage_height, products, entry = (
    hyperparameters["mutation_probability"],
    hyperparameters["mutation_power"],
    hyperparameters["number_individuals"],
    hyperparameters["max_iterations"],
    hyperparameters["storage_width"],
    hyperparameters["storage_height"],
    hyperparameters["products"],
    hyperparameters["entry"]
)
	populations: List[Population] = []
	
	init_population = get_init_population(number_individuals, storage_width, storage_height, products, entry)
	for i in init_population:
		print_products_location(i)
		print('----------------------')
	populations.append(init_population)
	best_individual = get_best_individual(init_population)
	best_individual_cost = cost_individual_func(best_individual)
 
	if best_individual_cost == 0:
		return (populations, best_individual, best_individual_cost)

	curr_population = init_population
	for _ in range(max_iterations):
		curr_population = selection_func(curr_population)
		curr_population = mutation_func(curr_population, mutation_power, mutation_probability)
		curr_best_individual = get_best_individual(curr_population)
		curr_best_individual_cost = cost_individual_func(curr_best_individual)

		if curr_best_individual_cost < best_individual_cost:
			best_individual = curr_best_individual
			best_individual_cost = curr_best_individual_cost
			if best_individual_cost == 0:
				break

		if succession_func is not None:
			curr_population = succession_func(curr_population)
		populations.append(curr_population)
  
	return (populations, best_individual, best_individual_cost)