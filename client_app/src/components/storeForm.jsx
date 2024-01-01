import { useState } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { increment, decrement } from '../slices/counterSlice';
import { setStoreWidth, setStoreHeight } from '../slices/storeSizeSlice'
function StoreForm() {
	// const dispatch = useDispatch();
	// const count = useSelector((state) => state.counterr);
	// return (
	// 	<div>
	// 		<p>{count}</p>
	// 		<button onClick={() => dispatch(increment())}>Increment</button>
	// 		<button onClick={() => dispatch(decrement())}>Decrement</button>
	// 	</div>
	// );
	const dispatch = useDispatch();
	const { storeWidth, storeHeight } = useSelector(state => state.storeSize)
	// const [storeWidth, setStoreWidth] = useState(5);
	// const [storeLength, setStoreLength] = useState(4);

	const paragraphs = Array.from({ length: storeHeight * storeWidth }, (_, index) => (
		<div className="store-cell" key={index}>{`P ${index + 1}`}</div>
	));
	// function updateSize(setterFunction, value) {
	// 	if value
	// }
	return (
		<form className="main-inner-container">
			<div className="store-size-container">
				<div className="form-group">

					<label htmlFor="widthStore">Width of store (m)</label>
					<input type="number" id="widthStore" value={storeWidth} name="widthStore" min="3" max="100" placeholder="Width of store (m)" onChange={(e) => {
						if (e.target.value == " ")
							console.log("dddddd");
						console.log(e.target.value);
						dispatch(setStoreWidth(e.target.value))
					}} required />
				</div>
				<div className="form-group">
					<label htmlFor="lengthStore">Length of store (m)</label>
					<input type="number" id="widthStore" name="widthStore" min="3" max="100" placeholder="Length of store (m)" onChange={(e) => { dispatch(setStoreHeight(e.target.value)) }} value={storeHeight} required />
				</div>
			</div>
			<div className="store-grid" style={{
				gridTemplateColumns: `repeat(${storeWidth}, 1fr)`
			}}>
				{paragraphs}
			</div>
		</form>
	)

}
export default StoreForm;