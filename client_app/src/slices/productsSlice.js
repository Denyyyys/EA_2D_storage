import { createSlice } from '@reduxjs/toolkit';
import { v4 as uuidv4 } from 'uuid';

const productsSlice = createSlice({
	name: 'products',
	initialState: {
		products: []
	},
	reducers: {
		addProduct: (state, action) =>{
			if ( typeof action.payload === 'object' 
			&& action.payload !== null
			&& 'width' in action.payload 
			&& 'height' in action.payload 
			&& typeof action.payload.width === 'number' 
			&& typeof action.payload.height === 'number') {
				const {width, height} = action.payload;
				state.products.push({
					width,
					height,
					id: uuidv4()
				})
			}
		},
		removeProduct: (state, action) => {
			if (typeof action.payload === 'number') {
				const id = action.payload;
				state = state.products.filter(product => product.id !== id);
			}
		},

	},
});

export const { addProduct, removeProduct } = productsSlice.actions;
export default productsSlice.reducer;