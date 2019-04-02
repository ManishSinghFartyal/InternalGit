
'''
Following function will create a output python file using file handling in python 
which stores the code passed through parameters and will run this code and
return the output to be print on UI
'''
from os.path import join
import os
import subprocess
def run_code(code):
	'''
	a contains all the code coming from UI
	'''
	a=code
	# saving this file into .py file	
	file = open('output.py','w')
	file.write(a)	
	file.close()		
	#To print the file content
	#print(file.read())
	#To print the file directory
	#print(os.path.realpath(file.name))

	# To run the code in python shell
	#output=os.system('python output.py')
	#print(output)
	try:
		code_output=subprocess.check_output('java output.java',stderr= subprocess.STDOUT,shell=True)
		print('Your output is ready :',code_output)
	except subprocess.CalledProcessError as cl:
		code_output=cl.output
		print("Error ",code_output)
	new_output=code_output.decode()
	#print(new_output)		
	return new_output
	