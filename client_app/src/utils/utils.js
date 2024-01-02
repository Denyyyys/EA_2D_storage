
export function isRectangle(array) {
	if (!Array.isArray(array) || array.length === 0) {
		return false; // Not a valid array
	}

	const rows = array.length;
	const columns = array[0].length;

	// Check if all rows have the same number of columns
	if (!array.every(row => row.length === columns)) {
		return false;
	}

	// Find the boundaries of the rectangle
	let minX = columns;
	let minY = rows;
	let maxX = -1;
	let maxY = -1;

	for (let i = 0; i < rows; i++) {
		for (let j = 0; j < columns; j++) {
			if (array[i][j] === 1) {
				minX = Math.min(minX, j);
				minY = Math.min(minY, i);
				maxX = Math.max(maxX, j);
				maxY = Math.max(maxY, i);
			}
		}
	}

	// Check if there are no 1s outside the rectangle formed by 1s
	for (let i = minY; i <= maxY; i++) {
		for (let j = minX; j <= maxX; j++) {
			if (array[i][j] !== 1) {
				return false;
			}
		}
	}

	return true;
}

export function getRectangleSize(array) {
	if (!Array.isArray(array) || array.length === 0) {
		return { width: 0, height: 0 }; // Not a valid array
	}

	const rows = array.length;
	const columns = array[0].length;

	// Check if all rows have the same number of columns
	if (!array.every(row => row.length === columns)) {
		return { width: 0, height: 0 }; // Not a valid rectangle
	}
	let width = 0;
	let height = 0;
	let size = 0;
	let firstOneInRow = false;
	let rowWithFirstOne = -1;
	for (let i = 0; i < rows; i++) {
		for (let j = 0; j < columns; j++) {
			if (array[i][j] === 1) {
				if (!firstOneInRow) {
					rowWithFirstOne = i;
					firstOneInRow = true
				}
				if (rowWithFirstOne === i){
					width += 1;
				}
				size += 1;
			}
		}
	}
	height = size / width;
	return {width, height}
}

export function createEmptyArray(storeWidth, storeHeight) {
  // Initialize an empty 2D array
  const newArray = [];

  // Loop to create rows
  for (let i = 0; i < storeHeight; i++) {
    // Initialize each row with zeros
    const row = Array(storeWidth).fill(0);
    newArray.push(row);
  }

  return newArray;
}



