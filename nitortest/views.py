"""
Nitor test module handles the activity of admin in the project.
"""
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login as auth_login, logout
from .forms import CreateQuestionPaper
from .forms import UserRegisterForm, UserLoginForm, AddCodingTestForm, AddMcqForm
from .service import *


@csrf_protect
@login_required
def index(request, next_url=None):
    """
     index : Handles the redirection of user as per their roles
    :param request: contains the details of the user who requested the URL
    :param next_url: where to fetch the user after confirmation
    :return: returning the user tp its respective URL
    """
    print(next_url)
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            if not next_url:
                next_url = '/adminHome'
            return HttpResponseRedirect(next_url)
            # return render(request, next_url)
        return HttpResponseRedirect('/candidate')
    return redirect('/login')


def admin_home(request):
    """
     Admin home redirection
    :param request: contains the details of the user who requested the URL
    :return: returning the user tp its respective URL
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, 'Nitor/adminHome.html', {'home': True})
        return HttpResponseRedirect('/candidate')
    return redirect('/login')


def is_admin(user_id):
    """
    is_admin :  To check if user has admin rights
    :param user_id: cotains the unique id of user
    :return: boolean value( is user is admin or not)
    """
    to_return = False
    try:
        user_profile = Profile.objects.get(userid=user_id)
        role = user_profile.role
        if role == 1:
            to_return = True
        return to_return
    except ObjectDoesNotExist:
        return False


def add_user(request):
    """
    add_user :  To register new user
    :param request: contains the details of the user who requested the URL
    :return: if user is admin then redirects to registration page if not then to index
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return success_message(request, "Candidate saved successfully")
            return render(request, 'Nitor/register.html', {'form': form})
        form = UserRegisterForm()
        return render(request, 'Nitor/register.html', {'form': form})
    return index(request)


def login(request):
    """
    login : To check user login
    :param request: contains the details of the user who requested the URL
    :return: if user is already logged in then return to the index and if not then return
    to the login page
    """
    user = request.user
    if user.is_authenticated:
        return index(request)
    next_url = request.GET.get('next')
    form = UserLoginForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            i = auth_login(request, user)
            return index(request, next_url)
        context = {'form': form}
    return render(request, 'Nitor/loginNew.html', context)


def user_logout(request):
    """
     To logout user django logout() method
    :param request: contains the details of the user who requested the URL
    :return: clears all the session and returns to login page
    """
    logout(request)
    return redirect('/login')


def list_candidates(request):
    """
    To list out all the candidates and their details
    :param request:  contains the details of the user who requested the URL
    :return: if user is admin then to canidate list page otherwise to index
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            candidates = list_of_candidates()
            return render(request, 'Nitor/candidateList.html', {'candidates': candidates})
        return index(request)
    return index(request)


def candidate_profile(request, user_id):
    """
    To view candidate profile using id
    :param request:  contains the details of the user who requested the URL
    :param user_id: user_id for which profile needs to be create
    :return: If user is authenticated Candidate profile else index
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            profile = get_candidate_profile(user_id)
            return show_profile(request, profile)
    return index(request)


def show_profile(request, profile):
    """
    Code to show profile of a user
    :param request: contains the details of the user who requested the URL
    :param profile: contains candidate data
    :return: candidate profile
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            print(profile)
            return render(request, 'Nitor/candidateProfile.html', {'candidate': profile})
    return index(request)


def remove_candidate(request, user_id):
    """
    Removing candidate by using id
    :param request: contains the details of the user who requested the URL
    :param user_id: user_id to be removed
    :return: after deleting the condidate it will redirect to candidate list page
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                Profile.objects.get(user_id=user_id).delete()
                User.objects.get(id=user_id).delete()
                CandidateStatus.objects.filter(candidate=user_id).delete()
                return HttpResponseRedirect('/listCandidate')
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/listCandidate')
    return index(request)


