# import libraries
from typing import List, Dict, Tuple, Callable
import random
import numpy as np

# import cutom modules
import constants
# from custom_types import Product_info, Hyperparameters
from custom_types import Product_info, Hyperparameters
from utility import print_products_location, get_product_origin_by_id, \
	delete_product_from_products_location, add_product_to_product_location, get_product

from utilty_individual import is_enough_space, create_random_products_position, get_number_overlaps, get_min_number_blocked_space

####################################
### Classes 	 				 ###
####################################
class Individual:
	def __init__(self, storage_width: int, storage_height: int, list_products: List[Product_info], enter_position: List[int] = [0, 1]):
		if not is_enough_space(list_products, storage_width, storage_height):
			raise ValueError(constants.NOT_ENOUGH_SPACE_MSG)
		self.products_location = create_random_products_position(list_products, storage_width, storage_height)
		self.storage_width = storage_width
		self.storage_height = storage_height
		# [x, y]
		self.enter_position = enter_position
		self.list_products = list_products

	def __str__(self):
		return("1")
		print(f"cost: {get_cost(self)}")
		print_products_location(self)
  
	def get_available_origin_positions(self, mutation_power: int) -> List[Dict[str,Tuple[int, int]]]:
		product_origins = [] 
		for product in self.list_products:
			product_start_x = None
			product_start_y = None
			product_origin_found = False
			for i in range(self.storage_height):
				for j in range(self.storage_width):				
					if (product["id"] in self.products_location[i][j]):
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
			max_x_origin_pos = min(self.storage_width - product["width"], product_start_x + mutation_power)
			max_y_origin_pos = min(self.storage_height - product["height"], product_start_y + mutation_power)
			product_origins.append({"id": product["id"], "min_x_origin_pos": min_x_origin_pos,"max_x_origin_pos": max_x_origin_pos,"min_y_origin_pos": min_y_origin_pos, "max_y_origin_pos": max_y_origin_pos})
		return product_origins


Population = List[Individual]

####################################
### Population Creation 	     ###
####################################


def create_random_population(number_individuals: int, storage_width: int, storage_height: int, 
                             list_products: List[Product_info], enter_position: Tuple[int, int] = (0, 0)):
    population = [Individual(storage_width, storage_height, list_products, enter_position) for _ in range(number_individuals)]
    return population


# create population near point, which is provided
def create_random_population_normal(number_individuals: int, storage_width: int, storage_height: int, 
                             list_products: List[Product_info],  enter_position: Tuple[int, int] = (0, 0)):
	pass


####################################
### Mutation		 			 ###
####################################

# mutation can work for every product or for none
def mutation_by_one_side_diff_products(population: List[Individual], mutation_power: int, mutation_probability: float) -> List[Individual]:
	# Chose randomly products, which will be mutated
	# Change of product origin is possible only in one direction (up, down or left, right)
	for individual in population:
		rand_number = random.uniform(0, 1)
		available_positions = individual.get_available_origin_positions(mutation_power)
		for available_position in available_positions:
			if mutation_probability == 1 or rand_number < mutation_probability:
				curr_x, curr_y = get_product_origin_by_id(available_position["id"], individual.products_location)
				# print('Before:')
				# print_products_location(individual)
				next_origin_pos = random.choice(get_next_pos_one_side(available_position["min_x_origin_pos"], available_position["max_x_origin_pos"],
                                     			 available_position["min_y_origin_pos"], available_position["max_y_origin_pos"], 
                                         		 curr_x, curr_y))
    
				product = get_product(available_position["id"], individual)

				individual.products_location = delete_product_from_products_location(individual.products_location,available_position["id"])

				individual.products_location = add_product_to_product_location(individual.products_location, product["width"], product["height"], product["id"],next_origin_pos[0], next_origin_pos[1])		
				# print('After:')
				# print_products_location(individual)
				
	return population


