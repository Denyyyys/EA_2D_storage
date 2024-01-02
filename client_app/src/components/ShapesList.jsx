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
				<p className='shapes-title'>Your Products</p>

				<div className='direct-shapes-container'>

					{products.map(({ width, height, id }) => {
						const widthArr = new Array(width).fill(0);
						const heightArr = new Array(height).fill(0);
						return <div className='single-shape-container' style={{ maxWidth: `${85 * width}px`, maxHeight: `${85 * height}px`, border: '1px solid red;' }}>
							<table>
								{heightArr.map(_ => {
									return <tr>
										{widthArr.map(i => {
											return <td></td>
										})}
									</tr>
								})}
							</table>
						</div>
					})}

				</div>

			</div>
		</div>
	)
}
export default ShapesList