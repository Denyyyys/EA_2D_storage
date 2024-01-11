# import libraries
from typing import List, Dict, Tuple, Callable
import random
import numpy as np

# import custom modules
import constants
from utility import get_available_positions_for_product

####################################
### Classes and custom types 	 ###
####################################
class Product_info:
    def __init__(self, width: int, height: int, id: str):
        self.width = width
        self.height = height
        self.id = id


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


def create_random_products_position(list_products: List[Product_info], storage_width: int, storage_height: int) -> List[List[List[str]]]:
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
			print()
			for j in range(x, x + product["width"]):				
				products_location[i][j].append(product["id"])

	for i in range(storage_height):
		print('')
		for j in range(storage_width):
			print(products_location[i][j])
   
   
	# TODO: add products into storage
	return products_location 



def mutation(individual: Individual, mutation_power: int, mutation_probability: float) -> Individual:
	## BB
	# wybiramy losowo produkt
	# 2 implementacje zmiany położenia produktu
	pass


def get_available_positions(individual: Individual, mutation_power: int) -> List[Dict[str,Tuple[int, int]]]:
	for product in individual.list_products:
		print(product)
 	# get_available_positions_for_product(individual.storage_width, individual.storage_height, individual)
	pass


def tournament_selection(population: Population):
	## BB
	pass


def roulet_selection(population: Population):
	## BB
	pass


def threshold_selection(population: Population):
	## BB
	pass


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
    get_init_population: Callable[[int], Population],
    selection_func: Callable[[Population], Population],
    mutation_func: Callable[[Population, int, float], Population],
    succession_func: Callable[[Population], Population] = None,
    mutation_probability: float = 0.2,
    mutation_power: float = 2,
    number_individuals: int = 100,
    max_iterations: int = 100):
    
	populations: List[Population] = []
	init_population = get_init_population(number_individuals)
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