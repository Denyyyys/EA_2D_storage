from algorithm import *
if __name__ == '__main__':
    correct_list_products = {
        "products":[
            {"width": 2, "height": 1, "id": "aaaa7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
            {"width": 2, "height": 2, "id": "bbbb7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
            {"width": 1, "height": 1, "id": "cccc7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
            {"width": 1, "height": 1, "id": "dddd7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
            {"width": 1, "height": 1, "id": "eeee7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
        ],
        "storage_width": 3,
        "storage_height": 5
    }
    products, storage_width, storage_height = correct_list_products["products"], correct_list_products["storage_width"], correct_list_products["storage_height"]
    hyperparameters = {
        "mutation_probability": 0.2,
        "mutation_power": 2,
        "number_individuals": 10,
        "max_iterations": 100,
        "storage_width": storage_width,
        "storage_height": storage_height,
        "products": products,
        "entry": (0,0)
    }
    
    populations, best_individual, best_individual_cost = run_simulation(
        get_cost, get_best_individual, create_random_population,
        tournament_selection, mutation_by_one_side, hyperparameters)
    
    print(populations)
