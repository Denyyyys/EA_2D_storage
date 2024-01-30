
import { useDispatch, useSelector } from 'react-redux';
import { setStoreWidth, setStoreHeight, setBestIndividual, setBestIndividualCost, setNumberNeededIterations } from '../slices/storeSizeSlice'
import { addProduct } from '../slices/productsSlice'
import { isRectangle, getRectangleSize, createEmptyArray } from '../utils/utils'
import { useState } from 'react';
import { toast } from 'react-toastify';
import React, { useRef, useEffect } from 'react';

function StoreForm() {
	const dispatch = useDispatch();
	const { storeWidth, storeHeight, max_iterations, number_individuals, mutation_power, number_products_to_mutate, mutation_probability } = useSelector(state => state.storeSize)
	const { products, entry } = useSelector(state => state.products)
	const [selectedFile, setSelectedFile] = useState(null);
	const [isLoading, setIsLoading] = useState(false);
	const [err, setErr] = useState('');
	const [data, setData] = useState({})
	console.log(Object.keys(data).length === 0 && data.constructor === Object);
	const handleFileChange = (event) => {
		const file = event.target.files[0];
		setSelectedFile(file);
	}
	const submitResultHandler = async (event) => {
		event.preventDefault();
		toast.clearWaitingQueue();
		setIsLoading(true);
		console.log(123432);

		toast.dismiss();
		let total_space = 0
		products.forEach(product => {
			total_space += product.width * product.height
		})
		if (total_space >= storeHeight * storeWidth) {
			toast.error('Your products require more space, than you have!', { position: toast.POSITION.TOP_CENTER, autoClose: 2000, closeOnClick: true });
			return
		}
		toast.success('Your order was sent!', { position: toast.POSITION.TOP_CENTER, autoClose: 2000, closeOnClick: true });
		try {
			let data = [0, 1] //& data=${ JSON.stringify(data) }
			const url_string = `http://127.0.0.1:9000/playground/hello/?id=10232r&data=${JSON.stringify(data)}` +
				`&storage_width=${storeWidth}&storage_height=${storeHeight}&max_iterations=${max_iterations}&number_individuals=${number_individuals}` +
				`&mutation_power=${mutation_power}&number_products_to_mutate=${number_products_to_mutate}&mutation_probability=${mutation_probability}` +
				`&products=${JSON.stringify(products)}&entry=${JSON.stringify(entry)}`

			const response = await fetch(url_string, {
				method: 'GET',
				headers: {
					Accept: 'application/json',
				},
				mode: 'cors'
			});
			console.log(response);
			if (!response.ok) {
				throw new Error(`Error! status: ${response.status}`);
			}

			const result = await response.json();

			console.log('result is: ', JSON.stringify(result, null, 4));
			console.log(result.best_individual);
			dispatch(setBestIndividualCost(result.best_individual_cost))
			dispatch(setNumberNeededIterations(result.number_iterations))
			dispatch(setBestIndividual(result.best_individual))
			console.log(result.number_iterations);
			console.log(result.best_individual);
			setData(result);
			// const data = {
			// 	key1: 'value1',
			// 	key2: 'value2'
			// };
			// fetch('http://127.0.0.1:9000/playground/hello/', {
			// 	method: 'POST',
			// 	headers: {
			// 		'Content-Type': 'application/json',
			// 	},
			// 	body: JSON.stringify(data),
			// });
		} catch (err) {
			console.log(err);
			setErr(err.message);
		} finally {
			setIsLoading(false);
		}
	}
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
			const cellsDOM = document.querySelectorAll('.store-cell');
			console.log(1111111111111111111111111);
			// for (let i = 0; i < cellsDOM.length; i++) {
			// 	const item = cellsDOM[i];
			// 	console.log(item.dataset);
			// 	item.dataset.clicked = "false"
			// 	item.style.backgroundColor = '#f1f5f8';
			// }
			cellsDOM.forEach(div => {
				div.setAttribute('data-clicked', 'false');
				div.style.backgroundColor = '#f1f5f8';
			})
			toast.success('Product added successfully!', { position: toast.POSITION.TOP_CENTER, autoClose: 3000, closeOnClick: true });
		}
		else {
			toast.error('Selected Product is not a rectangle!', { position: toast.POSITION.TOP_CENTER, autoClose: 3000, closeOnClick: true })
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
						<input type="number" id="widthStore" value={storeWidth} name="widthStore" min="3" max="50" placeholder="Width of store (m)" onChange={(e) => {
							dispatch(setStoreWidth(e.target.value));
							// dispatch(initCurrentProduct({
							// 	width: parseInt(e.target.value),
							// 	height: storeHeight
							// }))
						}} required />
					</div>
					<div className="form-group">
						<label htmlFor="lengthStore">Length of store (m)</label>
						<input type="number" id="widthStore" name="widthStore" min="3" max="50" placeholder="Length of store (m)" onChange={(e) => {
							dispatch(setStoreHeight(e.target.value));
							// dispatch(initCurrentProduct({
							// 	width: storeWidth,
							// 	height: parseInt(e.target.value)
							// }))
						}} value={storeHeight} required />
					</div>
				</div>
				<p className="new-product-title">Create Forms of your products by clicking in the squares</p>
			</div>

			<div className="store-grid" style={{
				gridTemplateColumns: `repeat(${storeWidth}, 1fr)`
			}}>
				{paragraphs}
			</div>
			<button disabled={isButtonDisabled} className="submit-product-btn btn btn-success" onClick={submitProductHandler} >Submit Product</button>

			<button className="submit-product-btn btn btn-success" onClick={submitResultHandler}>Get Result!</button>
		</form>

	)
}
export default StoreForm;