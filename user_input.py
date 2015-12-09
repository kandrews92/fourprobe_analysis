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