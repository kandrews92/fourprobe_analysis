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
from compute_data import  compute_fe_mobility
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
	length4 = get_user_val('4-probe length')
	length2 = get_user_val('2-probe length')
	width4 = get_user_val('4-probe width')
	width2 = get_user_val('2-probe width')

	capacitence = get_user_val('capacitence')

	## string for four probe length header
	f_probe_str ='4probe S(uS) L/W='+str(length4)+"/"+str(width4) 
	t_probe_str = '2probe S(uS) L/W='+str(length2)+"/"+str(width2)

	## initialize data array
	data = [[[] for i in range(0,nrows)] for j in range(0,ncols)]

	## get data from orig file into array
	extract_data(wsheet,data)
	copy_data_to_newsheet(newsheet, data, ncols, nrows)

	## compute V3-V2, conductivity
	diffV,conductivity,abs_conductivity =compute_conductivity(data,newsheet,ncols,nrows, length4, width4, f_probe_str, t_probe_str)

	## init new data array of calc vals
	new_data = [[[] for i in range(0,nrows)] for j in range(0, 5)]
	## assign calc vals to new data array
	new_data[0][:] = diffV
	new_data[1][:] = conductivity
	new_data[2][:] = abs_conductivity
	## compute trace and retrace of conductivity
	trace, retrace = find_trace(data, new_data, ncols, nrows, length4, width4,f_probe_str)
	## assign trace, retrace vals to new data array
	new_data[3][:] = trace
	new_data[4][:] = retrace
	## compute FE mobility
	##...
	## write trace, retrace to new data file and 
	## place them in the correct row with corresponding Vbg
	for i in range(ncols+3, ncols+4):
		for j in range(0, len(new_data[3][:])):
			newsheet.write(j,i,new_data[3][j])
	newsheet.write(0,ncols+4,new_data[4][0])
	for i in range(ncols+4, ncols+5):
		for j in range(1, len(new_data[4][:])):
			newsheet.write(j+len(new_data[4][:])-1,i,new_data[4][j])
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
	print "4-probe L/W= ", length4,"/",width4
	print "2-probe L/W= ", length2,"/",width2
	print "*"*40
	print