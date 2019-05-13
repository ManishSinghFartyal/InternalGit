''' VIEWS MANAGE '''
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from nitortest.models import CandidateStatus, Question
from .service import get_id, get_test
from .service import get_question_paper, save_answer, get_answered, save_time
from .service import get_remaining_time, save_code, count_score


# Extending compilers
from . import check_code_python as cPython
from . import check_code_java as cJava
from . import check_code_node as cNode

def index(request, next_url=None):
    ''' INDEX FOR VALIDATIONS'''
    user = request.user
    if user.is_superuser:
        return render(request, 'Nitor/adminHome.html')
    return HttpResponseRedirect('/candidate/candidateHome')

def candidate_home(request):
    ''' Candidate home page'''
    user = request.user
    i_d = get_id(user)
    tests = get_test(i_d)
    return render(request, 'candidateHome.html', {'tests':tests})


def starttest(request, pid, tid):
    ''' Starts test '''
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        #If user submit a mcq answer
        request.session['testid'] = pid
        userid = get_id(user)
        starttime = timezone.localtime(timezone.now())
        save_time(starttime, userid, pid, tid)
        test_str = "/candidate/test/"+pid+"/"+tid
        request.session['currentpage'] = 1
        return HttpResponseRedirect(test_str)
    return index(request)


def test(request, pid, tid):
    ''' Test fucntions '''
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        #If user submit a mcq answer
        if 'testid' not in request.session:
            return candidate_home(request)
        userid = get_id(user)
        mcq_answered, code_answered = get_answered(userid, pid, tid)
        page = request.GET.get('page', 1)
        i = pid
        paper = get_question_paper(i)
        candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=pid)&Q(id=tid))
        candidate.attempted = True
        candidate.save()
        if request.method == 'POST':
            if request.GET.get("type") == 'mcq':
                endtime = candidate.endtime
                remanining = endtime -  timezone.localtime(timezone.now())
                time = remanining.total_seconds()
                _h, _m, _s = get_remaining_time(time)
                if request.GET.get('page') and request.POST.get("correct"):
                    ans = request.POST.get("correct")
                    save_answer(ans, userid, pid, tid)
                    page = int(request.GET.get('page'))
                else:
                    page = int(request.GET.get('page'))
                mcq_answered, code_answered = get_answered(userid, pid, tid)
                question = {'mcq':paper['mcq'], 'code':paper["coding"]}
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
                endtime = candidate.endtime
                remanining = endtime -  timezone.localtime(timezone.now())
                time = remanining.total_seconds()
                _h, _m, _s = get_remaining_time(time)
                page = int(request.GET.get('page'))
                mcq_answered, code_answered = get_answered(userid, pid, tid)
                question = {'mcq':paper['mcq'], 'code':paper["coding"]}
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
            endtime = candidate.endtime
            remanining = endtime -  timezone.localtime(timezone.now())
            page = int(request.GET.get('page', 1))
            time = remanining.total_seconds()
            _h, _m, _s = get_remaining_time(time)
            question = {'mcq':paper['mcq'], 'code':paper["coding"]}
            question_paper = {}
            for key, value in question.items():
                for k, _v in value.items():
                    question_paper[k] = _v
            _t = tuple(question_paper.items())
            _p = Paginator(_t, 1)
            request.session['currentpage'] = page
            paginate = _p.page(page)
            pages = dict(paginate)
        return render(request, 'test.html', {'pid':pid, 'tid':tid, 'paper_details':paper, \
            'paper':question_paper, 'pages':pages, 'paginator':paginate, \
            'mcq_answered':mcq_answered, 'code_answered':code_answered, \
            'hour':int(_h), 'minute':int(_m), 'second':int(_s)})
    return redirect("/login")

def savetest(request, pid, tid):
    ''' To save test '''
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        request.message = 'Successfully submitted test.'
        userid = get_id(user)
        count_score(userid, pid, tid)
        try:
            del request.session['testid']
        except KeyError:
            pass
        candidate_home(request)
    return redirect("/login")


def ajaxcall(request, pid):
    ''' AJAX FUNCTION TO RUN CODE'''
    print("manish")
    userid = get_id(request.user)
    code = request.GET['code']
    testid = request.GET['testid']    
    tid = request.GET['tid']
    language = request.GET['language']
    if language == 'python':
        json = cPython.run_code2(code, userid, pid)
    elif language == 'java':
        json = cJava.run_code2(code, userid, pid)
    elif language == 'javascript':
        json = cNode.run_code2(code, userid, pid)
    save_code(pid, code, json, userid, testid, tid)
    return JsonResponse(json)


def ex(request):
    '''EXAMPLE'''
    return render(request, 'ex.html')


def rules(request, pid, tid):
    '''TO show rules'''
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        return render(request, 'rules.html', {'pid':pid, 'tid':tid})
    return redirect("/login")

def remove_que(queid):
    '''Remove question'''
    Question.object.filter(id=queid).delete()


def home(request):
    '''HOme page'''
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return index(request)
        return render(request, 'userHome.html')
    return redirect("/login")


def user_logout(request):
    '''To logout user django logout() method'''
    logout(request)
    return redirect('/login')
