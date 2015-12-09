from imports import *
from search_tools import find_col_idx
from copy_data import extract_data, copy_data_to_newsheet
from copy_data import write_computed_data_to_new_excel
from compute_data import find_trace, compute_conductivity
from excel_manipulation import create_wbook_sheet
from excel_manipulation import create_new_wbook_sheet
from user_input import get_length, get_width



if __name__=="__main__":
	error = 0 
	fname = 'kraig.xlsx'
	sheet_name = 'Data'
	new_sheet_name = 'Data'
	new_file_name = 'kraig_new.xls'
	wbook, wsheet, nrows, ncols = create_wbook_sheet(fname, sheet_name)
	newbook, newsheet = create_new_wbook_sheet(new_sheet_name)

	length = get_length()
	width = get_width()

	## initialize data array
	data = [[[] for i in range(0,nrows)] for j in range(0,ncols)]

	extract_data(wsheet,data)
	copy_data_to_newsheet(newsheet, data, ncols, nrows)

	diffV,conductivity =compute_conductivity(data,newsheet,ncols,nrows, length, width)

	new_data = [[[] for i in range(0,nrows)] for j in range(0, 4)]
	new_data[0][:] = diffV
	new_data[1][:] = conductivity
	trace, retrace = find_trace(data, new_data, ncols, nrows, length, width)
	new_data[2][:] = trace
	new_data[3][:] = retrace

	for i in range(ncols+2, ncols+3):
		for j in range(0, len(new_data[2][:])):
			newsheet.write(j,i,new_data[2][j])
	newsheet.write(0,ncols+3,new_data[3][0])
	for i in range(ncols+3, ncols+4):
		for j in range(1, len(new_data[3][:])):
			newsheet.write(j+len(new_data[3][:])-1,i,new_data[3][j])

	write_computed_data_to_new_excel(new_data, newsheet, ncols, nrows)
	try:
		newbook.save(new_file_name)
	except IOError:
		print "IOError was raised..."
		print "Check to make sure ", new_file_name, " is not open"
		error +=1
	print
	print "*"*40
	print "Program complete..."
	print "Number of errors raised: ", error
	if error != 0:
		print "File ", new_file_name, " was not written properly, check errors..."
	print
	print "Original data file: ", fname
	print "Created data file: ", new_file_name
	print "L/W= ", length,"/",width
	print "*"*40
	print