while True:
	try:
		import sys
	except ImportError:
		print "Package sys not found..."
		break
	try:
		import os
	except ImportError:
		print "Package os not found..."
		break
	try:
		from os import walk
	except ImportError:
		print "Package os.walk not found..."
		break
	try:
		import numpy as np
	except ImportError:
		print "Package numpy not found..."
		break
	"""
	try:
		from qdafile import QDAfile
	except ImportError:
		print "Package qdafile not found..."
		break
	"""
	try:
		from inexactfloat import InexactFloat
	except ImportError:
		print "Package InxeactFloat not found..."
		break
	print
	print "All packages imported successfully"
	print
	break