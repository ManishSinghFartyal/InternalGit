
'''
Following function will create a output python file using file handling in python 
which stores the code passed through parameters and will run this code and
return the output to be print on UI
'''
from os.path import join
import os
import subprocess

from django.conf import settings

media = settings.MEDIA_ROOT
def run_code(code,userid):	
	''' 
		a contains code user entered in given code editor
		now this code needs to create a folder which contains the user code into its respective 
		folder.
	'''
	
	hi_code = media+str(userid)+'.py' 
	a=code	
	os.makedirs(os.path.dirname(hi_code), exist_ok=True)
	with open(hi_code, "w") as f:
		f.write(a)
	f.close()
	command = 'python '+hi_code
	try:
		code_output=subprocess.check_output(command,stderr= subprocess.STDOUT,shell=True)
	except subprocess.CalledProcessError as cl:
		code_output=cl.output
		print("Error ",code_output)
	new_output=code_output.decode()
	return new_output
	