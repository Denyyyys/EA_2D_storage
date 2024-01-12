# import libraries
from typing import List, Dict, Tuple, Callable
import random
import numpy as np

# import custom modules
import constants
from utility import get_available_positions_for_product, print_products_location

####################################
### Classes and custom types 	 ###
####################################

# class Product_info:
#     def __init__(self, width: int, height: int, id: str):
#         self.width = width
#         self.height = height
#         self.id = id

Product_info = {"width": int, "height": int, "id": str}

class Individual:
	def __init__(self, storage_width: int, storage_height: int, list_products: List[Product_info], enter_position: Tuple[int, int] = (0, 0)):
		if not is_enough_space(list_products, storage_width, storage_height):
			raise ValueError(constants.NOT_ENOUGH_SPACE_MSG)
		self.products_location = create_random_products_position(list_products, storage_width, storage_height)
		self.storage_width = storage_width
		self.storage_height = storage_height
		self.enter_position = enter_position
		self.list_products = list_products


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



def mutation_by_one_side(individual: Individual, mutation_power: int, mutation_probability: float) -> Individual:
	## BB
	# wybiramy losowo produkt
	# implementacja zmiany położenia produktu tylko w jedną stronę
	return individual 


def mutation_by_two_sides(individual: Individual, mutation_power: int, mutation_probability: float) -> Individual:
	## BB
	# wybiramy losowo produkt
	# implementacja zmiany położenia produktu w dwie strony
	return individual 



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


def delete_product_from_products_location(products_location: List[List[List[str | int]]], id: str):
	for products_row in products_location:
		for product in products_row:
			if id in product:
				product.remove(id)

	return products_location


def add_product_to_product_location(product_location: List[List[List[str | int]]], product_width: int, product_height: int, id: str, product_origin_x: int, product_origin_y: int):
	storage_height = len(product_location)
	storage_width = len(product_location[0])
	if product_origin_x + product_width > storage_width or product_origin_y + product_height > storage_height:
		raise ValueError('Product is out of storage!')

	for i in range(product_origin_y, min(storage_height, product_origin_y + product_height)):
		for j in range(product_origin_x, min(storage_width, product_origin_x + product_width)):
			product_location[i][j].append(id)

	return product_location


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
	punishment = get_punishment_overlap(individual) + get_punishment_cannot_enter(individual) + get_punishment_blocked_free_space(individual) + get_punishment_blocked_products(individual)
	return punishment


def get_punishment_overlap(individual: Individual, cost = 400) -> float:
	## DF
	return 0


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