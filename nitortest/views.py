from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserLoginForm,addCodingTestForm,addMcqForm,createQuestionPaper
from .models import Profile,Question
from django.db.models import Q
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import login as auth_login, logout, authenticate
from .service import list_of_candidates,candidate_profile,saveMCQ
from django.contrib.auth.models import User
# Create your views here.



def index(request,next_url=None):	
	user =request.user
	if user.is_superuser:		
			return render(request,'Nitor/adminHome.html')
	return render(request,'Nitor/candidateHome.html')

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
		print(userid)
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
				return saveUserSuccessNotification(request)
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


def show_profile(request,profile):
	if request.user.is_authenticated:
		if request.user.is_superuser:			
			return render(request,'Nitor/candidateProfile.html',{'candidate':profile})
	return index(request)	





########## Removing candidate by using id #####################
def removeCandidate(request,userid):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			try:
				Profile.objects.get(id=userid).delete()
				User.objects.get(id=userid).delete()
				return HttpResponseRedirect('/listCandidate')
			except:
				return HttpResponseRedirect('/listCandidate')
	return index(request)

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
					form2 = addCodingTestForm(request.POST, extra=request.POST.get('total_testcases_count'))
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
					return HttpResponseRedirect("/successQue/")

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
								option='option_'+str(index)	
								test_options[option]=request.POST.get(option)
						options = test_options
						correct_option = request.POST.get('correct_option')
						subject= request.POST.get('subject')
						question=Question(qtype=qtype,subject=subject,description=question,options=options,correct_option=correct_option)
						print(qtype,'\n',question,'\n',options,'\n',correct_option,'\n',subject)
						question.save()
						return HttpResponseRedirect("/successQue/")
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
def createQuePaper(request):
	questions = Question.objects.all()
	form = createQuestionPaper()
	context={'form':form,'questions':questions}
	user=request.user
	if user.is_authenticated:
		if user.is_superuser:
			if request.method is 'POST':
				print('mehod')
			else:
				return render(request,'Nitor/createQuestion.html',context)
	return index(request)