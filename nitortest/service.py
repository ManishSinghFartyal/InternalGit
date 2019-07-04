""" Provide services to user generating tasks """
import math
import string
import secrets as sc
import json
import ast
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Profile, Question, CandidateStatus, QuestionPaper


def generate_password():
    """
    To automatically generate user password using the choice method from secret
    package which combines aal the possible permutation and combination for
    ascii letters and digits and return the string with length 8
    :return: Auto generated password
    """
    keys2 = string.ascii_letters + string.digits
    pwd = ''.join(sc.choice(keys2) for i in range(8))
    print("Password = "+pwd)
    return pwd


def generate_userid(username):
    """
     To automatically generate user id using the choice method from secret
    package which combines all the possible permutation and combination for
    symbols and return the string with length 4 + the username
    :param username: Username of candidate
    :return: Auto generated user id
    """
    keys2 = '!@#$%&*()?'
    user_id = username + '_' + '' .join(sc.choice(keys2) for i in range(3))
    print('User_id   =  ', user_id)
    return user_id


def list_of_candidates():
    """
     To get all the candidates list from database
    :return: All candidates from database
    """
    candidates = {}
    try:
        all_profiles = Profile.objects.all()
    except ObjectDoesNotExist:
        return candidates
    for profile in all_profiles:
        if profile.role == 2:
            try:
                user = User.objects.get(id=profile.user_id)
                candidates[profile.userid] = {'id': user.id, 'fname': user.first_name,
                                              'lname': user.last_name, 'email': user.email,
                                              'skill': profile.skills,
                                              'education': profile.education,
                                              'experience': profile.experience,
                                              'contact': profile.contact,
                                              'department': profile.department}
            except ObjectDoesNotExist:
                continue
    return candidates


def get_candidate_profile(user_id):
    """
    Show candidate profile
    :param user_id:Candidate id for which profile to show
    :return: Candidate details
    """
    que_paper_assigned = []
    _candidate = {}
    try:
        _profile = Profile.objects.get(user_id=user_id)
        if CandidateStatus.objects.filter(candidate=user_id).count() >= 1:
            assigned = CandidateStatus.objects.filter(candidate=user_id)
            for _a in assigned:
                que_paper_assigned.append(_a.question_paper)
            c_s = 'Already Assigned'
        else:
            c_s = 'Not assigned'
        user = User.objects.get(id=user_id)
        _candidate = {'id': _profile.id, 'user_id': user_id, 'fname': user.first_name,
                      'lname': user.last_name, 'email': user.email, 'skill': _profile.skills,
                      'education': _profile.education, 'experience': _profile.experience,
                      'contact': _profile.contact, 'department': _profile.department,
                      'status': c_s, 'que_paper_assigned': que_paper_assigned}
    except ObjectDoesNotExist:
        return _candidate
    return _candidate


def create_question_object():
    """
    Create question object with string as json
    :return: question objects
    """
    que = {}
    try:
        questions = Question.objects.all()
    except ObjectDoesNotExist:
        return que

    # for options in questions if MCQ
    j_s = None
    # for test cases in question if CODING
    t_c = None
    for question in questions:
        if question.options:
            j_s = ast.literal_eval(question.options)
            j_s = json.dumps(j_s)
            j_s = json.loads(j_s)
        if question.testcases:
            t_c = ast.literal_eval(question.testcases)
            t_c = json.dumps(t_c)
            t_c = json.loads(t_c)
        desc = question.description
        length = len(desc)
        if question.title:
            pre = question.title
            post = desc
        else:
            pre = desc[:25]
            post = desc[:length]
        que[question.id] = {"qtype": question.qtype, "subject": question.subject or None,
                            "language": question.language or None, "title": question.title or None,
                            "description": question.description or None,
                            "snippet": question.snippet or None, "options": j_s,
                            "correct_option": question.correct_option or None, "testcases": t_c,
                            "level": question.level or None, "pre": pre, "post": post}
    return que


def get_categorized_questions(questions):
    """
    Function takes input mixed questions list and part them into mcq and coding test
    :param questions: Contains all the questions
    :return: mcq question as well as coding question differently
    """
    m_c_q = {}
    c_t = {}
    for question in questions:
        que_d = Question.objects.get(id=question)
        q_type = que_d.qtype
        if q_type == 'mcq':
            m_c_q[que_d.id] = {'desc': que_d.description, 'options': que_d.options,
                               'correct_option': que_d.correct_option}
        elif q_type == 'ct':
            c_t[que_d.id] = {'desc': que_d.description, 'title': que_d.title,
                             'language': que_d.language, 'snippet': que_d.snippet,
                             'testcases': que_d.testcases}
    return m_c_q, c_t


