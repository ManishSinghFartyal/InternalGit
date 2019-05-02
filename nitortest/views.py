'''
Nitor test module handles the activity of admin in the project.
'''
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login as auth_login, logout
from .forms import createQuestionPaper
from .forms import UserRegisterForm, UserLoginForm, addCodingTestForm, addMcqForm
from .models import Profile, Question, QuestionPaper, CandidateStatus
from .service import  get_candidate_status, get_answered, get_scores, create_question_object
from .service import list_of_candidates, get_candidate_profile, get_categorized_questions
from .service import  get_all_candidates, get_question_paper, get_paper, question_remove_from_paper
from .service import questionpaper_remove_from_assigned


@csrf_protect
@login_required
def index(request, next_url=None):
    ''' Handles the redirection of user as per their roles '''
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, 'Nitor/adminHome.html')
        return HttpResponseRedirect('/candidate')
    return redirect('/login')

def success(request):
    """ To send user response after Candidate successfully saved """
    return render(request, 'Nitor/saveCandidate.html')

def is_admin(userid):
    ''' To check if user has admin rights '''
    to_return = False
    try:
        user_profile = Profile.objects.get(userid=userid)
        role = user_profile.role
        if role == 1:
            to_return = True
        return to_return
    except Exception:
        return False

def add_user(request):
    """To register new user"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return success_message(request, "Candidate saved successfully")
            return render(request, 'Nitor/register.html', {'form':form})
        form = UserRegisterForm()
        return render(request, 'Nitor/register.html', {'form':form})
    return index(request)

def login(request):
    """ To check user login    """
    user = request.user
    if user.is_authenticated:
        return index(request)
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            auth_login(request, user)
            return index(request, next_url)
        context = {'form':form}
    form = UserLoginForm()
    context = {'form':form}
    return render(request, 'Nitor/loginNew.html', context)

def user_logout(request):
    ''' To logout user django logout() method '''
    logout(request)
    return redirect('/login')

def list_candidates(request):
    ''' To list out all the candidates and their details '''
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            candidates = list_of_candidates()
            return render(request, 'Nitor/candidateList.html', {'candidates':candidates})
        return index(request)
        #return render(request, 'to candidate home page')
    return render(request, '/login')

def candidate_profile(request, userid):
    """ To view candidate profile using id """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            profile = get_candidate_profile(userid)
            return show_profile(request, profile)
    return index(request)

def show_profile(request, profile):
    """ Code to show profile of a user """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'Nitor/candidateProfile.html', {'candidate':profile})
    return index(request)

def remove_candidate(request, userid):
    """ Removing candidate by using id """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                Profile.objects.get(user_id=userid).delete()
                User.objects.get(id=userid).delete()
                CandidateStatus.objects.filter(candidate=userid).delete()
                return HttpResponseRedirect('/listCandidate')
            except:
                return HttpResponseRedirect('/listCandidate')
    return index(request)

def save_candidate(request):
    """save candidate method"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'Nitor/saveCandidate.html')
    return index(request)

def show_add_code(request):
    """ Add new coding questions """
    form1 = addMcqForm()
    form2 = addCodingTestForm()
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            if request.method == 'POST':
                qtype = request.POST.get('qtype')
                #code to add coding test in database
                if qtype == 'ct':
                    form2 = addCodingTestForm(request.POST, \
                     {'extra':int(request.POST.get('total_testcases_count'))})
                    if form2.is_valid():
                        test_cases = {}
                        title = request.POST.get('title')
                        level = request.POST.get('level')
                        description = request.POST.get('description')
                        snippet = request.POST.get('snippet')
                        language = request.POST.get('language')
                        total_test_cases = int(request.POST.get('total_testcases_count'))
                        if total_test_cases:
                            total_test_cases += 1
                            for index in range(1, total_test_cases):
                                case = 'case'+str(index)
                                input_str = 'input_'+str(index)
                                output_str = 'output_'+str(index)
                                test_cases[case] = {'testcase':request.POST.get(input_str), \
                                 'output':request.POST.get(output_str)}
                        testcases = test_cases
                        question = Question(qtype=qtype, language=language, \
                         title=title, level=level, description=description, snippet=snippet,\
                          testcases=testcases)
                        question.save()
                        return success_message(request, "One coding question saved successfully.")

                #code to add mcq in database
                elif qtype == 'mcq':
                    form1 = addMcqForm(request.POST,\
                     {'extra':int(request.POST.get('total_options'))})
                    if form1.is_valid():
                        test_options = {}
                        question = request.POST.get('question')
                        total_options = int(request.POST.get('total_options'))
                        if total_options:
                            total_options += 1
                            for index in range(1, total_options):
                                option = str(index)
                                option_val = "option_"+str(index)
                                test_options[option] = request.POST.get(option_val)
                        options = test_options
                        correct_option = request.POST.get('correct_option')
                        subject = request.POST.get('subject')
                        question = Question(qtype=qtype, subject=subject,\
                         description=question, options=options, correct_option=correct_option)
                        question.save()
                        return success_message(request,\
                         "One multiple choice question saved successfully.")
                    return render(request, 'Nitor/addCodingQuiz.html', {'form1':form1,\
                         'form2':form2, 'current':'mcq'})
            form1 = addMcqForm()
            form2 = addCodingTestForm()
            context = {'form1':form1, 'form2':form2, 'current':None}
            return render(request, 'Nitor/addCodingQuiz.html', context)
    return index(request)

