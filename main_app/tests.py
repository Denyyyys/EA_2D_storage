import unittest
from algorithm import *
from mockdata import *
import constants
class TestEnoughSpaceCheck(unittest.TestCase):
    def test_is_enough_space(self):
        products = correct_list_products["products"]
        store_width = correct_list_products["store_width"]
        store_height = correct_list_products["store_height"]
        self.assertTrue(is_enough_space(products, store_width, store_height))
        
        
    def test_is_not_enough_space(self):
        products = incorrect_full_list_product["products"]
        store_width = incorrect_full_list_product["store_width"]
        store_height = incorrect_full_list_product["store_height"]
        with self.assertRaises(ValueError) as context:            
            Individual(store_width, store_height, products, (0, 0))

        self.assertEqual(str(context.exception), constants.NOT_ENOUGH_SPACE_MSG)

        self.assertFalse(is_enough_space(products, store_width, store_height))
        
        products = incorrect_too_much_products_list_product["products"]
        store_width = incorrect_too_much_products_list_product["store_width"]
        store_height = incorrect_too_much_products_list_product["store_height"]

        with self.assertRaises(ValueError) as context:            
            Individual(store_width, store_height, products, (0, 0))

        self.assertEqual(str(context.exception), constants.NOT_ENOUGH_SPACE_MSG)
        self.assertFalse(is_enough_space(products, store_width, store_height))


class TestIndividual(unittest.TestCase):
    def test_create_correct_individual(self):
        products = correct_list_products["products"]
        store_width = correct_list_products["store_width"]
        store_height = correct_list_products["store_height"]
        individual = Individual(store_width, store_height, products)
        
        self.assertEqual(individual.store_height, store_height)
        self.assertEqual(individual.store_width, store_width)
        self.assertEqual(len(individual.list_products), len(products))
        print(individual.products_location)
        
        

class TestPopulation(unittest.TestCase):
    def test_creates_correct_random_population(self):
        products = correct_list_products["products"]
        store_width = correct_list_products["store_width"]
        store_height = correct_list_products["store_height"]
        # individual = Individual(store_width, store_height, products)

        population = create_random_population(10, store_width, store_height, products)

        # check if array has 10 elements
        self.assertEqual(len(population), 10)

        # check if every element of array is instance of class Individual
        self.assertTrue(all(isinstance(element, Individual) for element in population))

        
                


if __name__ == '__main__':
    unittest.main()

