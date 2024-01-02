import { combineReducers } from 'redux';
import storeSizeReducer from '../slices/storeSizeSlice'; 
import productsReducer from '../slices/productsSlice';
const rootReducer = combineReducers({
	storeSize: storeSizeReducer,
	products: productsReducer
});

export default rootReducer;