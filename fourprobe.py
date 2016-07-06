#!/usr/bin/env python

class InexactFloat(float):
    def __eq__(self, other):
        try:
            return abs(self.real - other) / (0.5 * (abs(self.real) + abs(other))) < 0.0001
        except ZeroDivisionError:
            # Could do another inexact comparison here, this is just an example:
            return self.real == other

    def __ne__(self, other):
        return not self.__eq__(other)

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

def copy_data_to_newsheet(data, newsheet):
	import xlwt
	ncols = len(data)
	nrows = len(data[0][:])
	for i in range(0, ncols):
		for j in range(0, nrows):
			newsheet.write(j, i, data[i][j])

def copy_new_data_to_newsheet(data, new_data, newsheet):
	import xlwt
	ncols = len(data)
	nrows = len(data[0][:])
	for i in range(ncols, ncols+len(new_data)-4):
		for j in range(0, nrows):
			newsheet.write(j,i, new_data[i-ncols][j])

def copy_trace_retrace_to_newsheet(data, new_data, newsheet, trace_idx, str4, str2):
	import xlwt
	ncols = len(data)
	nrows = len(data[0][:])
	trace4_idx = get_idx(new_data, str4+" trace", 1)
	trace2_idx = get_idx(new_data, str2+" trace", 1)
	retrace4_idx = get_idx(new_data, str4+" retrace", 1)
	retrace2_idx = get_idx(new_data, str2+" retrace", 1)
	for i in range(0, trace_idx):
		newsheet.write(i,len(new_data)-4+ncols,new_data[trace4_idx][i])
	newsheet.write(0,len(new_data)-3+ncols,new_data[retrace4_idx][0])
	for j in range(1, trace_idx):
		newsheet.write(j+trace_idx-1,len(new_data)-3+ncols,new_data[retrace4_idx][j])
	for k in range(0, trace_idx):
		newsheet.write(k,len(new_data)-2+ncols,new_data[trace2_idx][k])
	newsheet.write(0,len(new_data)-1+ncols,new_data[retrace2_idx][0])
	for l in range(1,trace_idx):
		newsheet.write(l+trace_idx-1,len(new_data)-1+ncols, new_data[retrace2_idx][l])

def extract_data(wsheet):
	import xlrd
	ncols = wsheet.ncols
	nrows = wsheet.nrows
	data = [[[] for i in range(0, nrows)] for j in range(0, ncols)]
	for i in range(0, ncols):
		for j in range(0,nrows):
			data[i][j] = wsheet.cell(j,i).value
	return data

def wbook_init(fname, sheet_name):
	while True:
		try:
			import xlrd
		except ImportError:
			print 'Package xlrd not found...'
			break
		try:
			import sys
			wbook = xlrd.open_workbook(fname)
			wsheet = wbook.sheet_by_name(sheet_name)
		except xlrd.biffh.XLRDError:
			print "No sheet named ", sheet_name
			break
		except:
			print "Unexpected error: ", sys.exc_info()[0]
			raise
			break
		break
	return wbook, wsheet, wsheet.nrows, wsheet.ncols

def init_new_wbook(new_sheet_name):
	try:
		import xlwt
	except ImportError:
		print "Package xlwt not found"
	newbook = xlwt.Workbook()
	newsheet = newbook.add_sheet(new_sheet_name)
	return newbook, newsheet

def init_new_data(num_vals_to_computed, nrows):
	return [[[] for i in range(0,nrows)] for j in range(0,num_vals_to_computed)]

def get_user_input(string, seek=1):
	## string that is the value the user is entering
	## if seek == 1 (default) enter float
	## if seek == 2 enter string
	## if seek == 3 enter integer
	while True:
		try:
			if seek == 1:
				val = float(raw_input('Enter %s: ' %(string)))
				break
			elif seek == 2:
				val = str(raw_input('Enter %s: ' %(string)))
				break
			elif seek == 3:
				val = int(raw_input('Enter %s: ' %(string)))
				break
		except ValueError:
			print "Entry not valid, try again..."
	return val

