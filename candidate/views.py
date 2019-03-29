from django.shortcuts import render,redirect
from .service import get_id,get_test,get_question_paper
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import login as auth_login, logout, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

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
	time = 0
	user = request.user	
	if user.is_authenticated:
		if user.is_superuser:
			return index(request)
		else:
			print(request.GET.get('page'))
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
			return render(request,'test.html',{'paper_details':paper,'paper':question_paper,'pages':pages,'paginator':paginate})
	return redirect("/login")