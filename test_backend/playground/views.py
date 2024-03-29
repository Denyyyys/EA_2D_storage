import random
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from typing import List, Dict, Tuple, Callable
import numpy as np


NOT_ENOUGH_SPACE_MSG = "Products cannot locate in this storage!"
PRODUCT_TOO_BIG_FOR_STORAGE = "Product width or height cannot be larger than storage!"
NO_PRODUCT_WITH_ID = "There is no product with id: {0} in storage"


Product_info = {"width": int, "height": int, "id": str}

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





def is_enough_space(list_products: List[Product_info], storage_width: int, storage_height: int) -> bool:
	total_space = 0
	for product_info in list_products:
		total_space += product_info["width"] * product_info["height"]
	return total_space < storage_width*storage_height


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


def get_available_positions_for_product(storage_width: int, storage_height: int, product_width: int, product_height: int) -> Tuple[int, int]:
    if (product_width > storage_width or product_height > storage_height) or (product_width == storage_width and product_height == storage_height):
        raise ValueError(PRODUCT_TOO_BIG_FOR_STORAGE)
    x_start_max = storage_width - product_width
    y_start_max = storage_height - product_height
    
    return (x_start_max, y_start_max)


def get_number_overlaps(products_location: List[List[List[int]]]) -> int:
    total_overlaps = 0
    for products_row in products_location:
        for product_cell in products_row:
            total_overlaps += max(0, len(product_cell) - 2)
    return total_overlaps


def get_free_space_coordinates(products_location: List[List[List[int]]]) -> List[List[int]]:
    # [x,y]
    free_spaces_arr = []
    for i in range(len(products_location)):
        for j in range((len(products_location[i]))):
            if len(products_location[i][j]) == 1:
                free_spaces_arr.append([j, i])
    return free_spaces_arr
    
    
def get_neighbors(products_location: List[List[List[int]]], point: List[int]) -> List[List[int]]:
	neighbors = []
	x = point[0]
	y = point[1]
	# top neighbor
	if y != 0:
		neighbors.append([x,y-1])
	# left neighbor
	if x != 0:
		neighbors.append([x-1, y])	
	# right neighbor	
	if x < len(products_location[0]) - 1:
		neighbors.append([x+1, y])
	# bottom neighbor	
	if y < len(products_location) - 1:
		neighbors.append([x, y+1])
	return neighbors


def is_element_present(array, element):
    for sub_array in array:
        if element == sub_array:
            return True
    return False


def find_unique_element(array1, array2):
    for element in array2:
        if element not in array1:
            return element


# def printt(product_location):
# 	for i in range(len(product_location)):
# 		for j in range(len(product_location[0])):
# 			if len(product_location[i][j]) > 1:
# 				print('#', end=' ')
# 			else:
# 				print('.', end=" ")
# 		print('')


def get_min_number_blocked_space(products_location: List[List[List[int]]]) -> int:
	free_space_arr = get_free_space_coordinates(products_location)
	number_free_space = len(free_space_arr)
	visited_space = []
	total_visited = []
	waiting_to_visit = []
	while len(visited_space) != number_free_space:
		temp = 0
		not_visited_element = find_unique_element(visited_space, free_space_arr)
		waiting_to_visit.append(not_visited_element)
		while len(waiting_to_visit) > 0:
			start_point = waiting_to_visit[0]
			neighbors = get_neighbors(products_location, start_point)
			for neighbor in neighbors:
				neighbor_x = neighbor[0]
				neighbor_y = neighbor[1]
				if len(products_location[neighbor_y][neighbor_x]) == 1 and not is_element_present(visited_space, neighbor) and not is_element_present(waiting_to_visit, neighbor):
					waiting_to_visit.append(neighbor)	
			visited_space.append(start_point)
			waiting_to_visit.pop(0)
			temp += 1
		total_visited.append(temp)
	blocked_spaces = [number_free_space - x for x in total_visited]
	min_blocked_spaces = min(blocked_spaces)
	return min_blocked_spaces


def print_products_location(individual):
    products_location = individual.products_location
    
    for i in range(individual.storage_height):
        for j in range(individual.storage_width):
            print(products_location[i][j], end="")
        print()
        
        
        