def get_filelist():
	try:
		import os
	except ImportError:
		print "Package os not found..."
	try:
		from os import walk
	except ImportError:
		print "Package os.walk not found..."
	mypath = os.path.dirname(os.path.realpath(__file__))
	f = []
	fname = []
	for (path, dirnames, filenames) in os.walk(mypath):
		f.extend( name for name in filenames)

	for i in range(0,len(f)):
		if f[i].endswith('.xlsx') or f[i].endswith('.xls'): 
			if 'analyzed' not in f[i]:
				idx = i
				fname.append(f[idx])
	print
	print "*"*40
	print "Files available for analysis:"
	print "*"*40
	for i in range(0,len(fname)):
		print "[%d]: %s" % (i+1, fname[i])
	print "*"*40
	print "Enter the number corresponding to the file"
	print
	while True:
		try:
			file_num = int(raw_input('File number: '))
			#if 0 < (file_num - 1) or (file_num-1) >= len(fname):
			#	print "Enter a valid number..."
			#	continu	e
			if file_num-1 < 0: 
				print "Enter a valid number..."
				continue
			elif file_num -1 >= len(fname):
				print "Enter a valid number..."
				continue
			else:
				break
		except ValueError:
			print "Enter a valid number..."
	return file_num-1, fname

def get_4probe_conduct(data, len4, wid4, str4):
	v3idx = get_idx(data, 'V3', 1)
	v2idx = get_idx(data, 'V2', 1)
	Ids_idx = get_idx(data, 'Ids', 1)
	conduct4probe = [str4]
	abs_conduct4probe = ["abs "+str4]
	diffV = ['V3-V2']
	nrows = len(data[0][:])
	ncols = len(data)
	for i in range(1, nrows):
		v3_v2 = data[v3idx][i] - data[v2idx][i]
		Ids = data[Ids_idx][i]
		conduct4 = Ids/v3_v2 * len4/wid4 * 1e6
		conduct4probe.append(conduct4)
		abs_conduct4probe.append(abs(conduct4))
		diffV.append(v3_v2)
	return conduct4probe, abs_conduct4probe, diffV

def get_2probe_conduct(data, len2, wid2, str2):
	Ids_idx = get_idx(data, 'Ids', 1)
	Vds_idx = get_idx(data, 'Vds', 1)
	conduct2probe = [str2]
	abs_conduct2probe = ["abs "+str2]
	abs_Ids = ['abs Ids']
	nrows = len(data[0][:])
	ncols = len(data)
	for i in range(1, nrows):
		Ids = data[Ids_idx][i]
		Vds = data[Vds_idx][i]
		conduct2 = Ids/Vds * len2/wid2 * 1e6
		conduct2probe.append(conduct2)
		abs_conduct2probe.append(abs(conduct2))
		abs_Ids.append(abs(Ids))
	return conduct2probe, abs_conduct2probe, abs_Ids


def get_trace_retrace(data, conduct4probe, conduct2probe, str4, str2):
	from inexactfloat import InexactFloat
	ncols = len(data)
	nrows = len(data[0][:])
	Vbg_idx = get_idx(data, 'Vbg', 1)
	trace_4probe = [str4+" trace"]
	trace_2probe = [str2+" trace"]
	retrace_4probe = [str4+" retrace"]
	retrace_2probe = [str2+" retrace"]
	for i in range(2, nrows-1):
		if InexactFloat(data[Vbg_idx][i]) == InexactFloat(data[Vbg_idx][i-1]):
			trace_idx = i 
	for j in range(1, trace_idx):
		trace_4probe.append(conduct4probe[j])
		trace_2probe.append(conduct2probe[j])
	for k in range(trace_idx, nrows):
		retrace_4probe.append(conduct4probe[k])
		retrace_2probe.append(conduct2probe[k])
	return trace_4probe, retrace_4probe, trace_2probe, retrace_2probe, trace_idx

if __name__=="__main__":
	"""
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
	"""
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
