import { useDispatch, useSelector } from 'react-redux';

function Result() {
	const { best_individual_cost, number_needed_iterations, best_individual } = useSelector(state => state.storeSize)
	const { storeWidth, storeHeight, max_iterations, number_individuals, mutation_power, number_products_to_mutate, mutation_probability } = useSelector(state => state.storeSize)

	let paragraphs = Array.from({ length: storeHeight * storeWidth }, (_, index) => {
		let column = (index) % storeWidth;
		let row = Math.floor(index / storeWidth);

		return (
			<div className="store-cell" key={index} data-column={column} data-row={row} data-clicked={false}></div>)
	});
	if (best_individual) {
		paragraphs = Array.from({ length: storeHeight * storeWidth }, (_, index) => {
			let column = (index) % storeWidth;
			let row = Math.floor(index / storeWidth);
			let element = best_individual[row][column]
			let content = ''
			if (element.length > 1) {
				console.log(element);
				element = element.slice(1);
				content = element.map(str => str.substring(0, 5)).join(", ");
			}

			return (
				<div className="store-cell" key={index} data-column={column} data-row={row} data-clicked={false}>{content}</div>)
		});
	}
	if (best_individual_cost != null) {
		return (
			<div>
				<p style={{ textAlign: 'center', fontSize: '1.25rem', marginTop: '20px', fontWeight: 'bold' }}>
					Best found individual cost: {best_individual_cost}
				</p>

				<p style={{ textAlign: 'center', fontSize: '1.25rem', marginBottom: '20px', fontWeight: 'bold' }}>
					Number of iteration: {number_needed_iterations}
				</p>
				<div className="store-grid" style={{
					gridTemplateColumns: `repeat(${storeWidth}, 1fr)`
				}}>
					{paragraphs}
				</div>
			</div>
		)

	}
	return <div>
		<p style={{ textAlign: 'center', fontSize: '1.25rem', marginTop: '20px', fontWeight: 'bold' }}>

			Please Submit Your Form
		</p>
	</div>
}
export default Result