""" VIEWS MANAGE """
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout
from django.core.paginator import Paginator
from nitortest.models import CandidateStatus, Question
from .service import *

# Extending compilers
from . import check_code_python as cPython
from . import check_code_java as cJava
from . import check_code_node as cNode


def index(request, next_url=None):
    """
    INDEX FOR VALIDATIONS
    :param request: contains the details of the user who requested the URL
    :param next_url:Next url to be redirect
    :return: If user is superuser then redirect to admin home page vis a vis for candidate
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, 'Nitor/adminHome.html')
        return HttpResponseRedirect('/candidate/candidateHome')
    return redirect("/login")


def candidate_home(request):
    """
    Candidate home page
    :param request:contains the details of the user who requested the URL
    :return: Redirect to candidate home page
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, 'Nitor/adminHome.html')
        i_d = get_id(user)
        tests = get_test(i_d)
        return render(request, 'candidateHome.html', {'tests': tests})
    return redirect('/login')


def start_test(request, pid, tid):
    """
    Starts test
    :param request: contains the details of the user who requested the URL
    :param pid: Paper id
    :param tid: test id
    :return: Redirect to test_str
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        # If user submit a mcq answer
        request.session['testid'] = pid
        user_id = get_id(user)
        start_time = timezone.localtime(timezone.now())
        save_time(start_time, user_id, pid, tid)
        test_str = "/candidate/test/"+pid+"/"+tid
        request.session['currentpage'] = 1
        return HttpResponseRedirect(test_str)
    return index(request)


def test(request, pid, tid):
    """
    Starts a test and save answer, time limit
    :param request:contains the details of the user who requested the URL
    :param pid: Paper id
    :param tid: test id
    :return: To the test page after saving previous answer or login if not logged in
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        # If user submit a mcq answer
        if 'testid' not in request.session:
            return candidate_home(request)
        userid = get_id(user)
        mcq_answered, code_answered = get_answered(userid, pid, tid)
        page = request.GET.get('page', 1)
        i = pid
        paper = get_question_paper(i)
        candidate = CandidateStatus.objects.get(Q(candidate=userid) &
                                                Q(question_paper=pid) &
                                                Q(id=tid))
        candidate.attempted = True
        candidate.save()
        if request.method == 'POST':
            if request.GET.get("type") == 'mcq':
                end_time = candidate.endtime
                remaining = end_time -  timezone.localtime(timezone.now())
                time = remaining.total_seconds()
                _h, _m, _s = get_remaining_time(time)
                if request.GET.get('page') and request.POST.get("correct"):
                    ans = request.POST.get("correct")
                    save_answer(ans, userid, pid, tid)
                    page = int(request.GET.get('page'))
                else:
                    page = int(request.GET.get('page'))
                mcq_answered, code_answered = get_answered(userid, pid, tid)
                question = {'mcq': paper['mcq'], 'code': paper["coding"]}
                question_paper = {}
                for key, value in question.items():
                    for k, _v in value.items():
                        question_paper[k] = _v
                _t = tuple(question_paper.items())
                _p = Paginator(_t, 1)
                total_pages = _p.num_pages
                paginate = _p.page(page)
                if page < total_pages:
                    request.session['currentpage'] = paginate.next_page_number()
                    paginate = _p.page(request.session['currentpage'])
                    pages = dict(paginate)
                elif page == total_pages:
                    if 'currentpage' in request.session:
                        request.session['currentpage'] = paginate.previous_page_number()
                    else:
                        request.session['currentpage'] = 1
                    paginate = _p.page(page)
                    pages = dict(paginate)
                else:
                    pages = None
                    request.session['currentpage'] = 1
            elif request.GET.get("type") == 'code':
                print("Get coding question")
                end_time = candidate.endtime
                remaining = end_time - timezone.localtime(timezone.now())
                time = remaining.total_seconds()
                _h, _m, _s = get_remaining_time(time)
                page = int(request.GET.get('page'))
                mcq_answered, code_answered = get_answered(userid, pid, tid)
                question = {'mcq': paper['mcq'], 'code': paper["coding"]}
                question_paper = {}
                for key, value in question.items():
                    for k, _v in value.items():
                        question_paper[k] = _v
                _t = tuple(question_paper.items())
                _p = Paginator(_t, 1)
                total_pages = _p.num_pages
                paginate = _p.page(page)
                if page < total_pages:
                    request.session['currentpage'] = paginate.next_page_number()
                    paginate = _p.page(request.session['currentpage'])
                    pages = dict(paginate)
                elif page == total_pages:
                    try:
                        request.session['currentpage'] = paginate.previous_page_number()
                    except:
                        request.session['currentpage'] = 1
                    paginate = _p.page(page)
                    pages = dict(paginate)
                else:
                    pages = None
                    request.session['currentpage'] = 1
        else:
            end_time = candidate.endtime
            remaining = end_time - timezone.localtime(timezone.now())
            page = int(request.GET.get('page', 1))
            time = remaining.total_seconds()
            _h, _m, _s = get_remaining_time(time)
            question = {'mcq': paper['mcq'], 'code': paper["coding"]}
            question_paper = {}
            for key, value in question.items():
                for k, _v in value.items():
                    question_paper[k] = _v
            _t = tuple(question_paper.items())
            _p = Paginator(_t, 1)
            request.session['currentpage'] = page
            paginate = _p.page(page)
            pages = dict(paginate)
        return render(request, 'test.html', {'pid': pid, 'tid': tid, 'paper_details': paper,
                                             'paper': question_paper, 'pages': pages,
                                             'paginator': paginate, 'mcq_answered': mcq_answered,
                                             'code_answered': code_answered, 'hour': int(_h),
                                             'minute': int(_m), 'second': int(_s)})
    return redirect("/login")


