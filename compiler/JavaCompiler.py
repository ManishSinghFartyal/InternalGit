from . import service
from django.conf import settings
MEDIA = settings.MEDIA_ROOT


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
        processes = service.CommonProcesses()
        compile_command = 'javac ' + compile_code_directory
        run_command = 'java ' + code_directory
        processes.save_code(code, compile_code_directory)
        # answers = processes.get_output_of_code(compile_command)
        answers = processes.get_output_of_each_test_case(compile_command, test_cases)
        error = True
        for key, value in answers.items():
            if answers[key]['your_output'] != "":
                error = False
        if error:
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

