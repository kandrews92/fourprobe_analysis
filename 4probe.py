"""
Author: Kraig Andrews

Version: 1.0.0

Date Created: Dec. 8, 2015

"""

## importing various functions, classes, and packages from 
## other python files. These are required.
from imports import *
from search_tools import find_col_idx
from copy_data import extract_data, copy_data_to_newsheet
from copy_data import write_computed_data_to_new_excel
from compute_data import find_trace, compute_conductivity
from excel_manipulation import create_wbook_sheet
from excel_manipulation import create_new_wbook_sheet
from user_input import get_filelist, get_user_val

if __name__=="__main__":
	error = 0 	## error counter
	sheet_name = 'Data' ## sheet name of orig data file
	new_sheet_name = 'Data' ## sheet name of new data file
	
	file_num, f_list = get_filelist() ## get file list in pwd
	fname = f_list[file_num]  ## assign name
	temp1 = fname.strip('.xlsx') ## strip file ext for new file name
	new_file_name = temp1+'_analyzed.xls' ## assign new file name

	## copy data and init new sheets and workbooks
	wbook, wsheet, nrows, ncols = create_wbook_sheet(fname, sheet_name)
	newbook, newsheet = create_new_wbook_sheet(new_sheet_name)

	## get user input values
	length = get_user_val('length')
	width = get_user_val('width')


	## initialize data array
	data = [[[] for i in range(0,nrows)] for j in range(0,ncols)]

	## get data from orig file into array
	extract_data(wsheet,data)
	copy_data_to_newsheet(newsheet, data, ncols, nrows)

	## compute V3-V2, conductivity
	diffV,conductivity =compute_conductivity(data,newsheet,ncols,nrows, length, width)

	## init new data array of calc vals
	new_data = [[[] for i in range(0,nrows)] for j in range(0, 4)]
	## assign calc vals to new data array
	new_data[0][:] = diffV
	new_data[1][:] = conductivity
	## compute trace and retrace of conductivity
	trace, retrace = find_trace(data, new_data, ncols, nrows, length, width)
	## assign trace, retrace vals to new data array
	new_data[2][:] = trace
	new_data[3][:] = retrace
	## write trace, retrace to new data file and 
	## place them in the correct row with corresponding Vbg
	for i in range(ncols+2, ncols+3):
		for j in range(0, len(new_data[2][:])):
			newsheet.write(j,i,new_data[2][j])
	newsheet.write(0,ncols+3,new_data[3][0])
	for i in range(ncols+3, ncols+4):
		for j in range(1, len(new_data[3][:])):
			newsheet.write(j+len(new_data[3][:])-1,i,new_data[3][j])
	## finish writing to new excel file
	write_computed_data_to_new_excel(new_data, newsheet, ncols, nrows)
	## save new workbook and error check
	try:
		newbook.save(new_file_name)
	except IOError:
		print "IOError was raised..."
		print "Check to make sure ", new_file_name, " is not open"
		error +=1
	## output final program stats
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