def save_test(request, pid, tid):
    """
     To save test
    :param request:contains the details of the user who requested the URL
    :param pid: paper id
    :param tid: Test id
    :return: After final submit it saves the test and return to candidate home
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        request.message = 'Successfully submitted test.'
        user_id = get_id(user)
        count_score(user_id, pid, tid)
        try:
            del request.session['testid']
        except KeyError:
            pass
        candidate_home(request)
    return redirect("/login")


def ajax_call(request, pid):
    """
    AJAX FUNCTION TO RUN CODE
    :param request:contains the details of the user who requested the URL
    :param pid:Paper id
    :return: Compiles the code and returns the output along with the testcases
    """
    user_id = get_id(request.user)
    code = request.GET['code']
    test_id = request.GET['testid']
    tid = request.GET['tid']
    language = request.GET['language']
    if language == 'python':
        _json = cPython.run_code2(code, user_id, pid)
    elif language == 'java':
        _json = cJava.run_code2(code, user_id, pid)
    elif language == 'javascript':
        _json = cNode.run_code2(code, user_id, pid)
    save_code(pid, code, _json, user_id, test_id, tid)
    return JsonResponse(_json)


def rules(request, pid, tid):
    """
    To show rules
    :param request: contains the details of the user who requested the URL
    :param pid: Paper id
    :param tid: Test id
    :return: Rules regarding the test
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        return render(request, 'rules.html', {'pid': pid, 'tid': tid})
    return redirect("/login")


def remove_que(queid):
    """
    Remove question
    :param queid: Id of question to be removed
    :return: Nothing
    """
    Question.object.filter(id=queid).delete()


def home(request):
    """
    Address for home page
    :param request:
    :return: Home page
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        return render(request, 'userHome.html')
    return redirect("/login")


def user_logout(request):
    """
    To logout user django logout() method
    :param request:  contains the details of the user who requested the URL
    :return: clear the user session and return to the login page
    """
    logout(request)
    return redirect('/login')