def get_all_candidates():
    """
    To get all candidates list
    :return: All candidates in a dictionary format
    """
    candidate_dict = {}
    try:
        candidates_list = Profile.objects.all()
    except ObjectDoesNotExist:
        return candidate_dict
    for candidate in candidates_list:
        if candidate.role == 2:
            candidate_dict[candidate.id] = get_candidate_profile(candidate.user_id)

    return candidate_dict


def get_question_paper():
    """
    To get all question paper details
    :return: All question paper in a dictionary format
    """
    q_paper = {}
    try:
        q_paper_db = QuestionPaper.objects.all()
        for paper in q_paper_db:
            q_paper[paper.id] = {'title': paper.title_qp, 'total_q': paper.total_question,
                                 'mcq': paper.mcq, 'coding': paper.coding,
                                 'max_time': paper.max_time}
    except ObjectDoesNotExist:
        return q_paper
    return q_paper


def get_paper(q_paper):
    """
    Function will return a particular question paper by searching for its id
    :param q_paper:Question paper id
    :return: Question paper details
    """
    paper = {}
    mcq = ast.literal_eval(q_paper.mcq)
    mcq = json.dumps(mcq)
    mcq = json.loads(mcq)
    for key, value in mcq.items():
        mcq_values = ast.literal_eval(value['options'])
        mcq_values = json.dumps(mcq_values)
        mcq_values = json.loads(mcq_values)
        mcq[key]['options'] = mcq_values
    coding = ast.literal_eval(q_paper.coding)
    coding = json.dumps(coding)
    coding = json.loads(coding)
    paper = {'title': q_paper. title_qp, 'total': q_paper.total_question, 'mcq': mcq,
             'coding': coding, 'max_time': q_paper.max_time}
    return paper


def get_candidate_status(candidate_id):
    """
    Will return candidate dictionary which contains the related status of candidate
    :param candidate_id: Id of candidate
    :return: candidate dictionary
    """
    candidate_status = {}
    try:
        status = CandidateStatus.objects.filter(candidate=candidate_id)
        for i in status:
            paper = QuestionPaper.objects.filter(id=i.question_paper)
            title = ""
            for _p in paper:
                title = _p.title_qp
            candidate = get_candidate_profile(candidate_id)
            candidate_status[i.id] = {'candidate': candidate, 'paperId': i.question_paper,
                                      'paper_title': title, 'date': i.exam_date,
                                      'attempted': i.attempted, 'score': i.score,
                                      'time_taken': i.total_time, 'mcq_correct': i.correct_mcq,
                                      'coding_correct': i.correct_ct, 'total_score': i.total_score,
                                      'total_mcq_score': i.total_mcq_score,
                                      'total_code_score': i.total_code_score}
    except ObjectDoesNotExist:
        candidate_status = {}
    return candidate_status


def get_answered(user_id, qp_id, tid):
    """
    Function will return the answered questions by searching for user_id and question_id
    :param user_id: Id of user for which answer need to find
    :param qp_id: Question id for which it wants answer
    :param tid: Test id for which answer to be search
    :return: details of candidate's attempt and his score
    """
    details = {}
    scores = {}
    candidate = CandidateStatus.objects.get(Q(candidate=user_id)
                                            & Q(question_paper=qp_id)
                                            & Q(id=tid))
    scores["score"] = math.ceil(float(candidate.score))
    scores["mcq_score"] = candidate.correct_mcq
    scores["total_mcq_score"] = candidate.total_mcq_score
    scores["code_score"] = candidate.correct_ct
    scores["total_code_score"] = candidate.total_code_score
    scores["total_score"] = candidate.total_score
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
    for key, value in code_ans.items():
        question = Question.objects.get(id=key)
        details[key] = {'type': question.qtype, 'title': question.title,
                        "description": question.description,
                        "testcases": question.testcases, "code": value['code'],
                        "cases": value['cases']}
    for key, value in mcq_ans.items():
        question = Question.objects.get(id=key)
        options = ast.literal_eval(question.options)
        options = json.dumps(options)
        options = json.loads(options)
        details[key] = {'type': question.qtype,
                        "description": question.description, "selected": value["answer"],
                        "options": options, "correct": question.correct_option}
    return details, scores