def get_product_origin_by_id(id: str, products_location) -> Tuple[int]:
    already_found = False   
    origin = [-1,-1]
    # for products_row in products_location:
    #     for product in products_row:
    #         if id in product:
    #             origin[0] = 
    for i in range(0, len(products_location)):
        if already_found:
            break
        for j in range(0, len(products_location[i])):
            if id in products_location[i][j]:
                origin[0] = j
                origin[1] = i
                already_found = True
                break
    
    if not already_found:
        raise IndexError(f"Cannot find origin of product with id: {id}") 
    return origin


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


def get_product(id:int, individual) -> Product_info:
    for product in individual.list_products:
        if product["id"] == id:
            return product
    raise ValueError("product not found!")

###################
###################
###################
###################
###################
###################
###################
###################


####################################
### Classes 	 				 ###
####################################
class Individual:
	def __init__(self, storage_width: int, storage_height: int, list_products: List[Product_info], enter_position: List[int] = [0, 1]):
		if not is_enough_space(list_products, storage_width, storage_height):
			raise ValueError(NOT_ENOUGH_SPACE_MSG)
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
                             list_products: List[Product_info], enter_position = [0, 0]):
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


	populations.append(init_population)
	best_individual = get_best_individual(init_population)
	best_individual_cost = cost_individual_func(best_individual)
 
	number_iterations = 0
	if best_individual_cost == 0:
		return (populations, best_individual, best_individual_cost, number_iterations)
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






def say_hello(request):
	mutation_probability = request.GET.get('mutation_probability', '') ################
	number_products_to_mutate = request.GET.get('number_products_to_mutate', '') ################
	mutation_power = request.GET.get('mutation_power', '')################
	number_individuals = request.GET.get('number_individuals', '')################
	max_iterations = request.GET.get('max_iterations', '')################
	storage_width = request.GET.get('storage_width', '') ################
	storage_height = request.GET.get('storage_height', '') ################
	products = request.GET.get('products', '')################
	entry = request.GET.get('entry', '') ################
	try:
		storage_width = int(storage_width)
		storage_height = int(storage_height)
		max_iterations = int(max_iterations)
		number_individuals = int(number_individuals)
		mutation_power = int(mutation_power)
		mutation_probability = float(mutation_probability)
		number_products_to_mutate = int(number_products_to_mutate)
		products = json.loads(products)
		entry = json.loads(entry)
		print(storage_height)
		print(storage_width)
		print(max_iterations)
		print(number_individuals)
		print(mutation_power)
		print(mutation_probability)
		print(number_products_to_mutate)
		print(products)
		print(len(products))
		print(entry)
		print(len(entry))
		# if (not entry) or (not products) or (not storage_height) or (not storage_width) or (not max_iterations) or (not number_individuals) \
		# 	or (not mutation_power):


		# correct_list_products = {
		# 	"products":[
		# 		{"width": 2, "height": 1, "id": "a"},
		# 		{"width": 2, "height": 2, "id": "b"},
		# 		{"width": 1, "height": 1, "id": "c"},
		# 		{"width": 1, "height": 1, "id": "d"},
		# 		{"width": 1, "height": 1, "id": "e"},
		# 		{"width": 1, "height": 1, "id": "f"},
		# 		{"width": 1, "height": 1, "id": "g"},
		# 		{"width": 1, "height": 1, "id": "h"},
		# 	],
		# 	"storage_width": 3,
		# 	"storage_height": 5
		# }
		# products, storage_width, storage_height = correct_list_products["products"], correct_list_products["storage_width"], correct_list_products["storage_height"]
		hyperparameters = {
			"mutation_probability": mutation_probability,
			"number_products_to_mutate": number_products_to_mutate,
			"mutation_power": mutation_power,
			"number_individuals": number_individuals,
			"max_iterations": max_iterations,
			"storage_width": storage_width,
			"storage_height": storage_height,
			"products": products,
			"entry": entry
		}
		populations, best_individual, best_individual_cost, number_iterations = run_simulation(
			cost_individual_func=get_cost,
			get_best_individual=get_best_individual, 
			get_init_population=create_random_population,
			selection_func=tournament_selection, 
			mutation_func=mutation_by_one_side_product, 
			hyperparameters=hyperparameters
		)

		# print(populations)
		print_products_location(best_individual)
		print(best_individual_cost)
		print(f"number iterations: {number_iterations}")
		data = {
			"best_individual_cost": best_individual_cost,
			"number_iterations": number_iterations,
			"best_individual": best_individual.products_location
		}
		response = JsonResponse(data, safe=False)
		return response
	except Exception as e:
		print('exception: ', e)
		return JsonResponse({'error': 'Erooooor'}, status=400)
