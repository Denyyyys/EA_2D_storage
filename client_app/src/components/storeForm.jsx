
import { useDispatch, useSelector } from 'react-redux';
import { setStoreWidth, setStoreHeight } from '../slices/storeSizeSlice'
import { addProduct } from '../slices/productsSlice'
import { isRectangle, getRectangleSize, createEmptyArray } from '../utils/utils'
import { useState } from 'react';
import { toast } from 'react-toastify';


function StoreForm() {
	const dispatch = useDispatch();
	const { storeWidth, storeHeight } = useSelector(state => state.storeSize)
	// const { products, currentProduct } = useSelector(state => state.products)

	const [isButtonDisabled, setButtonDisabled] = useState(false);
	const clickProductCellHandler = (event) => {
		const row = event.target.dataset.row;
		const column = event.target.dataset.column;

		// dispatch(setCurrentProduct({ x: row, y: column }))
		if (event.target.dataset.clicked === "false") {
			event.target.style.backgroundColor = '#176B87';
			event.target.dataset.clicked = "true"
		}
		else {
			event.target.style.backgroundColor = '#f1f5f8';
			event.target.dataset.clicked = "false"
		}
	}
	const submitProductHandler = (event) => {
		let currentProduct = createEmptyArray(storeWidth, storeHeight);
		event.preventDefault();
		toast.clearWaitingQueue();
		setButtonDisabled(true);

		const cells = document.querySelectorAll('.store-cell');
		for (let i = 0; i < cells.length; i++) {
			const item = cells[i];
			let { row, column, clicked } = item.dataset;
			row = parseInt(row);
			column = parseInt(column);
			if (clicked === "true") {
				currentProduct[row][column] = 1;
			}
		}

		setTimeout(() => {
			setButtonDisabled(false);
		}, 3000);
		toast.dismiss();

		if (isRectangle(currentProduct)) {
			const { width, height } = getRectangleSize(currentProduct);
			dispatch(addProduct({ width, height }))
			toast.success('Success!', { position: toast.POSITION.TOP_CENTER, autoClose: 3000, closeOnClick: true });
		}
		else {
			toast.error('Error', { position: toast.POSITION.TOP_CENTER, autoClose: 3000, closeOnClick: true })
		}
	}
	const paragraphs = Array.from({ length: storeHeight * storeWidth }, (_, index) => {
		let column = (index) % storeWidth;
		let row = Math.floor(index / storeWidth);
		return (
			<div className="store-cell" key={index} data-column={column} data-row={row} data-clicked={false} onClick={clickProductCellHandler}></div>)
	});

	return (
		<form className="main-inner-container">
			<div>

				<div className="store-size-container">
					<div className="form-group">

						<label htmlFor="widthStore">Width of store (m)</label>
						<input type="number" id="widthStore" value={storeWidth} name="widthStore" min="3" max="100" placeholder="Width of store (m)" onChange={(e) => {
							dispatch(setStoreWidth(e.target.value));
							// dispatch(initCurrentProduct({
							// 	width: parseInt(e.target.value),
							// 	height: storeHeight
							// }))
						}} required />
					</div>
					<div className="form-group">
						<label htmlFor="lengthStore">Length of store (m)</label>
						<input type="number" id="widthStore" name="widthStore" min="3" max="100" placeholder="Length of store (m)" onChange={(e) => {
							dispatch(setStoreHeight(e.target.value));
							// dispatch(initCurrentProduct({
							// 	width: storeWidth,
							// 	height: parseInt(e.target.value)
							// }))
						}} value={storeHeight} required />
					</div>
				</div>/
				<p className="new-product-title">Create Forms of your products by clicking in the squares</p>
			</div>

			<div className="store-grid" style={{
				gridTemplateColumns: `repeat(${storeWidth}, 1fr)`
			}}>
				{paragraphs}
			</div>
			<button disabled={isButtonDisabled} className="submit-product-btn btn btn-success" onClick={submitProductHandler} >Submit Product</button>
		</form>
	)

}
export default StoreForm;