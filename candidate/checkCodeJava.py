
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
from subprocess import PIPE,check_output, CalledProcessError, STDOUT
from django.conf import settings
from nitortest.models import Question
from .service import get_question_paper
media = settings.MEDIA_ROOT




def run_code(code,userid):	
	''' 
		a contains code user entered in given code editor
		now this code needs to create a folder which contains the user code into its respective 
		folder.
	'''	
	hi_code = media+str(userid)+"/"+str(userid)+'.java'
	a=code	
	os.makedirs(os.path.dirname(hi_code), exist_ok=True)
	with open(hi_code, "w") as f:
		f.write(a)
	f.close()
	command = 'java '+hi_code
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



def get_output(testcase,code,userid):
	testcase = str.encode(testcase)
	a=code
	class_name = get_class_name(a)
	hi_code = media+str(userid)+"/"+class_name+".java"
	hi_code1 = "-cp "+media+str(userid)+" "+class_name
	os.makedirs(os.path.dirname(hi_code), exist_ok=True)
	with open(hi_code, "w") as f:
		f.write(a)
	f.close()
	command = 'java '+hi_code1
	commandC = 'javac '+hi_code
	try:
		subprocess.check_output(commandC,shell=True,stderr=STDOUT)
	except subprocess.CalledProcessError as cl:
		code_output=cl.output
		new_output=code_output.decode()
		return new_output
	try:
		code_output=subprocess.check_output(command,stderr= subprocess.STDOUT,shell=True,input = testcase)
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
		new_output = get_output(value,code,userid)
		if new_output.strip() != old_output.strip():
			answers[case] = {"input":value,"result":"incorrect","your_output":new_output,"expected_output":old_output}
		else:
			answers[case] = {"result":"correct","your_output":new_output,"expected_output":old_output}	
	return answers



def show_output(code,userid,queid):
	testcase = str.encode(testcase)
	hi_code = media+str(userid)+"/"+str(userid)
	a=code	
	os.makedirs(os.path.dirname(hi_code), exist_ok=True)
	with open(hi_code, "w") as f:
		f.write(a)
	f.close()
	command = 'java '+hi_code
	try:
		code_output=subprocess.check_output(command,stderr= subprocess.STDOUT,shell=True,input = testcase)
	except subprocess.CalledProcessError as cl:
		code_output=cl.output
	new_output=code_output.decode()
	return new_output


def get_class_name(code):
	lines = code.split("\n")
	for line in lines:
		if 'class' in line:
			class_name = line.split(" ")
			if class_name[0] == 'public':
				name = class_name[2]
			else:
				name =class_name[1]
			break
	return name.strip()
