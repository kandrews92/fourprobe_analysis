def get_idx(array, header, seek=1):
	## array containing data to search
	## header is a string to be searched for 
	## if seek = 1 (default) search columns
	## if seek = 2 search rows
	# ncols = len(array)
	# nrows = len(array[0][:])
	if seek == 1:
		for i in range(0, len(array)):
			if array[i][0] == header:
				return i
	elif seek == 2:
		for i in range(0, len(array)):
			for j in range(0, len(array[0][:])):
				if array[i][j] == header:
					return i