def save_candidate(request):
    """
    save candidate method
    :param request:  contains the details of the user who requested the URL
    :return: return to save candidate page or index
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'Nitor/saveCandidate.html')
    return index(request)


def show_add_question(request):
    """
    Function provides facility to add new question either MCQ or code tests
    :param request: contains the details of the user who requested the URL
    :return: after saving the question it will redirect to success message page or index
    """
    form1 = AddMcqForm()
    form2 = AddCodingTestForm()
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            if request.method == 'POST':
                qtype = request.POST.get('qtype')
                # code to add coding test in database
                if qtype == 'ct':
                    form2 = AddCodingTestForm(request.POST,
                                              {'extra': int(request.POST.get('total_testcases_count'))
                                               })
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
                            for index_range in range(1, total_test_cases):
                                case = 'case'+str(index_range)
                                input_str = 'input_'+str(index_range)
                                output_str = 'output_'+str(index_range)
                                test_cases[case] = {'testcase': request.POST.get(input_str),
                                                    'output': request.POST.get(output_str)}
                        testcases = test_cases
                        question = Question(qtype=qtype, language=language,
                                            title=title, level=level, description=description,
                                            snippet=snippet, testcases=testcases)
                        question.save()
                        return success_message(request, "One coding question saved successfully.")

                # code to add mcq in database
                elif qtype == 'mcq':
                    form1 = AddMcqForm(request.POST,
                                       {'extra': int(request.POST.get('total_options'))})
                    if form1.is_valid():
                        test_options = {}
                        question = request.POST.get('question')
                        total_options = int(request.POST.get('total_options'))
                        if total_options:
                            total_options += 1
                            for index_range in range(1, total_options):
                                option = str(index_range)
                                option_val = "option_"+str(index_range)
                                test_options[option] = request.POST.get(option_val)
                        options = test_options
                        correct_option = request.POST.get('correct_option')
                        subject = request.POST.get('subject')
                        question = Question(qtype=qtype, subject=subject,
                                            description=question, options=options,
                                            correct_option=correct_option)
                        question.save()
                        return success_message(request,
                                               "One multiple choice question saved successfully.")

            form1 = AddMcqForm()
            form2 = AddCodingTestForm()
            context = {'form1': form1, 'form2': form2, 'current': None}
            return render(request, 'Nitor/addNewQuestion.html', context)
    return index(request)


def success_que(request):
    """
     To show the success message after adding a question
    :param request: contains the details of the user who requested the URL
    :return: return the success message after saving question
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, 'Nitor/quesuccess_message.html')
    return index(request)


def get_questions(request):
    """
    Fetching all the questions from database to manage in interpolation
    :param request: contains the details of the user who requested the URL
    :return: returns all the question from database as json reponse
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            questions = Question.objects.values()
            return JsonResponse({'questions': list(questions)})
    return index(request)


def create_que_paper(request):
    """
    To create question paper
    :param request: contains the details of the user who requested the URL
    :return: returns to create question paper page or index
    """
    # fetching all the questions from database to manage in interpolation
    user = request.user
    questions = Question.objects.all()
    que = create_question_object()
    form = CreateQuestionPaper()
    context = {'form': form, 'questions': que}
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            if request.method == 'POST':
                form = CreateQuestionPaper(request.POST)
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
                q_p = QuestionPaper(title_qp=title, total_question=total,
                                    mcq=_mcq, coding=_ct, max_time=max_time)
                q_p.save()
                return success_message(request, "Question paper created successfully.")
            return render(request, 'Nitor/createQuestion.html', context)
    return index(request)


def success_message(request, message):
    """
    to show success message on completing some event.
    :param request:  contains the details of the user who requested the URL
    :param message: contains message to show in success page
    :return: redirects to success page
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, 'Nitor/successMessage.html', {'message': message})
    return index(request)


def assign_test(request):
    """
    Code to assign the test for candidates.
    :param request: contains the details of the user who requested the URL
    :return: redirects to page which is used to assign test to candidate
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            context = {'candidates': get_all_candidates(), 'papers': QuestionPaper.objects.all()}
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
                        _c = CandidateStatus(candidate=i, exam_date=assigned_date,
                                             question_paper=assigned_test, mcq_ans=mcq_ans,
                                             code_ans=code_ans, total_score=total_score,
                                             total_code_score=code_score,
                                             total_mcq_score=mcq_score)
                        _c.save()
                    return success_message(request, "Successfully asssigned")
            return render(request, 'Nitor/assignTestToCandidate.html', context)
        return index(request)


def question_papers(request, message=""):
    """
    Code to show question papers
    :param request: contains the details of the user who requested the URL
    :param message: message contains the details of question paper
    :return: List of question paper
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            q_p = get_question_paper()
            return render(request, 'Nitor/listquestionPaper.html', {'paper': q_p,
                                                                    'message': message})
    return index(request)


