import { createSlice } from '@reduxjs/toolkit';

const storeSizeSlice = createSlice({
	name: 'storeSize',
	initialState: {
		storeWidth: 3,
		storeHeight: 4
	},
	reducers: {
		setStoreWidth: (state, action) => {
			console.log(action);
			if (action.payload !== "")
				state.storeWidth = action.payload;
		},
		setStoreHeight: (state, action) =>{
			if (action.payload !== "")
				state.storeHeight = action.payload
		},
	},
});

export const { setStoreWidth, setStoreHeight } = storeSizeSlice.actions;
export default storeSizeSlice.reducer;