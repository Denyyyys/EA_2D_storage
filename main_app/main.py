from algorithm import *
if __name__ == '__main__':
    correct_list_products = {
        # "products":[
        #     {"width": 2, "height": 1, "id": "aaaa7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
        #     {"width": 2, "height": 2, "id": "bbbb7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
        #     {"width": 1, "height": 1, "id": "cccc7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
        #     {"width": 1, "height": 1, "id": "dddd7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
        #     {"width": 1, "height": 1, "id": "eeee7cb9-e1e0-4ba1-a807-3f9b66ffd200"},
        # ],
        # "products":[
        #     {"width": 2, "height": 1, "id": "a"},
        #     {"width": 2, "height": 2, "id": "b"},
        #     {"width": 1, "height": 1, "id": "c"},
        #     {"width": 1, "height": 1, "id": "d"},
        #     {"width": 1, "height": 1, "id": "e"},
        # ],
        # "storage_width": 3,
        # "storage_height": 5
        "products":[
            {"width": 2, "height": 1, "id": "a"},
            {"width": 2, "height": 2, "id": "b"},
            {"width": 1, "height": 1, "id": "c"},
            {"width": 1, "height": 1, "id": "d"},
            {"width": 1, "height": 1, "id": "e"},
            {"width": 1, "height": 1, "id": "f"},
            {"width": 1, "height": 1, "id": "g"},
            {"width": 1, "height": 1, "id": "h"},
        ],
        "storage_width": 3,
        "storage_height": 5
    }
    products, storage_width, storage_height = correct_list_products["products"], correct_list_products["storage_width"], correct_list_products["storage_height"]
    hyperparameters = {
        "mutation_probability": 1,
        "number_products_to_mutate": 2,
        "mutation_power": 5,
        "number_individuals": 10,
        "max_iterations": 100,
        "storage_width": storage_width,
        "storage_height": storage_height,
        "products": products,
        "entry": [0,1]
    }
    
    populations, best_individual, best_individual_cost, number_iterations = run_simulation(
        cost_individual_func=get_cost,
        get_best_individual=get_best_individual, 
        get_init_population=create_random_population,
        selection_func=tournament_selection, 
        mutation_func=mutation_by_one_side_product, 
        hyperparameters=hyperparameters
    )
    print("Best individual products location:")
    print_products_location(best_individual)
    print(f"best individual cost: {best_individual_cost}")
    print(f"number iterations: {number_iterations}")
