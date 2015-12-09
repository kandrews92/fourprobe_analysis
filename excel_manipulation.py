def create_wbook_sheet(fname, sheet_name):
	while True:
		try: 
			import xlrd
		except ImportError:
			print "Package xlrd not found..."
			break
		try:
			wbook = xlrd.open_workbook(fname)
			wsheet = wbook.sheet_by_name(sheet_name)
		except xlrd.biffh.XLRDError:
			print "No sheet named ", sheet_name
			break
		except:
			print "Unexpected error...:", sys.exc_info()[0]
			raise
			break
		break
	return wbook, wsheet, wsheet.nrows, wsheet.ncols

def create_new_wbook_sheet(new_sheet_name):
	try:
		import xlwt
	except ImportError:
		print "Package xlwt not found..."
	newbook = xlwt.Workbook()
	newsheet = newbook.add_sheet(new_sheet_name)
	return newbook, newsheet
