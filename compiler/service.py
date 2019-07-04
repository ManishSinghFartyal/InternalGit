import os
from subprocess import STDOUT
import subprocess


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

    def get_output_of_code(self, command, test_case=None, std_output=None):        
        if test_case:
            test_case = str.encode(test_case)
        print(std_output)
        try:
            code_output = subprocess.check_output(command, stderr=std_output, shell=True,
                                                  input=test_case)
        except subprocess.CalledProcessError as c_l:
            code_output = c_l.output
        new_output = code_output.decode()
        return new_output

    def get_output_of_each_test_case(self, command, test_cases, std_output=None):
        answers = {}
        for case in test_cases:
            test_case = test_cases[case]['testcase']
            old_output = test_cases[case]['output']
            new_output = self.get_output_of_code(command, test_case, std_output)
            print("Output : ", new_output)
            if new_output.strip() != old_output.strip():
                answers[case] = {"input": test_case, "result": "incorrect", "your_output": new_output,
                                 "expected_output": old_output}
            else:
                answers[case] = {"result": "correct", "your_output": new_output,
                                 "expected_output": old_output}
        return answers



