""" Provides candidates based services """
import ast
import json
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from nitortest.models import Profile, CandidateStatus, QuestionPaper, Question


def get_id(user):
    """
    get id by username
    :param user: Id of user
    :return: Get unique user id by user id
    """
    try:
        profile = Profile.objects.get(userid=user)
        i_d = profile.user_id
    except ObjectDoesNotExist:
        i_d = None
    return i_d


def get_test(candidate_id):
    """
    get tests allocated to candiadte
    :param candidate_id: Candidate ID
    :return: Tests assigned to candidate
    """
    candidate_status = {}
    try:
        status = CandidateStatus.objects.filter(candidate=candidate_id)
        for i in status:
            paper = QuestionPaper.objects.filter(id=i.question_paper)
            title = ""
            _p = None
            for _p in paper:
                title = _p.title_qp
            candidate_status[i.id] = {'paperId': i.question_paper, 'paper_title': title,
                                      'date': i.exam_date, 'attempted': i.attempted,
                                      'score': i.score, 'time_taken': i.total_time,
                                      'mcq_correct': i.correct_mcq, 'coding_correct': i.correct_ct,
                                      'max_time': _p.max_time}
    except ObjectDoesNotExist:
        candidate_status = {}
    return candidate_status


def get_question_paper(testid):
    """
    GET question paper assigned to tests id
    :param testid: test id of candidate
    :return: Question paper assigned for that test id
    """
    i = 1
    paper = {}
    try:
        q_paper = QuestionPaper.objects.get(id=testid)
    except ObjectDoesNotExist:
        paper = {}
    mcq = ast.literal_eval(q_paper.mcq)
    mcq = json.dumps(mcq)
    mcq = json.loads(mcq)
    for key, value in mcq.items():
        mcq_values = ast.literal_eval(value['options'])
        mcq_values = json.dumps(mcq_values)
        mcq_values = json.loads(mcq_values)
        mcq[key]['sr'] = i
        mcq[key]['options'] = mcq_values
        mcq[key]['type'] = "mcq"
        i = i+1
    code = {}
    coding = ast.literal_eval(q_paper.coding)
    coding = json.dumps(coding)
    coding = json.loads(coding)
    for key, value in coding.items():
        test_cases = ast.literal_eval(value['testcases'])
        test_cases = json.dumps(test_cases)
        test_cases = json.loads(test_cases)
        code[key] = {'desc': value['desc'], 'title': value['title'], 'language': value['language'],
                     'snippet': value['snippet'], "testcases": test_cases, "sr": i, "type": "code"}
        i = i+1
    paper = {'title': q_paper.title_qp, 'total': q_paper.total_question, 'mcq': mcq,
             'coding': code, 'max_time': q_paper.max_time}
    return paper


def save_answer(answer, user_id, pid, tid):
    """
     to save candidate answer into database
    :param answer: Answer of candidate
    :param user_id: Id of user
    :param pid: Paper id
    :param tid: test id
    :return: All the MCQ which have been answered
    """

    ans_split = answer.split("|")
    question = ans_split[0]
    ans = ans_split[1]
    test_id = str(pid)
    # GETTING CANDIDATE OBJECT
    candidate = CandidateStatus.objects.get(Q(candidate=user_id) &
                                            Q(question_paper=test_id) &
                                            Q(id=tid))
    # Saving MCQ answered
    try:
        mcq_ans = ast.literal_eval(candidate.mcq_ans)
        mcq_ans = json.dumps(mcq_ans)
        mcq_ans = json.loads(mcq_ans)
    except ValueError:
        mcq_ans = {}
    mcq_ans[question] = {"answer": ans}
    candidate.mcq_ans = mcq_ans
    candidate.save()
    return mcq_ans


def get_answered(user_id, pid, tid):
    """
    to get questions already answered by candidate
    :param user_id: Id of user
    :param pid: paper id
    :param tid: Test id
    :return: Already answered mcq and code
    """
    candidate = CandidateStatus.objects.get(Q(candidate=user_id) &
                                            Q(question_paper=pid) &
                                            Q(id=tid))
    try:
        mcq_ans = ast.literal_eval(candidate.mcq_ans)
        mcq_ans = json.dumps(mcq_ans)
        mcq_ans = json.loads(mcq_ans)
        code_ans = ast.literal_eval(candidate.code_ans)
        code_ans = json.dumps(code_ans)
        code_ans = json.loads(code_ans)
    except ValueError:
        mcq_ans = {}
        code_ans = {}
        get_snippet_for_code(54)
    return mcq_ans, code_ans


def get_snippet_for_code(question_id):
    print("hi")
    try:
        question = Question.objects.get(Q(id=question_id))
        print(question.snippet)
    except:
        print("Exception")
        pass



def save_time(start_time, user_id, pid, tid):
    """
    Saves the remaining time for candidate test
    :param start_time: Start time of test
    :param user_id: Id of candidate
    :param pid: Paper id
    :param tid: Test id
    :return: End time for test
    """
    candidate = CandidateStatus.objects.get(Q(candidate=user_id) &
                                            Q(question_paper=pid) &
                                            Q(id=tid))
    candidate.starttime = start_time
    paper = get_question_paper(pid)
    end_time = start_time + timezone.timedelta(minutes=paper["max_time"])
    candidate.endtime = end_time
    candidate.save()
    return end_time


def get_remaining_time(seconds):
    """
    Remaining time of candidates
    :param seconds: remaining seconds
    :return: updated remaining seconds
    """
    _h = seconds//(60*60)
    _m = (seconds-_h*60*60)//60
    _s = seconds-(_h*60*60)-(_m*60)
    return _h, _m, _s


def save_code(que_id, code, json1, user_id, test_id, tid):
    """
    Save the code of candidate
    :param que_id: Id of question which code is answered
    :param code: Code
    :param json1: Testcases for that code
    :param user_id: Id of user
    :param test_id: Id of test
    :param tid: Test id
    :return:
    """
    candidate = CandidateStatus.objects.get(Q(candidate=user_id) &
                                            Q(question_paper=test_id) &
                                            Q(id=tid))
    code_ans = {}
    cases = {}
    for key, value in json1.items():
        cases[key] = value['result']
    try:
        code_ans = ast.literal_eval(candidate.code_ans)
        code_ans = json.dumps(code_ans)
        code_ans = json.loads(code_ans)
    except ValueError:
        code_ans = {}
    code_ans[que_id] = {"code": code, "cases": cases}
    candidate.code_ans = code_ans
    candidate.save()


def count_score(user_id, pid, tid):
    """
    count score of user answers
    :param user_id: Id of user for which count the score
    :param pid: Paper id
    :param tid: Test id
    :return: Total score, MCQ score, Code test score
    """
    count = 0
    correct = 0
    total = 0
    candidate = CandidateStatus.objects.get(Q(candidate=user_id) &
                                            Q(question_paper=pid) &
                                            Q(id=tid))
    mcq_ans, code_ans = get_answered(user_id, pid, tid)
    if mcq_ans != 0:
        for key, value in mcq_ans.items():
            question = Question.objects.get(id=key)
            if value['answer'] == question.correct_option:
                candidate.correct_mcq = candidate.correct_mcq+10
    if code_ans != 0:
        for key, value in code_ans.items():
            for _k, _v in value['cases'].items():
                count += 1
                if _v == 'correct':
                    correct += 1
            total = total + (correct/count) * 100
        candidate.correct_ct = total
    candidate.score = candidate.correct_mcq + candidate.correct_ct
    candidate.save()