def fetch_question_paper(request, question_id):
    """
    To fetch details of created question paper
    :param request: contains the details of the user who requested the URL
    :param question_id: id of question paper which details need to be fetch
    :return: redirects to page which shows the particular question paper
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            _id = int(question_id)
            q_paper = QuestionPaper.objects.get(id=question_id)
            paper = get_paper(q_paper)
            return render(request, 'Nitor/showQuestionPaper.html', {'paper': paper, 'id': _id})
    return index(request)


def candidate_status(request, candidate_id):
    """
    To show candidate status
    :param request: contains the details of the user who requested the URL
    :param candidate_id: id of candidate whose status to be show
    :return: Redirect to page whose status to be show
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            _id = int(candidate_id)
            cst = get_candidate_status(_id)
            return render(request, 'Nitor/candidateStatus1.html', {'status': cst, 'cid': candidate_id})
    return index(request)


def rem_candidate_status(request, cid, pid, tid):
    """
    To remove Assigned test of candidate
    :param request:contains the details of the user who requested the URL
    :param cid: candidate id
    :param pid: paper id
    :param tid: test id
    :return: To assigned page after removing assigned page
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            CandidateStatus.objects.get(candidate=cid, question_paper=pid, id=tid).delete()
            url = "/candidatestatus/" + cid
            return HttpResponseRedirect('/assignTest/name="ALL"')
    return index(request)


def remove_question_paper(request, pid):
    """
    To remove question paper
    :param request:contains the details of the user who requested the URL
    :param pid:Question paper id
    :return:
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            existed_in = questionpaper_remove_from_assigned(pid)
            if not existed_in:
                QuestionPaper.objects.get(id=pid).delete()
                message = ""
            else:
                message = "Question paper is already assigned to some candidates cannot be deleted."
            return question_papers(request, message)
    return index(request)


def show_score(request, cid, pid,tid):
    """
    To show selected candidate score of his/her attempted assigned exam
    :param request: contains the details of the user who requested the URL
    :param cid: Candidate id
    :param pid: paper id
    :param tid: test id
    :return:
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            details, scores = get_answered(cid, pid, tid)
            return render(request, 'Nitor/answerSheet.html', {'scores': scores, 'details': details})
    return index(request)


def list_questions(request):
    """
    Function to list all the available questions in database
    :param request: contains the details of the user who requested the URL
    :return: List of questions which are available in database
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            questions = create_question_object()
            return render(request, 'Nitor/questions.html', {'questions': questions})
    return index(request)


def remove_question(request, que_id):
    """
    Function to remove question from database
    :param request: contains the details of the user who requested the URL
    :param que_id: Id of question to be remove
    :return: After deleting the question returns to questions list page
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            existed_in = question_remove_from_paper(que_id)
            if not existed_in:
                Question.objects.get(id=que_id).delete()
                message = ""
            else:
                message = "Question existed in papers cannot be deleted,\
                    first delete the paper."
            questions = create_question_object()
            return render(request, 'Nitor/questions.html', {'questions': questions,
                                                            'message': message})
    return index(request)


def assign_test2(request, name="ALL"):
    """
    Code to assign the test for candidates.
    :param request:contains the details of the user who requested the URL
    :param name:Contains the type of question to show
    :return: After assigning the test it wil return to the updated list of candidate assigned page
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            all_candidate_status = get_all_candidate_status()
            context = {'candidates': get_all_candidates(), 'papers': QuestionPaper.objects.all(),
                       "all_candidate_status": all_candidate_status}
            if request.method == 'POST':
                ids = request.POST.get('candidate')                
                assigned_test = request.POST.get("paper")
                total_score, mcq_score, code_score = get_scores(assigned_test)
                assigned_date = request.POST.get("date_str")
                mcq_ans = {}
                code_ans = {}
                if assigned_date == "" or assigned_test is None or ids is None:
                    messages.error(request, ' Select all information.')
                    return render(request, 'Nitor/assignTest.html', context)
                _c = CandidateStatus(candidate=ids, exam_date=assigned_date,
                                     question_paper=assigned_test, mcq_ans=mcq_ans, code_ans=code_ans,
                                     total_score=total_score, total_code_score=code_score,
                                     total_mcq_score=mcq_score)
                _c.save()
                return HttpResponseRedirect('/assignTest/name="ALL"')
            return render(request, 'Nitor/assignTestToCandidate.html', context)
    return index(request)


def error404(request):
    return render(request, 'Nitor/error_404.html')


def error500(request):
    return render(request, 'Nitor/error_404.html')

