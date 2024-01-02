import { useDispatch, useSelector } from 'react-redux';
import { removeProduct } from '../slices/productsSlice';
import { toast } from 'react-toastify';
function ShapesList() {
	const dispatch = useDispatch();
	const { products } = useSelector(state => state.products)
	console.log(products);
	return (
		<div className="main-inner-container shapes-container">
			<div>
				{products.map({ width, height, id })}
			</div>

		</div>
	)
}
export default ShapesList