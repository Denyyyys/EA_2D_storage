import unittest
from algorithm import Individual, is_enough_space
from mockdata import *

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
        
        self.assertFalse(is_enough_space(products, store_width, store_height))
        
        products = incorrect_too_much_products_list_product["products"]
        store_width = incorrect_too_much_products_list_product["store_width"]
        store_height = incorrect_too_much_products_list_product["store_height"]
        
        self.assertFalse(is_enough_space(products, store_width, store_height))




if __name__ == '__main__':
    unittest.main()
