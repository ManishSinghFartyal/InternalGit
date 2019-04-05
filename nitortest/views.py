from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserLoginForm,addCodingTestForm,addMcqForm,createQuestionPaper
from .models import Profile,Question,QuestionPaper,CandidateStatus
from django.db.models import Q
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.contrib.auth import login as auth_login, logout, authenticate
from .service import list_of_candidates,candidate_profile,saveMCQ,createQuestionObject,getCategorizedQuestions,getAllCandidates,getQuestionPaper,getPaper,getCandidateStatus
from django.contrib.auth.models import User
# Create your views here.



def index(request,next_url=None):	
	user =request.user
	if user.is_authenticated:
		if user.is_superuser:
			return render(request,'Nitor/adminHome.html')
		return HttpResponseRedirect('/candidate')
	print("Manishd")
	return redirect('/login')


def saveUserSuccessNotification(request):	
	user =request.user	
	if user.is_superuser:
		return HttpResponseRedirect('/success')
	return redirect('/login')

################# To send user response after Candidate successfully saved ###################
def success(request):
	return render(request,'Nitor/saveCandidate.html')

def index1(request,next_url=None):
	return redirect('/addUser' if not next_url else next_url)

#To check if user has admin rights
def is_admin(userid):		
	try:
		userProfile = Profile.objects.get(userid=userid)
		role=userProfile.role
		if role == 1:
			return True
		else:
			return False
	except Exception:
		print('IN is_admin method : ',Exception)
		return False


