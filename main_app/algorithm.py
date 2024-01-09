import random
from typing import List, Dict, Tuple, Callable

####################################
### Classes and custom types 	 ###
####################################
class Product_info:
    def __init__(self, width: int, height: int, id: str):
        self.width = width
        self.height = height
        self.id = id


class Individual:
	def __init__(self, store_width: int, store_height: int, list_product: List[Product_info], enter_position: Tuple[int, int]):
		self.products_location = create_random_products_position(list_product)
		self.store_width = store_width
		self.store_height = store_height
		self.enter_position = enter_position


Population = List[Individual]

####################################
### Functions for EA 			 ###
####################################
def is_enough_space(list_product: List[Product_info], store_width: int, store_height: int) -> bool:
	total_space = 0
	for product_info in list_product:
		total_space += product_info["width"] * product_info["height"]
	return total_space < store_width*store_height


def get_best_individual(population: Population) -> Individual:
    sorted_pop = sort_population(population)
    return sorted_pop[0]


def get_random_population(number_individuals: int, store_width: int, store_height: int, list_product: List[Product_info], enter_position: Tuple[int, int]):
    population = [Individual(store_width, store_height, list_product, enter_position) for _ in range(number_individuals)]
    return population


def sort_population(population: Population):
    return sorted(population, key=get_cost)


def create_random_products_position(list_product: List[Dict]) -> List:
	# DF
	pass


def mutation(individual: Individual, mutation_power: int, mutation_probability: float) -> Individual:
	## BB
	# wybiramy losowo produkt
	# 2 implementacje zmiany położenia produktu
	pass


def get_available_positions(individual: Individual, mutation_power: int) -> List:
	## BB
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
    ## DF
	pass


def get_punishment(individual: Individual) -> float:
	## DF
	pass


def get_punishment_overlap(individual: Individual, cost = 400) -> float:
	## DF
	pass


def get_punishment_cannot_enter(individual: Individual, cost = 400) -> float:
	## DF
	pass


def get_punishment_blocked_free_space(individual: Individual, cost = 400) -> float:
	## DF
	pass


def get_punishment_blocked_products(individual: Individual, cost_per_frame = 100) -> float:
	## DF
	pass


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
