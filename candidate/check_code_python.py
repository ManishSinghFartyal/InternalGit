
"""
Following function will create a output python file using file handling in python
which stores the code passed through parameters and will run this code and
return the output to be print on UI
"""

import ast
import json
import os
import subprocess
from django.conf import settings
from nitortest.models import Question
MEDIA = settings.MEDIA_ROOT


def run_code(code, user_id):
    """
        a contains code user entered in given code editor
        now this code needs to create a folder which contains the user code into its respective
        folder
    """
    hi_code = MEDIA+str(user_id)+"/"+str(user_id)+'.py'
    _a = code
    os.makedirs(os.path.dirname(hi_code), exist_ok=True)
    with open(hi_code, "w") as _f:
        _f.write(_a)
    _f.close()
    command = 'python '+hi_code
    try:
        code_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as c_l:
        code_output = c_l.output
    new_output = code_output.decode()
    return new_output


def fetch_test_cases(que_id):
    """ fetched testcases """
    que = Question.objects.get(id=que_id)
    if que.qtype == "ct":
        test_cases = ast.literal_eval(que.testcases)
        test_cases = json.dumps(test_cases)
        test_cases = json.loads(test_cases)
    return test_cases


def get_output(test_case, code, user_id, que_id):
    """TO get output"""
    test_case = str.encode(test_case)
    hi_code = MEDIA+str(user_id)+"/"+str(que_id)+"-"+str(user_id)+'.py'
    _a = code
    os.makedirs(os.path.dirname(hi_code), exist_ok=True)
    with open(hi_code, "w") as _f:
        _f.write(_a)
    _f.close()
    command = 'python '+hi_code
    try:
        code_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True,
                                              input=test_case)
    except subprocess.CalledProcessError as c_l:
        code_output = c_l.output
    new_output = code_output.decode()
    return new_output


def run_code2(code, user_id, que_id):
    """
        a contains code user entered in given code editor
        now this code needs to create a folder which contains the user code into its respective
        folder.
    """
    test_cases = fetch_test_cases(que_id)
    answers = {}
    for case in test_cases:
        value = test_cases[case]['testcase']
        old_output = test_cases[case]['output']
        new_output = get_output(value, code, user_id, que_id)
        if new_output.strip() != old_output.strip():
            answers[case] = {"input": value, "result": "incorrect", "your_output": new_output,
                             "expected_output": old_output}
        else:
            answers[case] = {"result": "correct", "your_output": new_output,
                             "expected_output": old_output}
    return answers
