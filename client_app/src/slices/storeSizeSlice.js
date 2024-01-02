import { createSlice } from '@reduxjs/toolkit';

const storeSizeSlice = createSlice({
	name: 'storeSize',
	initialState: {
		storeWidth: 4,
		storeHeight: 3
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
	},
});

export const { setStoreWidth, setStoreHeight } = storeSizeSlice.actions;
export default storeSizeSlice.reducer;