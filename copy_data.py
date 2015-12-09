def extract_data(wsheet,data):
	ncols = wsheet.ncols
	nrows = wsheet.nrows
	for i in range(0,ncols):
		data[i][0] = wsheet.cell(0,i).value
	for i in range(0,ncols):
		for j in range(1,nrows):
			data[i][j] = wsheet.cell(j,i).value
	#return data

def copy_data_to_newsheet(newsheet, data, ncols, nrows):
	for i in range(0,ncols):
		for j in range(0,nrows):
			newsheet.write(j,i,data[i][j])

def write_computed_data_to_new_excel(new_data, newsheet, ncols, nrows):
	k = 0
	for i in range(ncols, ncols+len(new_data)-2):
		for j in range(0, nrows):
			newsheet.write(j,i,new_data[k][j])
		k += 1