# mutation work only for specific amount of products
def mutation_by_one_side_product(population: List[Individual], mutation_power: int, number_products_to_mutate: int) -> List[Individual]:
	# Chose randomly number_products_to_mutate products
	# Change of product origin is possible only in one direction (up, down or left, right)
	for individual in population:
		available_positions = individual.get_available_origin_positions(mutation_power)
		number_products_to_mutate = min(number_products_to_mutate, len(available_positions))
		# print("individual")
		# print("------------------------------------------------")
		indexes_arr = list(range(len(available_positions)))
		random.shuffle(indexes_arr)
		indexes_arr = indexes_arr[:number_products_to_mutate]
		chosen_products = [available_positions[i] for i in indexes_arr]
		for chosen_product in chosen_products:
			curr_x, curr_y = get_product_origin_by_id(chosen_product["id"], individual.products_location)
			# print('Before:')
			# print_products_location(individual)
			next_origin_pos = random.choice(get_next_pos_one_side(chosen_product["min_x_origin_pos"], chosen_product["max_x_origin_pos"],
												chosen_product["min_y_origin_pos"], chosen_product["max_y_origin_pos"], 
												curr_x, curr_y))

			product = get_product(chosen_product["id"], individual)

			individual.products_location = delete_product_from_products_location(individual.products_location,chosen_product["id"])

			individual.products_location = add_product_to_product_location(individual.products_location, product["width"], product["height"], product["id"],next_origin_pos[0], next_origin_pos[1])		
			# print('After:')
			# print_products_location(individual)

	return population


def get_next_pos_one_side(min_x:int, max_x:int, min_y:int, max_y:int, curr_x:int, curr_y:int) -> List[Tuple[int]]:
	dirr = None # if 0 then mutation goes for y direction, if 1 - x direction  
	list_new_positions = []
	if (min_x == max_x) and (min_y == max_y):
		raise ValueError("Cannot mutate product, which size is size of storage")
	elif min_x == max_x:
		dirr = 0 
	elif min_y == max_y:
		dirr = 1
	elif min_x < max_x and min_y < max_y and min_x <= curr_x <= max_x and min_y <= curr_y <= max_y:
		dirr = random.randint(0, 1)
	else:
		raise ValueError("Your positions are wrong :/")

	if dirr == 0:
		list_new_positions = [(curr_x, i) for i in range(min_y, max_y+1)]
	else:
		list_new_positions = [(i, curr_y) for i in range(min_x, max_x+1)]

	filtered_list_new_positions = [item for item in list_new_positions if item != (curr_x, curr_y)]
	# next_pos = random.choice(filtered_list_new_positions)

	return filtered_list_new_positions


def mutation_by_two_sides(population: List[Individual], mutation_power: int, mutation_probability: float) -> List[Individual]:
	## BB
	# wybiramy losowo produkt
	# implementacja zmiany położenia produktu w dwie strony

	# get_next_pos_two_sides
 
	return population 


def get_next_pos_two_sides(min_x, max_x, min_y, max_y, curr_x, curr_y):
    # tuple_array = [(a, b) for a in range(a_min, a_max + 1) for b in range(b_min, b_max + 1)]
	pass


####################################
### Selection		 			 ###
####################################


def tournament_selection(population: Population):
    next_population = []
    for _ in range(len(population)):
        individual_1 = random.choice(population)
        individual_2 = random.choice(population)
        if get_cost(individual_1) > get_cost(individual_2):
            next_population.append(copy_individual(individual_2))
        else:
            next_population.append(copy_individual(individual_1))
    return next_population


def roulet_selection(population: Population):
	## BB
	return population


def threshold_selection(population: Population):
	## BB
	return population


def copy_individual(individual: Individual):
	products_locations_copy = []
	
	for i in range(len(individual.products_location)):
		temp_row = []
		for j in range(len(individual.products_location[0])):
			temp_arr = []
			for element in individual.products_location[i][j]:
				temp_arr.append(element)
			temp_row.append(temp_arr)
		products_locations_copy.append(temp_row)

	individual_copy = Individual(individual.storage_width, individual.storage_height, individual.list_products,[individual.enter_position[0],individual.enter_position[1]])
	
	individual_copy.products_location = products_locations_copy    
	return individual_copy

####################################
### Cost Functions		 	     ###
####################################


