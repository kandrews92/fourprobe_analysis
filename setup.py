from distutils.core import setup
import py2exe

setup(name='fourprobe', 
		version='1.0',
		description='Analysis program for excel sheet and four-probe measurements',
		author='Kraig Andrews',
		author_email='kraigandrews1992@gmail.com',
		packages=['xlrd', 'xlwt', 'numpy','math', 'os', 'sys'
		],
	)
