"""
Following function will create a output python file using file handling in python
which stores the code passed through parameters and will run this code and
return the output to be print on UI
"""
import ast
import json
import os
import subprocess
from subprocess import STDOUT
from django.conf import settings
from nitortest.models import Question
MEDIA = settings.MEDIA_ROOT


def run_code(code, userid):
    """
        a contains code user entered in given code editor
        now this code needs to create a folder which contains the user code into its respective
        folder.
    """
    hi_code = MEDIA+str(userid)+"/"+str(userid)+'.java'
    _a = code
    os.makedirs(os.path.dirname(hi_code), exist_ok=True)
    with open(hi_code, "w") as _f:
        _f.write(_a)
    _f.close()
    command = 'java ' + hi_code
    try:
        code_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as c_l:
        code_output = c_l.output
    new_output = code_output.decode()
    return new_output


def fetch_test_cases(queid):
    """
    a contains code user entered in given code editor
    now this code needs to create a folder which contains the user code into its respective
    folder.
    """
    que = Question.objects.get(id=queid)
    if que.qtype == "ct":
        testcases = ast.literal_eval(que.testcases)
        testcases = json.dumps(testcases)
        testcases = json.loads(testcases)
    return testcases


def get_output(testcase, code, userid):
    """ TO get output"""
    testcase = str.encode(testcase)
    _a = code
    class_name = get_class_name(_a)
    hi_code = MEDIA+str(userid)+"/"+class_name+".java"
    hi_code1 = "-cp "+MEDIA+str(userid)+" "+class_name
    os.makedirs(os.path.dirname(hi_code), exist_ok=True)
    with open(hi_code, "w") as _f:
        _f.write(_a)
    _f.close()
    command = 'java ' + hi_code1
    command_c = 'javac ' + hi_code
    try:
        subprocess.check_output(command_c, shell=True, stderr=STDOUT)
    except subprocess.CalledProcessError as c_l:
        code_output = c_l.output
        new_output = code_output.decode()
        return new_output
    try:
        code_output = subprocess.check_output(command, stderr=subprocess.STDOUT,\
         shell=True, input=testcase)
    except subprocess.CalledProcessError as c_l:
        code_output = c_l.output
    new_output = code_output.decode()
    return new_output


def run_code2(code, userid, queid):
    """
        a contains code user entered in given code editor
        now this code needs to create a folder which contains the user code into its respective
        folder.
    """
    testcases = fetch_test_cases(queid)
    answers = {}
    for case in testcases:
        value = testcases[case]['testcase']
        old_output = testcases[case]['output']
        new_output = get_output(value, code, userid)
        if new_output.strip() != old_output.strip():
            answers[case] = {
                "input":value, "result": "incorrect", "your_output": new_output,
                "expected_output": old_output}
        else:
            answers[case] = {
                "result": "correct", "your_output": new_output,
                "expected_output": old_output
            }
    return answers


def get_class_name(code):
    """ TO GET CLASS NAME """
    lines = code.split("\n")
    for line in lines:
        if 'class' in line:
            class_name = line.split(" ")
            if class_name[0] == 'public':
                name = class_name[2]
            else:
                name = class_name[1]
            break
    return name.strip()