def get_scores(testid):
    """
    To score candidate's attempt
    :param testid: id of test
    :return: after assigning score to candidate returns Total score, mcq score and coding score
    """
    total = 0
    mcq = 0
    code = 0
    key = None
    question = QuestionPaper.objects.get(id=testid)
    try:
        mcqs = ast.literal_eval(question.mcq)
        mcqs = json.dumps(mcqs)
        mcqs = json.loads(mcqs)
    except ValueError:
        mcqs = {}
    try:
        codes = ast.literal_eval(question.coding)
        codes = json.dumps(codes)
        codes = json.loads(codes)
    except ValueError:
        codes = {}

    for key in mcqs:
        mcq = mcq+10

    for key in codes:
        code = code + 100
    total = mcq + code
    return total, mcq, code


def question_remove_from_paper(question_id):
    """
    Before removing the question it also
    needs to be removed from the previous question papers
    :param question_id: Id of question paper to be removed
    :return:Updated List of question paper if paper is deletd
    """
    _existed = {}
    _mcqs = {}
    existed_in = []
    all_questions = QuestionPaper.objects.all()
    for question in all_questions:
        try:
            _mcqs = ast.literal_eval(question.mcq)
            _mcqs = json.dumps(_mcqs)
            _mcqs = json.loads(_mcqs)
            for k in _mcqs:
                if question_id == k:
                    existed_in.append(question.id)
        except ValueError:
            existed_in = {}
        try:
            _codes = ast.literal_eval(question.coding)
            _codes = json.dumps(_codes)
            _codes = json.loads(_codes)
            for k in _codes:
                if question_id == k:
                    existed_in.append(question.id)
        except ValueError:
            existed_in = {}
    return existed_in


def questionpaper_remove_from_assigned(question_paper_id):
    """
    Before removing the question paper it makes
    sure that it is not assigned to any student
    :param question_paper_id: id of question paper
    :return: returns list of ids of candidate for which question paper is assigned
    """
    existed_in = []
    candidate_status = CandidateStatus.objects.all()
    for c_d in candidate_status:
        if c_d.question_paper == int(question_paper_id):
            existed_in.append(c_d.candidate)
    return existed_in


def get_all_candidate_status():
    """
    Details of all candidate
    :return: All candidates details
    """
    all_candidates_status = {}
    candidates_in_status = CandidateStatus.objects.all()
    for candidate in candidates_in_status:
        all_candidates_status[candidate.id] = get_candidate_status2(candidate.id,
                                                                    candidate.candidate,
                                                                    candidate.question_paper)
    return all_candidates_status


def get_candidate_status2(_id, candidate_id, question_id):
    """
    Will return candidate dictionary which contains the related status of candidate
    :param _id: Unique id of candidate
    :param candidate_id: Id of candidate
    :param question_id: Id of question paper assigned to him
    :return: Returns candidate's status
    """
    candidate_status = {}
    try:
        i = CandidateStatus.objects.get(Q(candidate=candidate_id) &
                                        Q(question_paper=question_id) &
                                        Q(id=_id))
        paper = QuestionPaper.objects.filter(id=i.question_paper)
        title = ""
        max_time = ""
        for _p in paper:
            title = _p.title_qp
            max_time = _p.max_time
        candidate = get_candidate_profile(candidate_id)
        candidate_status = {'test_id': _id, 'candidate': candidate, 'paperId': i.question_paper,
                            'paper_title': title, 'date': i.exam_date, 'attempted': i.attempted,
                            'score': i.score, 'time_taken': i.total_time,
                            'mcq_correct': i.correct_mcq, 'coding_correct': i.correct_ct,
                            'total_score': i.total_score, 'total_mcq_score': i.total_mcq_score,
                            'total_code_score': i.total_code_score, 'max_time': max_time}
    except ObjectDoesNotExist:
        candidate_status = {}
    return candidate_status


def get_total_candidates():
    """
    Returns number of candidates registered till date
    :return:
    """
    count = Profile.objects.all().count()
    return count


def get_total_assigned_test():
    """

    :return:
    """
    count = CandidateStatus.objects.all().count()
    return count


def get_total_attempted_test():
    """

    :return:
    """
    count = CandidateStatus.objects.filter(attempted=True).count()
    return count


def get_top_scorer():
    """

    :return:
    """
    score = 0
    top_scorer = None
    count = CandidateStatus.objects.filter(attempted=True)
    for candidate in count:
        if score < candidate.total_score:
            top_scorer = candidate
    top_scorer = {'status': top_scorer, 'profile': get_candidate_profile(top_scorer.candidate)}
    return top_scorer