###########   To register new user   #########################
def add_user(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			form = UserRegisterForm(request.POST)
			if form.is_valid():
				newUserProfile=form.save()
				return successMessage(request,"Candidate saved successfully")
			else:
				return render(request,'Nitor/register.html',{'form':form})
		form=UserRegisterForm()
		return render(request,'Nitor/register.html',{'form':form})
	return index(request)


###########   To check user login     #########################
def login(request):
	user =request.user
	if user.is_authenticated:
		return index(request)

	next_url = request.GET.get('next')
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data
			print(user)
			auth_login(request, user)
			return index(request,next_url)
		else:
			context={'form':form}
	else:
		form=UserLoginForm()
		context={'form':form}
	return render(request,'Nitor/login.html',context)



########## To logout user django logout() method ##############
def userLogout(request):
	logout(request)
	return redirect('/login')



##################### To list out all the candidates and their details  #########################
def listCandidates(request):
	user = request.user
	if user.is_authenticated:
		if user.is_superuser:
			candidates = list_of_candidates()
			return render(request,'Nitor/candidatesList.html',{'candidates':candidates})
		else:
			return index(request)
			#return render(request,'to candidate home page')
	return render(request,'/login')




##################### To view candidate profile using id #############################
def candidateProfile(request,userid):
	user=request.user
	if user.is_authenticated:
		if user.is_superuser:
			profile =candidate_profile(userid)
			return show_profile(request,profile)
	return index(request)




##################### Code to show profile of a user ###############################
def show_profile(request,profile):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			return render(request,'Nitor/candidateProfile.html',{'candidate':profile})
	return index(request)



########## Removing candidate by using id #####################
def removeCandidate(request,userid):
	print(userid)
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



# save candidate method
def saveCandidate(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			return render(request,'Nitor/saveCandidate.html')
	return index(request)





########## Add new coding questions #####################
def showAddCode(request):
	form1 = addMcqForm()
	form2=addCodingTestForm()
	user=request.user
	if user.is_authenticated:
		if user.is_superuser:
			if request.method == 'POST':
				qtype = request.POST.get('qtype')
			#code to add coding test in database
				if qtype == 'ct':
					print(request.POST.get('total_testcases_count'))
					form2 = addCodingTestForm(request.POST, {'extra':int(request.POST.get('total_testcases_count'))})
					print(form2.is_valid())					
					if form2.is_valid():
						print(qtype)
						test_cases={}
						title= request.POST.get('title')
						level=request.POST.get('level')
						description=request.POST.get('description')
						snippet=request.POST.get('snippet')
						language=request.POST.get('language')
						total_test_cases=int(request.POST.get('total_testcases_count'))
						if total_test_cases:
							total_test_cases+=1
							for index in range(1,total_test_cases):
								case='case'+str(index)
								input_str = 'input_'+str(index)
								output_str = 'output_'+str(index)
								test_cases[case]={'testcase':request.POST.get(input_str),'output':request.POST.get(output_str)}
						testcases=test_cases
						print(qtype,'\n',title,'\n',level,'\n',description,'\n',snippet,'\n',testcases,'\n',language)
						question=Question(qtype=qtype,language=language,title=title,level=level,description=description,snippet=snippet,testcases=testcases)					
						question.save()
						return successMessage(request,"One coding question saved successfully.")

			#code to add mcq in database

				elif qtype == 'mcq':
					print(request.POST.get('total_options'))
					form1 = addMcqForm(request.POST, {'extra':int(request.POST.get('total_options'))})
					if form1.is_valid():
						test_options={}
						question=request.POST.get('question')
						total_options=int(request.POST.get('total_options'))
						if total_options:
							total_options+=1
							for index in range(1,total_options):
								option=str(index)
								option_val = "option_"+str(index)
								test_options[option]=request.POST.get(option_val)
						options = test_options
						correct_option = request.POST.get('correct_option')
						subject= request.POST.get('subject')
						question=Question(qtype=qtype,subject=subject,description=question,options=options,correct_option=correct_option)
						print(qtype,'\n',question,'\n',options,'\n',correct_option,'\n',subject)
						question.save()
						return successMessage(request,"One multiple choice question saved successfully.")
					else:
						return render(request,'Nitor/addCodingQuiz.html',{'form1':form1,'form2':form2,'current':'mcq'})

				form = addCodingTestForm(request.POST, extra=request.POST.get('total_testcases_count'))
				return HttpResponse("Data needs to be saved.")
			else:
				form1 = addMcqForm()
				form2=addCodingTestForm()
				context ={'form1':form1,'form2':form2,'current':None}
				return render(request,'Nitor/addCodingQuiz.html',context)
	return index(request)



# To show the success message after adding a question
def successQue(request):
	user=request.user
	if user.is_authenticated:
		if user.is_superuser:
			return render(request,'Nitor/queSuccessMessage.html')
	return index(request)


# To create question paper
def getQuestions(request):
	# fetching all the questions from database to manage in interpolation
	questions = Question.objects.values()
	return JsonResponse({'questions': list(questions)})


# To create question paper
def createQuePaper(request):
	# fetching all the questions from database to manage in interpolation
	user=request.user
	questions = Question.objects.all()
	que = createQuestionObject()
	form = createQuestionPaper()
	context={'form':form,'questions':que}
	user=request.user
	if user.is_authenticated:
		if user.is_superuser:
			if request.method == 'POST':
				form = createQuestionPaper(request.POST)
				total = int(request.POST.get('totalquestions'))
				if total == 0:
					messages.error(request,'**Questions not selected.')
					return render(request,'Nitor/createQuestion.html',context)
				title = request.POST.get('title_qp')
				if not title:
					messages.error(request,'**Please enter title.')
					return render(request,'Nitor/createQuestion.html',context)
				questions = request.POST.getlist('questionid')
				mcq,ct=getCategorizedQuestions(questions)
				maxtime = int(request.POST.get('max_time'))
				if maxtime == 0:
					messages.error(request,'**Enter max time')
					return render(request,'Nitor/createQuestion.html',context)
				qp = QuestionPaper(title_qp=title,total_question=total,mcq=mcq,coding=ct,max_time=maxtime)
				qp.save()
				return successMessage(request,"Question paper created successfully.")
			else:
				return render(request,'Nitor/createQuestion.html',context)
	return index(request)



# to show success message on completing some event.
def successMessage(request,message):
	user=request.user
	if user.is_authenticated:
		if user.is_superuser:
			return render(request,'Nitor/successMessage.html',{'message':message})
	return index(request)

# Code to assign the test for canidates.
def assignTest(request):
	user=request.user
	if user.is_authenticated:
		if user.is_superuser:
			candidates=getAllCandidates()			
			question_papers = QuestionPaper.objects.all()
			context = {'candidates':candidates,'papers':question_papers}
			if request.method == 'POST':
				ids= request.POST.getlist('candidate_id')
				if not ids:
					messages.error(request,'**No candidate selected.')
					return render(request,'Nitor/assignTest.html',context)
				for i in ids:
					test_str = i+"-paper"
					date_str = i+"-date"
					assigned_test = request.POST.get(test_str)
					assigned_date =  request.POST.get(date_str)
					mcq_ans = {}
					if assigned_date == "" or assigned_test is None:
						messages.error(request,' Either date of test or exam not selected.')
						return render(request,'Nitor/assignTest.html',context)
					c=CandidateStatus(candidate=i,exam_date=assigned_date,question_paper=assigned_test,mcq_ans=mcq_ans)
					c.save()
				return successMessage(request,"Successfully asssigned")
			else:
				return render(request,'Nitor/assignTest.html',context)
	return index(request)

# Code to show question papers
def questionPapers(request):
	user=request.user
	if user.is_authenticated:
		if user.is_superuser:
			qp = getQuestionPaper()
			return render(request,'Nitor/questionPaper.html',{'paper':qp})
	return index(request)

def fetchQuestionPaper(request,questionid):
	id = int(questionid)
	q_paper = QuestionPaper.objects.get(id=questionid)
	paper = getPaper(q_paper)
	return render(request,'Nitor/showQuestion.html',{'paper':paper,'id':id})

def candidatestatus(request,candidateid):
	id = int(candidateid)
	cst = getCandidateStatus(id)
	return render(request,'Nitor/candidateStatus.html',{'status':cst,'cid':candidateid})

def remcandidatestatus(request,cid,pid):
	print(cid,"   ",pid)
	CandidateStatus.objects.get(candidate=cid,question_paper=pid).delete()
	url = "/candidatestatus/"+cid
	print(url)
	return HttpResponseRedirect(url)

def removeQuestionPaper(request,pid):
	id = int(pid)
	q_paper = QuestionPaper.objects.get(id=pid).delete()
	return HttpResponseRedirect("/questionPapers")
