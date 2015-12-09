def find_col_idx(data, col_str, ncols):
	try:
		for i in range(0, ncols):
			if data[i][0] == col_str:
				return i
	except ValueError:
		print "Header ", col_str, " not found"
		return None
	except IndexError:
		print "Header ", col_str, " not found, IndexError"