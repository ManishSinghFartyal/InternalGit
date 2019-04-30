
'''
Following function will create a output python file using file handling in python 
which stores the code passed through parameters and will run this code and
return the output to be print on UI
'''
import ast
import json
from os.path import join
import os
import subprocess
from subprocess import PIPE
from django.conf import settings
from nitortest.models import Question
from .service import get_question_paper
from Naked.toolshed.shell import execute_js, muterun_js
from subprocess import Popen, PIPE

media = settings.MEDIA_ROOT




def run_code(code,userid):	
	''' 
		a contains code user entered in given code editor
		now this code needs to create a folder which contains the user code into its respective 
		folder.
	'''	
	hi_code = media+str(userid)+"/"+str(userid)+'.py'
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
	new_output=code_output.decode()
	return new_output




def fetch_test_cases(queid):
	que= Question.objects.get(id=queid)
	if que.qtype == "ct":
		testcases=ast.literal_eval(que.testcases)
		testcases=json.dumps(testcases)
		testcases=json.loads(testcases)
	return testcases



def get_output(testcase,code,userid,queid):
	testcase = str.encode(testcase)
	hi_code = media+str(userid)+"/"+str(userid)+'.js'
	a=code	
	os.makedirs(os.path.dirname(hi_code), exist_ok=True)
	with open(hi_code, "w") as f:
		f.write(a)
	f.close()
	command = 'node '+hi_code	
	try:		
		code_output=subprocess.check_output(command,stderr= subprocess.STDOUT,shell=True,input = testcase)
		print(code_output)
	except subprocess.CalledProcessError as cl:
		code_output=cl.output
	new_output=code_output.decode()
	return new_output




def run_code2(code,userid,queid):	
	''' 
		a contains code user entered in given code editor
		now this code needs to create a folder which contains the user code into its respective 
		folder.
	'''
	testcases  = fetch_test_cases(queid)
	answers = {}
	for case in testcases:
		value=testcases[case]['testcase']
		old_output=testcases[case]['output']
		new_output = get_output(value,code,userid,queid)
		if new_output.strip() != old_output.strip():
			answers[case] = {"input":value,"result":"incorrect","your_output":new_output,"expected_output":old_output}
		else:
			answers[case] = {"result":"correct","your_output":new_output,"expected_output":old_output}	
	return answers


def show_output(code,userid,queid):
	testcase = str.encode(testcase)
	hi_code = media+str(userid)+"\\"+str(userid)+'.js'
	a=code	
	os.makedirs(os.path.dirname(hi_code), exist_ok=True)
	with open(hi_code, "w") as f:
		f.write(a)
	f.close()
	command = 'node '+hi_code
	try:
		code_output=subprocess.check_output(command,stderr= subprocess.STDOUT,shell=True,input = testcase)
	except subprocess.CalledProcessError as cl:
		code_output=cl.output
	new_output=code_output.decode()
	return new_output