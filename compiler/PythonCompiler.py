from . import service
from django.conf import settings
MEDIA = settings.MEDIA_ROOT


class PythonInterpreter(object):
    extension = None

    def __init__(self, extension):
        self.extension = extension

    def run_code(self, question_id, code, user_id, test_cases):
        processes = service.CommonProcesses()
        code_directory = MEDIA+str(user_id)+"/"+str(question_id)+self.extension
        command = 'python '+code_directory
        processes.save_code(code, code_directory)
        answers = processes.get_output_of_each_test_case(command, test_cases)
        return answers
