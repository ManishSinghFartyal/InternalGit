''' Provides candidates based services '''
import ast
import json
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from nitortest.models import Profile, CandidateStatus, QuestionPaper, Question


def get_id(user):
    ''' get id by username '''
    try:
        profile = Profile.objects.get(userid=user)
        i_d = profile.user_id
    except ObjectDoesNotExist:
        i_d = None
    return i_d

def get_test(candidate_id):
    ''' get tests allocated to candiadte '''
    candidate_status = {}
    try:
        status = CandidateStatus.objects.filter(candidate=candidate_id)
        for i in status:
            paper = QuestionPaper.objects.filter(id=i.question_paper)
            title = ""
            _p = None
            for _p in paper:
                title = _p.title_qp
            candidate_status[i.id] = {'paperId':i.question_paper,\
            'paper_title':title, 'date':i.exam_date, 'attempted':i.attempted, 'score':i.score,\
            'time_taken':i.total_time, 'mcq_correct':i.correct_mcq,\
            'coding_correct':i.correct_ct, 'max_time':_p.max_time}
    except ObjectDoesNotExist:
        candidate_status = {}
    return candidate_status

def get_question_paper(testid):
    ''' GET question paper assigned to tests id '''
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
        mcqvalues = ast.literal_eval(value['options'])
        mcqvalues = json.dumps(mcqvalues)
        mcqvalues = json.loads(mcqvalues)
        mcq[key]['sr'] = i
        mcq[key]['options'] = mcqvalues
        mcq[key]['type'] = "mcq"
        i = i+1
    code = {}
    coding = ast.literal_eval(q_paper.coding)
    coding = json.dumps(coding)
    coding = json.loads(coding)
    for key, value in coding.items():
        testcases = ast.literal_eval(value['testcases'])
        testcases = json.dumps(testcases)
        testcases = json.loads(testcases)
        code[key] = {'desc':value['desc'], 'title':value['title'], \
        'language':value['language'], 'snippet':value['snippet'], "testcases":testcases, \
        "sr":i, "type":"code"}
        i = i+1
    paper = {'title':q_paper.title_qp, 'total':q_paper.total_question, \
    'mcq':mcq, 'coding':code, 'max_time':q_paper.max_time}
    return paper

def save_answer(answer, userid, pid, tid):
    ''' to save candidate answer into dATAbase '''
    ans_split = answer.split("|")
    question = ans_split[0]
    ans = ans_split[1]
    testid = str(pid)
    #GETTING CANDIDATE OBJECT
    candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=testid)&Q(id=tid))
    #Saving MCQ answered
    try:
        mcq_ans = ast.literal_eval(candidate.mcq_ans)
        mcq_ans = json.dumps(mcq_ans)
        mcq_ans = json.loads(mcq_ans)
    except ValueError:
        mcq_ans = {}
    mcq_ans[question] = {"answer":ans}
    candidate.mcq_ans = mcq_ans
    candidate.save()
    return mcq_ans

def get_answered(userid, pid, tid):
    ''' to get questions already answered by candidate '''
    candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=pid)&Q(id=tid))
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
    return mcq_ans, code_ans


def save_time(starttime, userid, pid, tid):
    '''  candidates times'''
    candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=pid)&Q(id=tid))
    candidate.starttime = starttime
    paper = get_question_paper(pid)
    endtime = starttime + timezone.timedelta(minutes=paper["max_time"])
    candidate.endtime = endtime
    candidate.save()
    return endtime


def get_remaining_time(seconds):
    '''Remaining time of candidates'''
    _h = seconds//(60*60)
    _m = (seconds-_h*60*60)//60
    _s = seconds-(_h*60*60)-(_m*60)
    return _h, _m, _s


def save_code(queid, code, json1, userid, testid, tid):
    '''Save code'''
    candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=testid)&Q(id=tid))
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
    code_ans[queid] = {"code":code, "cases":cases}
    candidate.code_ans = code_ans
    candidate.save()


def count_score(userid, pid, tid):
    '''  count score  '''
    count = 0
    correct = 0
    total = 0
    candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=pid)&Q(id=tid))
    mcq_ans, code_ans = get_answered(userid, pid, tid)
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
