from typing import List, Dict, Tuple, Callable
import constants

from custom_types import Product_info, Hyperparameters


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