def get_length():
	while True:
		try:
			length = float(raw_input('Enter length: '))
			break
		except ValueError:
			print "Enter a valid length..."
	return length

def get_width():
	while True:
		try:
			width = float(raw_input('Enter width: '))
			break
		except ValueError:
			print "Enter a valid width..."
	return width

def get_user_val(string):
	while True:
		try: 
			val = float(raw_input('Enter %s: ' %(string)))
			break
		except ValueError:
			print "Enter a valid number..."
	return val

def get_user_val_str(string):
	while True:
		try: 
			val = str(raw_input('Enter %s: ' %(string)))
			break
		except ValueError:
			print "Enter a valid number..."
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
		if f[i].endswith('.xlsx'): 
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
			#	continue
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