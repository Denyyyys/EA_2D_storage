import { combineReducers } from 'redux';
import counterReducer from '../slices/counterSlice';
import storeSizeReducer from '../slices/storeSizeSlice'; 
const rootReducer = combineReducers({
//   counter: counterReducer,
	storeSize: storeSizeReducer
  // Add other reducers here
});

export default rootReducer;