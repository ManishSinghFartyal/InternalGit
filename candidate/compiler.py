
"""
Following function will create a output python file using file handling in python
which stores the code passed through parameters and will run this code and
return the output to be print on UI
"""

import ast
import json
from subprocess import STDOUT
import os
import subprocess
from django.conf import settings
from nitortest.models import Question
from .service import *
MEDIA = settings.MEDIA_ROOT


class RunCode:
    """
    Class will create the environment to handle the compiler flow
    """

    def __init__(self, user_id, code, question_paper_id, candidate_status_id, question_id, language):
        self.user_id = user_id
        self.code = code
        self.question_paper_id = question_paper_id
        self.candidate_status_id = candidate_status_id
        self.language = language
        self.question_id = question_id
        # print('USER', self.user_id, self.code, self.tid)
        self.test_cases = self.fetch_test_cases(question_id)

    def fetch_test_cases(self, question_id):
        """
        Fetches question related test cases for codeing test
        :param question_id: ID of particular question
        :return: Test cases
        """
        test_cases = {}
        que = Question.objects.get(id=question_id)
        if que.qtype == "ct":
            test_cases = ast.literal_eval(que.testcases)
            test_cases = json.dumps(test_cases)
            test_cases = json.loads(test_cases)
        return test_cases

    def execute_code(self):
        mediator = self.get_object(self.language)
        output = mediator.run_code(self.question_id, self.code, self.user_id, self.test_cases)
        return output

    def get_object(self, language):
        if language == 'python':
            mediator = PythonInterpreter('.py')
        elif language == 'java':
            mediator = JavaCompiler('.java')
        elif language == 'javascript':
            mediator = NodeInterpreter('.js')
        return mediator


class PythonInterpreter(object):
    extension = None

    def __init__(self, extension):
        self.extension = extension

    def run_code(self, question_id, code, user_id, test_cases):
        processes = CommonProcesses()
        code_directory = MEDIA+str(user_id)+"/"+str(question_id)+self.extension
        command = 'python '+code_directory
        processes.save_code(code, code_directory)
        answers = processes.get_output_of_each_test_case(command, test_cases)
        return answers


class NodeInterpreter(object):
    extension = None

    def __init__(self, extension):
        NodeInterpreter.extension = extension

    def run_code(self, question_id, code, user_id, test_cases):
        processes = CommonProcesses()
        code_directory = MEDIA + str(user_id) + "/" + str(question_id) + self.extension
        command = 'node '+code_directory
        processes.save_code(code, code_directory)
        answers = processes.get_output_of_each_test_case(command, test_cases)
        return answers


class JavaCompiler(object):
    """
    Java compiler + java run command
    """
    extension = None

    def __init__(self, extension):
        JavaCompiler.extension = extension

    def run_code(self, question_id, code, user_id, test_cases):
        """

        :param question_id:
        :param code:
        :param user_id:
        :param test_cases:
        :return:
        """
        class_name = self.get_java_class_name(code)
        compile_code_directory = MEDIA + str(user_id) + "/" + class_name + self.extension
        code_directory = "-cp " + MEDIA + str(user_id) + " " + class_name
        processes = CommonProcesses()
        compile_command = 'javac ' + compile_code_directory
        run_command = 'java ' + code_directory
        processes.save_code(code, compile_code_directory)
        answers = processes.get_output_of_code(compile_command)
        if not answers:
            answers = processes.get_output_of_each_test_case(run_command, test_cases)
        return answers

    def get_java_class_name(self, code):
        """
        TO GET CLASS NAME WRITTEN INSIDE THE JAVA CODE
        :param code: Code written by user
        :return: class name of java using its code
        """
        name = None
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


class CommonProcesses(object):
    """
    Contains all the common processes which are used by compilers
    """
    def save_code(self, code, code_directory):
        """

        :param code:
        :param code_directory:
        :return:
        """
        os.makedirs(os.path.dirname(code_directory), exist_ok=True)
        with open(code_directory, "w") as _f:
            _f.write(code)
        _f.close()

    def get_output_of_code(self, command, test_case=None):
        if test_case:
            test_case = str.encode(test_case)
        try:
            code_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True,
                                                  input=test_case)
        except subprocess.CalledProcessError as c_l:
            code_output = c_l.output
        new_output = code_output.decode()
        return new_output

    def get_output_of_each_test_case(self, command, test_cases):
        answers = {}
        for case in test_cases:
            test_case = test_cases[case]['testcase']
            old_output = test_cases[case]['output']
            new_output = self.get_output_of_code(command, test_case)
            if new_output.strip() != old_output.strip():
                answers[case] = {"input": test_case, "result": "incorrect", "your_output": new_output,
                                 "expected_output": old_output}
            else:
                answers[case] = {"result": "correct", "your_output": new_output,
                                 "expected_output": old_output}
        return answers



