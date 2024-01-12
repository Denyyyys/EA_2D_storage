from typing import Tuple
import constants
def get_available_positions_for_product(storage_width: int, storage_height: int, product_width: int, product_height: int) -> Tuple[int, int]:
    if product_width > storage_width or product_height > storage_height:
        raise ValueError(constants.PRODUCT_TOO_BIG_FOR_STORAGE)
    x_start_max = storage_width - product_width
    y_start_max = storage_height - product_height
    
    return (x_start_max, y_start_max)
    

def print_products_location(individual):
    products_location = individual.products_location
    
    for i in range(individual.storage_height):
        for j in range(individual.storage_width):
            print(products_location[i][j], end=" ")
        print()