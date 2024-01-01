import { useState } from "react";

export default function StoreForm() {
	const [storeWidth, setStoreWidth] = useState(5);
	const [storeLength, setStoreLength] = useState(4);

	const paragraphs = Array.from({ length: storeLength * storeWidth }, (_, index) => (
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
						setStoreWidth(e.target.value)
					}} required />
				</div>
				<div className="form-group">
					<label htmlFor="lengthStore">Length of store (m)</label>
					<input type="number" id="widthStore" name="widthStore" min="3" max="100" placeholder="Length of store (m)" onChange={(e) => { setStoreLength(e.target.value) }} value={storeLength} required />
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