def success_que(request):
    """ To show the success message after adding a question"""
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, 'Nitor/quesuccess_message.html')
    return index(request)

def get_questions(request):
    """ fetching all the questions from database to manage in interpolation"""
    questions = Question.objects.values()
    return JsonResponse({'questions': list(questions)})

def create_que_paper(request):
    """# To create question paper"""

    # fetching all the questions from database to manage in interpolation
    user = request.user
    questions = Question.objects.all()
    que = create_question_object()
    form = createQuestionPaper()
    context = {'form':form, 'questions':que}
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            if request.method == 'POST':
                form = createQuestionPaper(request.POST)
                total = int(request.POST.get('totalquestions'))
                if total == 0:
                    messages.error(request, '**Questions not selected.')
                    return render(request, 'Nitor/createQuestion.html', context)
                title = request.POST.get('title_qp')
                if not title:
                    messages.error(request, '**Please enter title.')
                    return render(request, 'Nitor/createQuestion.html', context)
                questions = request.POST.getlist('questionid')
                _mcq, _ct = get_categorized_questions(questions)
                max_time = int(request.POST.get('max_time'))
                if max_time == 0:
                    messages.error(request, '**Enter max time')
                    return render(request, 'Nitor/createQuestion.html', context)
                q_p = QuestionPaper(title_qp=title, total_question=total,\
                 mcq=_mcq, coding=_ct, max_time=max_time)
                q_p.save()
                return success_message(request, "Question paper created successfully.")
            return render(request, 'Nitor/createQuestion.html', context)
    return index(request)

def success_message(request, message):
    """# to show success message on completing some event."""
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, 'Nitor/successMessage.html', {'message':message})
    return index(request)

def assign_test(request):
    """ Code to assign the test for canidates."""
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            context = {'candidates':get_all_candidates(), 'papers':QuestionPaper.objects.all()}
            if request.method == 'POST':
                ids = request.POST.getlist('candidate_id')
                if not ids:
                    messages.error(request, '**No candidate selected.')
                else:
                    for i in ids:
                        test_str = i+"-paper"
                        date_str = i+"-date"
                        assigned_test = request.POST.get(test_str)
                        total_score, mcq_score, code_score = get_scores(assigned_test)
                        assigned_date = request.POST.get(date_str)
                        mcq_ans = {}
                        code_ans = {}
                        if assigned_date == "" or assigned_test is None:
                            messages.error(request, ' Either date of test or exam not selected.')
                            return render(request, 'Nitor/assignTest.html', context)
                        _c = CandidateStatus(candidate=i, exam_date=assigned_date,\
                         question_paper=assigned_test, mcq_ans=mcq_ans,\
                          code_ans=code_ans, total_score=total_score, total_code_score=code_score,\
                           total_mcq_score=mcq_score)
                        _c.save()
                    return success_message(request, "Successfully asssigned")
            return render(request, 'Nitor/assignTest.html', context)
        return index(request)

def question_papers(request, message=None):
    """# Code to show question papers"""
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            q_p = get_question_paper()
            return render(request, 'Nitor/listquestionPaper.html', {'paper':q_p, \
                'message':message})
    return index(request)

def fetch_question_paper(request, questionid):
    """#To fetch details of created question paper"""
    _id = int(questionid)
    q_paper = QuestionPaper.objects.get(id=questionid)
    paper = get_paper(q_paper)
    return render(request, 'Nitor/showQuestionPaper.html', {'paper':paper, 'id':_id})

def candidate_status(request, candidateid):
    """#To show candidate status"""
    _id = int(candidateid)
    cst = get_candidate_status(_id)
    return render(request, 'Nitor/candidateStatus1.html', {'status':cst, 'cid':candidateid})

def rem_candidate_status(request, cid, pid):
    """#To remove Assigned test of candidate"""
    CandidateStatus.objects.get(candidate=cid, question_paper=pid).delete()
    url = "/candidatestatus/"+cid
    return HttpResponseRedirect(url)

def remove_question_paper(request, pid):
    """ To remove question paper """    
    existed_in = questionpaper_remove_from_assigned(pid)
    if not existed_in:
        QuestionPaper.objects.get(id=pid).delete()
        message = ""
    else:
        message = "Question paper is already assigned to some candidates cannot be deleted."
    return question_papers(request, message)

def show_score(request, cid, pid):
    """ To show selected candidate score of his/her attempted assigned exam """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            details, scores = get_answered(cid, pid)
            return render(request, 'Nitor/answerSheet.html', {'scores':scores, 'details':details})
    return index(request)

def list_questions(request):
    """ Function to list all the available questions in databse """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            questions = create_question_object()
            return render(request, 'Nitor/questions.html', {'questions' : questions})
    return index(request)

def remove_question(request, queid):
    """ Function to remove question from database """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            existed_in = question_remove_from_paper(queid)
            if not existed_in:
                #Question.objects.filter(id=queid).delete()
                message = ""
            else:
                message = "Question existed in papers cannot be deleted,\
                    first delete the paper."
            questions = create_question_object()
            return render(request, 'Nitor/questions.html', {'questions' : \
                questions, 'message' : message})
    return index(request)
