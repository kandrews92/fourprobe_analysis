if __name__=="__main__":
	from user_input import get_filelist, get_user_input
	from excel_manip import copy_data_to_newsheet
	from excel_manip import copy_new_data_to_newsheet
	from excel_manip import copy_trace_retrace_to_newsheet
	from excel_manip import extract_data
	from excel_manip import wbook_init, init_new_data
	from excel_manip import init_new_wbook
	from compute import get_4probe_conduct
	from compute import get_2probe_conduct
	from compute import get_trace_retrace
	import xlrd
	import xlwt

	num_vals_to_computed = 10 ## number of new vals to be found 
	file_num, f_list = get_filelist()
	fname = f_list[file_num]
	temp1 = fname.strip('.xlsx')
	new_file_name = temp1+'_analyzed.xls'

	len4 = get_user_input('4-probe length')
	wid4 = get_user_input('4-probe width')
	len2 = get_user_input('2-probe length')
	wid2 = get_user_input('2-probe width')
	str2 = 'S(us) 2-probe L/W='+str(len2)+'/'+str(wid2)
	str4 = 'S(us) 4-probe L/W='+str(len4)+'/'+str(wid4)
	
	sheet_name = 'Data'
	new_sheet_name = 'Data'
	
	## init workbook and initial excel files
	wbook, wsheet, nrows, ncols = wbook_init(fname, sheet_name)
	## init wbook to save data to
	newbook, newsheet = init_new_wbook(new_sheet_name)
	data = extract_data(wsheet) ## init orig data into array
	## init new_data array
	new_data = init_new_data(num_vals_to_computed, nrows)
	
	## compute 4 probe values of conductivity
	conduct4probe, abs_conduct4probe, diffV = get_4probe_conduct(data, len4, wid4, str4)
	## compute 2 probe values of conductivity
	conduct2probe, abs_conduct2probe, abs_Ids = get_2probe_conduct(data, len2, wid4, str2)
	## compute trace, retrace of 2 and 4 probe conduct
	trace_4probe, retrace_4probe, trace_2probe, retrace_2probe, trace_idx = \
		get_trace_retrace(data, conduct4probe, conduct2probe, str4, str2)

	new_data[0][:] = abs_Ids 
	new_data[1][:] = diffV
	new_data[2][:] = conduct4probe
	new_data[3][:] = abs_conduct4probe
	new_data[4][:] = conduct2probe
	new_data[5][:] = abs_conduct2probe
	new_data[6][:] = trace_4probe
	new_data[7][:] = retrace_4probe
	new_data[8][:] = trace_2probe
	new_data[9][:] = retrace_2probe

	copy_data_to_newsheet(data, newsheet)
	copy_new_data_to_newsheet(data, new_data, newsheet)
	copy_trace_retrace_to_newsheet(data, new_data, newsheet, trace_idx, str4, str2)

	## save new workbook and error check
	try:
		newbook.save(new_file_name)
	except IOError:
		print "*** IOError was raised..."
		print "*** Check to make sure ", new_file_name, " is not open"
	## output final program stats
	print

	print
	print "*"*40
	print "Program complete "
	print "*"*40
	print
	print "Original data file: ", fname
	print
	print "New data file: ", new_file_name
	print "*"*40
