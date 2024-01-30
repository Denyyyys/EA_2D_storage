import { createSlice } from '@reduxjs/toolkit';

const storeSizeSlice = createSlice({
	name: 'storeSize',
	initialState: {
		storeWidth: 4,
		storeHeight: 3,
		max_iterations: 100,
		number_individuals: 20,
		mutation_power: 2,
		mutation_probability: 0.5,
		number_products_to_mutate: 2,
		best_individual_cost: null,
		number_needed_iterations: null,
		best_individual: null
	},
	reducers: {
		setStoreWidth: (state, action) => {
			console.log();
			if (action.payload !== "")
				state.storeWidth = parseInt(action.payload);
		},
		setStoreHeight: (state, action) =>{
			if (action.payload !== "")
				state.storeHeight = parseInt(action.payload);
		},
		setMaxIterations: (state, action) =>{
			if (action.payload !== "")
				state.max_iterations = parseInt(action.payload);
		},
		setNumberIndividuals: (state, action) =>{
			if (action.payload !== "")
				state.number_individuals = parseInt(action.payload);
		},
		setMutationPower: (state, action) =>{
			if (action.payload !== "")
				state.mutation_power = parseInt(action.payload);
		},
		setMutationProbability: (state, action) =>{
			if (action.payload !== "")
				state.mutation_probability = parseInt(action.payload);
		},
		setNumberProductsToMutate: (state, action) =>{
			if (action.payload !== "")
				state.number_products_to_mutate = parseInt(action.payload);
		},
		setBestIndividualCost: (state, action) =>{
			if (action.payload !== "")
				state.best_individual_cost = parseInt(action.payload);
		},
		setNumberNeededIterations: (state, action) =>{
			if (action.payload !== "")
				state.number_needed_iterations = parseInt(action.payload);
		},
		setBestIndividual: (state, action) =>{
			if (action.payload !== "")
				state.best_individual = action.payload;
		},
	},
});

export const { setStoreWidth, setStoreHeight, setMaxIterations, setNumberIndividuals, setMutationPower, setMutationProbability, setNumberProductsToMutate,setBestIndividual,setBestIndividualCost,setNumberNeededIterations } = storeSizeSlice.actions;
export default storeSizeSlice.reducer;