from typing import List, Dict, Tuple, Callable
import constants
# from algorithm import Individual
Product_info = {"width": int, "height": int, "id": str}

Hyperparameters = {
	"mutation_probability": float,
	"mutation_power": int,
	"number_individuals": int,
	"max_iterations": int,
	"storage_width": int,
	"storage_height": int,
	"products": List[Product_info],
	"entry": Tuple[int, int]
}