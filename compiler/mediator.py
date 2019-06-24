from nitortest.models import Question
import ast
import json
from . import PythonCompiler, JavaCompiler, NodeCompiler


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
            mediator = PythonCompiler.PythonInterpreter('.py')
        elif language == 'java':
            mediator = JavaCompiler.JavaCompiler('.java')
        elif language == 'javascript':
            mediator = NodeCompiler.NodeInterpreter('.js')
        return mediator