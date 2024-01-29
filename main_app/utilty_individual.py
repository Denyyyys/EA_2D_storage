from typing import List, Dict, Tuple, Callable
import constants
import random
from custom_types import Product_info, Hyperparameters

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
        raise ValueError(constants.PRODUCT_TOO_BIG_FOR_STORAGE)
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
        for j in range(len(len(products_location[i]))):
            if products_location[i][j] == ['0']:
                free_spaces_arr.append([j, i])
    return free_spaces_arr
    

def get_min_number_blocked(products_location: List[List[List[int]]]) -> int:
    free_space_arr = get_free_space_coordinates(products_location)
    