def get_best_individual(population: Population) -> Individual:
	sorted_pop = sort_population(population)
	best_ind = sorted_pop[0]
	best_ind_list_products = best_ind.products_location
	products_locations_copy = []
	
	for i in range(len(best_ind_list_products)):
		temp_row = []
		for j in range(len(best_ind_list_products[0])):
			temp_arr = []
			for element in best_ind_list_products[i][j]:
				temp_arr.append(element)
			temp_row.append(temp_arr)
		products_locations_copy.append(temp_row)

	best_ind_copy = Individual(best_ind.storage_width, best_ind.storage_height, best_ind.list_products,[best_ind.enter_position[0],best_ind.enter_position[1]])
	best_ind_copy.products_location = products_locations_copy
	return best_ind_copy


def sort_population(population: Population):
    return sorted(population, key=get_cost)


def get_cost(individual: Individual) -> float:
    cost = 0
    punishment = get_punishment(individual)
    return cost + punishment


def get_punishment(individual: Individual) -> float:
	overlap = get_punishment_overlap(individual)
	cannot_enter = get_punishment_cannot_enter(individual)
	blocked_free_space = get_punishment_blocked_free_space(individual)
	punishment = get_punishment_overlap(individual) + get_punishment_cannot_enter(individual) + \
     get_punishment_blocked_free_space(individual) + get_punishment_blocked_products(individual)
	return punishment


def get_punishment_overlap(individual: Individual, cost = 400) -> float:
	total_overlaps = get_number_overlaps(individual.products_location)
	return total_overlaps * cost


def get_punishment_cannot_enter(individual: Individual, cost = 400) -> float:
	if len(individual.products_location[individual.enter_position[1]][individual.enter_position[0]]) > 1:
		return cost
	return 0


def get_punishment_blocked_free_space(individual: Individual, cost = 400) -> float:
	total_blocked_space = get_min_number_blocked_space(individual.products_location)
	return cost * total_blocked_space


def get_punishment_blocked_products(individual: Individual, cost_per_frame = 100) -> float:
	
	return 0


def run_simulation(
	cost_individual_func: Callable[[Individual], float],
	get_best_individual: Callable[[Population], Individual],
	get_init_population: Callable[[int, int, int, List[Product_info], Tuple[int, int]], Population],
	selection_func: Callable[[Population], Population],
	mutation_func: Callable[[Population, int, float], Population],
	hyperparameters: Hyperparameters,
	succession_func: Callable[[Population], Population] = None):
    

	mutation_power, number_individuals, max_iterations, storage_width, storage_height, products, entry = (
		hyperparameters["mutation_power"],
		hyperparameters["number_individuals"],
		hyperparameters["max_iterations"],
		hyperparameters["storage_width"],
		hyperparameters["storage_height"],
		hyperparameters["products"],
		hyperparameters["entry"]
	)
	# based on mutation function is either mutation_probability or number_products_to_mutate
	mutation_parameter = None

	if mutation_func == mutation_by_one_side_product:
		mutation_parameter = hyperparameters["number_products_to_mutate"]
	elif mutation_func == mutation_by_one_side_diff_products:
		mutation_parameter = hyperparameters["mutation_probability"]
	populations: List[Population] = []
	init_population = get_init_population(number_individuals, storage_width, storage_height, products, entry)
	# print('init population:')
	# for i in init_population:
	# 	print_products_location(i)
	# 	print('----------------------')
	populations.append(init_population)
	best_individual = get_best_individual(init_population)
	best_individual_cost = cost_individual_func(best_individual)
 
	if best_individual_cost == 0:
		return (populations, best_individual, best_individual_cost)
	number_iterations = 0
	curr_population = init_population
	for _ in range(max_iterations):
		number_iterations += 1
		curr_population = selection_func(curr_population)
		curr_population = mutation_func(curr_population, mutation_power, mutation_parameter)
		curr_best_individual = get_best_individual(curr_population)
		curr_best_individual_cost = cost_individual_func(curr_best_individual)
		# print(curr_best_individual_cost)
		if curr_best_individual_cost < best_individual_cost:
			best_individual = curr_best_individual
			best_individual_cost = curr_best_individual_cost
			if best_individual_cost == 0:
				break

		if succession_func is not None:
			curr_population = succession_func(curr_population)
		# print(f"population: {_}")
		# for i in curr_population:
		# 	print_products_location(i)
		# 	print('----------------------')
		
		populations.append(curr_population)
  
	return (populations, best_individual, best_individual_cost, number_iterations)


