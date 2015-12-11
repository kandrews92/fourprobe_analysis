from search import get_idx

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

