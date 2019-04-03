from django.shortcuts import render,redirect
from .service import get_id,get_test,get_question_paper,save_answer,get_answered
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import login as auth_login, logout, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

# Create your views here.
from . import checkCodePython as cPython

def index(request,next_url=None):	
	user =request.user
	if user.is_superuser:		
			return render(request,'Nitor/adminHome.html')
	return HttpResponseRedirect('/candidate/candidateHome')

def candidateHome(request):
	user=request.user
	id = get_id(user)
	tests = get_test(id)
	return render(request,'candidateHome.html',{'tests':tests})

def test(request,testid):
	answered = {}
	time = 0
	user = request.user	
	if user.is_authenticated:
		if user.is_superuser:
			return index(request)
		#If user submit a mcq answer
		elif request.method == 'POST':
			userid = get_id(user)
			ans = request.POST.get("correct")
			page = int(request.GET.get('page', 1))
			answered = save_answer(ans,userid,testid)
			i = testid
			paper = get_question_paper(i)
			question = {'mcq':paper['mcq'],'code':paper["coding"]}			
			question_paper = {}
			for key,value in question.items():
				for k,v in value.items():
					question_paper[k] = v
			t = tuple(question_paper.items())
			p = Paginator(t,1)
			paginate = p.page(page)
			pages = dict(paginate)
			starttime = timezone.now
		else:
			userid = get_id(user)
			answered = get_answered(userid,testid)			
			page = request.GET.get('page', 1)
			i = testid
			paper = get_question_paper(i)
			question = {'mcq':paper['mcq'],'code':paper["coding"]}
			question_paper = {}
			for key,value in question.items():
				for k,v in value.items():
					question_paper[k] = v
			t = tuple(question_paper.items())
			p = Paginator(t,1)
			paginate = p.page(page)
			pages = dict(paginate)
			starttime = timezone.localtime(timezone.now())
			endtime = timezone.localtime(timezone.now())
			endtime = endtime+timezone.timedelta(minutes=paper["max_time"])
			print(starttime,"   ",endtime)
		return render(request,'test.html',{'paper_details':paper,'paper':question_paper,'pages':pages,'paginator':paginate,'answered':answered,'starttime':starttime})
	return redirect("/login")


def ajaxcall(request):
	code = request.GET['code']
	output = cPython.run_code(code)
	return HttpResponse(output)


def ex(request):
		return render(request,'ex.html')