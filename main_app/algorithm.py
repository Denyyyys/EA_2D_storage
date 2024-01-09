import random
from typing import List, Dict

class Individual:
	def __init__(self, store_width, store_height, list_product, enter_position):

		self.list_product = create_random_individual(list_product)
		self.store_width = store_width
		self.store_height = store_height
		self.enter_position = enter_position
		

def is_enough_space(list_product: List[Dict], store_width, store_height) -> bool:
	total_space = 0
	for product_info in list_product:
		total_space += product_info["width"] * product_info["height"]
	return total_space < store_width*store_height



def create_random_individual(list_product: List[Dict]) -> List:
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


def tournament_selection(population: List[Individual]):
	## BB
	pass


def roulet_selection(population: List[Individual]):
	## BB
	pass


def threshold_selection(population: List[Individual]):
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


