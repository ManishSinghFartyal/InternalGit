from django.shortcuts import render,redirect
from .service import get_id,get_test,get_question_paper,save_answer,get_answered,save_time,get_remaining_time,save_code,countScore
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import login as auth_login, logout, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from nitortest.models import CandidateStatus
from django.db.models import Q
import datetime
from django.contrib import messages


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


def starttest(request,testid):
	answered = {}
	user = request.user	
	if user.is_authenticated:
		if user.is_superuser:
			return index(request)
		#If user submit a mcq answer
		else:
			userid = get_id(user)
			starttime = timezone.localtime(timezone.now())
			endtime = save_time(starttime,userid,testid)
			test_str="/candidate/test/"+testid
			request.session['currentpage']=1
			return HttpResponseRedirect(test_str)
	return index(request)


def test(request,testid):
	answered = {}
	user = request.user	
	if user.is_authenticated:
		if user.is_superuser:
			return index(request)
		#If user submit a mcq answer
		else:
			userid = get_id(user)
			mcq_answered,code_answered = get_answered(userid,testid)
			page = request.GET.get('page', 1)
			i = testid
			paper = get_question_paper(i)
			candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=testid))
			#candidate.attempted =True
			candidate.save()
			if request.method == 'POST':
				if request.GET.get("type") == 'mcq':
					endtime = candidate.endtime
					remanining = endtime -  timezone.localtime(timezone.now())
					time = remanining.total_seconds()
					h,m,s=get_remaining_time(time)
					try:
						ans = request.POST.get("correct")
						save_answer(ans,userid,testid)
						page=int(request.GET.get('page'))
					except:
						page=int(request.GET.get('page'))
					mcq_answered,code_answered = get_answered(userid,testid)
					question = {'mcq':paper['mcq'],'code':paper["coding"]}
					question_paper = {}
					for key,value in question.items():
						for k,v in value.items():
							question_paper[k] = v
					t = tuple(question_paper.items())
					p = Paginator(t,1)
					total_pages = p.num_pages
					paginate = p.page(page)
					if page<total_pages:						
						request.session['currentpage']=paginate.next_page_number()
						paginate = p.page(request.session['currentpage'])
						pages = dict(paginate)
					elif page==total_pages:
						request.session['currentpage']=paginate.previous_page_number()
						paginate = p.page(page)
						pages = dict(paginate)
					else:
						pages = None
						request.session['currentpage']=1
				elif request.GET.get("type") == 'code':
					endtime = candidate.endtime
					remanining = endtime -  timezone.localtime(timezone.now())
					time = remanining.total_seconds()
					h,m,s=get_remaining_time(time)
					page=int(request.GET.get('page'))
					mcq_answered,code_answered = get_answered(userid,testid)
					question = {'mcq':paper['mcq'],'code':paper["coding"]}
					question_paper = {}
					for key,value in question.items():
						for k,v in value.items():
							question_paper[k] = v
					t = tuple(question_paper.items())
					p = Paginator(t,1)
					total_pages = p.num_pages
					paginate = p.page(page)
					if page<total_pages:						
						request.session['currentpage']=paginate.next_page_number()
						paginate = p.page(request.session['currentpage'])
						pages = dict(paginate)
					elif page==total_pages:
						request.session['currentpage']=paginate.previous_page_number()
						paginate = p.page(page)
						pages = dict(paginate)
					else:
						pages = None
						request.session['currentpage']=1
			else:
				endtime = candidate.endtime
				remanining = endtime -  timezone.localtime(timezone.now())
				page = int(request.GET.get('page',1))
				time = remanining.total_seconds()
				h,m,s=get_remaining_time(time)
				question = {'mcq':paper['mcq'],'code':paper["coding"]}
				question_paper = {}
				for key,value in question.items():
					for k,v in value.items():
						question_paper[k] = v
				t = tuple(question_paper.items())
				p = Paginator(t,1)
				request.session['currentpage']=page
				paginate = p.page(page)
				pages = dict(paginate)
		return render(request,'test.html',{'testid':testid,'paper_details':paper,'paper':question_paper,'pages':pages,'paginator':paginate,'mcq_answered':mcq_answered,'code_answered':code_answered,'hour':int(h),'minute':int(m),'second':int(s)})
	return redirect("/login")

def savetest(request,testid):
	user = request.user	
	if user.is_authenticated:
		if user.is_superuser:			
			return index(request)
		#If user submit a mcq answer
		else:
			request.message = 'Successfully submitted test.'
			userid = get_id(user)
			countScore(userid,testid)
			candidateHome(request)
	return redirect("/login")


def ajaxcall(request,queid):
	userid = get_id(request.user)
	code = request.GET['code']
	testid = request.GET['testid']
	json = cPython.run_code2(code,userid,queid)
	save_code(queid,code,json,userid,testid)
	return JsonResponse(json)


def ex(request):
		return render(request,'ex.html')


def rules(request,testid):
	user = request.user	
	if user.is_authenticated:
		if user.is_superuser:
			return index(request)
		#If user submit a mcq answer
		else:
			return render(request,'rules.html',{'testid':testid})
	return redirect("/login")