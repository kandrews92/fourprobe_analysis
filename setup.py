from distutils.core import setup
import py2exe

setup(
		console=['analyze_fourprobe.py'],
		name='analyze_fourprobe', 
		version='1.0',
		description='Analysis program for excel sheet and four-probe measurements',
		author='Kraig Andrews',
		author_email='kraigandrews1992@gmail.com',
	)
