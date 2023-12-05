export default function storeForm() {
	return (
		<form>
			<label for="tentacles">Number of tentacles (10-100):</label>

			<input type="number" id="tentacles" name="tentacles" min="10" max="100" />
		</form>
	)
}