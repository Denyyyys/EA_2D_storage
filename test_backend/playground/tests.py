import unittest
from algorithm import Individual, create_random_population, get_next_pos_one_side
from utilty_individual import get_available_positions_for_product, is_enough_space
from mockdata import *
from utility import *
import constants

class TestEnoughSpaceCheck(unittest.TestCase):
    def test_is_enough_space(self):
        products = correct_list_products["products"]
        storage_width = correct_list_products["storage_width"]
        storage_height = correct_list_products["storage_height"]
        self.assertTrue(is_enough_space(products, storage_width, storage_height))
        
        
    def test_is_not_enough_space(self):
        products = incorrect_full_list_product["products"]
        storage_width = incorrect_full_list_product["storage_width"]
        storage_height = incorrect_full_list_product["storage_height"]
        with self.assertRaises(ValueError) as context:            
            Individual(storage_width, storage_height, products, (0, 0))

        self.assertEqual(str(context.exception), constants.NOT_ENOUGH_SPACE_MSG)
        self.assertFalse(is_enough_space(products, storage_width, storage_height))
        
        products = incorrect_too_much_products_list_product["products"]
        storage_width = incorrect_too_much_products_list_product["storage_width"]
        storage_height = incorrect_too_much_products_list_product["storage_height"]

        with self.assertRaises(ValueError) as context:            
            Individual(storage_width, storage_height, products, (0, 0))
        self.assertEqual(str(context.exception), constants.NOT_ENOUGH_SPACE_MSG)
        self.assertFalse(is_enough_space(products, storage_width, storage_height))


class TestIndividual(unittest.TestCase):
    def test_create_correct_individual(self):
        products = correct_list_products["products"]
        storage_width = correct_list_products["storage_width"]
        storage_height = correct_list_products["storage_height"]
        individual = Individual(storage_width, storage_height, products)
        # print()
        # print('Before deleting product:')
        # print_products_location(individual)
        delete_product_from_products_location(individual.products_location, "bbbb7cb9-e1e0-4ba1-a807-3f9b66ffd200")
        # print('After deleting product with id = bbbb7cb9-e1e0-4ba1-a807-3f9b66ffd200:')
        # print_products_location(individual)
        # print('After adding product with id = bbbb7cb9-e1e0-4ba1-a807-3f9b66ffd200: ')
        add_product_to_product_location(individual.products_location, 2, 2, "bbbb7cb9-e1e0-4ba1-a807-3f9b66ffd200", 1, 2)
        # print_products_location(individual)
        self.assertEqual(individual.storage_height, storage_height)
        self.assertEqual(individual.storage_width, storage_width)
        self.assertEqual(len(individual.list_products), len(products))
        
        self.assertEqual(len(individual.products_location), storage_height)
        self.assertEqual(len(individual.products_location[0]), storage_width)
        

class TestPopulation(unittest.TestCase):
    def test_creates_correct_random_population(self):
        products = correct_list_products["products"]
        storage_width = correct_list_products["storage_width"]
        storage_height = correct_list_products["storage_height"]

        population = create_random_population(10, storage_width, storage_height, products)

        # check if array has 10 elements
        self.assertEqual(len(population), 10)

        # check if every element of array is instance of class Individual
        self.assertTrue(all(isinstance(element, Individual) for element in population))
        

        
class TestUtilityFunctions(unittest.TestCase):
    def test_available_positions_success(self):
        storage_width = 4
        storage_height = 5
        product_width = 3
        product_height = 1
        x_start_max, y_start_max = get_available_positions_for_product(storage_width, storage_height, product_width, product_height)

        self.assertEqual(x_start_max, 1)
        self.assertEqual(y_start_max, 4)

    def test_available_positions_product_too_wide(self):
        storage_width = 4
        storage_height = 5
        product_width = 6
        product_height = 1

        with self.assertRaises(ValueError) as context:
            get_available_positions_for_product(storage_width, storage_height, product_width, product_height)

        self.assertEqual(str(context.exception), constants.PRODUCT_TOO_BIG_FOR_STORAGE)
        
    
    def test_available_positions_product_too_tall(self):
        storage_width = 4
        storage_height = 5
        product_width = 1
        product_height = 6

        with self.assertRaises(ValueError) as context:
            get_available_positions_for_product(storage_width, storage_height, product_width, product_height)

        self.assertEqual(str(context.exception), constants.PRODUCT_TOO_BIG_FOR_STORAGE)
        
    

class TestMutation(unittest.TestCase):
    def test_get_next_pos_one_side(self):
        pos = get_next_pos_one_side(1,3, 2, 4, 2, 3)
        a = 1
    
if __name__ == '__main__':
    unittest.main()

