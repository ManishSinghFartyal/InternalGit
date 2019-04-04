from nitortest.models import Profile,CandidateStatus,QuestionPaper
import ast
import json
from django.db import connection
from django.db.models import Q
from django.utils import timezone

def get_id(user):	
	try:
		profile =Profile.objects.get(userid=user)
		id = profile.user_id		
	except:
		id = None
	return id

def get_test(candidate_id):
	candidate_status = {}
	try:		
		status=CandidateStatus.objects.filter(candidate=candidate_id)
		for i in status:
			paper = QuestionPaper.objects.filter(id=i.question_paper)
			title = ""
			for p in paper:				
				title = p.title_qp
			candidate_status[i.id] = {'paperId':i.question_paper,'paper_title':title,'date':i.exam_date,'attempted':i.attempted,'score':i.score,'time_taken':i.total_time,'mcq_correct':i.correct_mcq,'coding_correct':i.correct_ct,'max_time':p.max_time}
	except:
		candidate_status = {}	
	return candidate_status

def get_question_paper(testid):
	i=1;
	paper={}
	try:
		q_paper = QuestionPaper.objects.get(id=testid)
	except:
		paper={}
	mcqjson={}
	mcq=ast.literal_eval(q_paper.mcq)
	mcq = json.dumps(mcq)
	mcq= json.loads(mcq)
	for key,value in mcq.items():
		mcqvalues=ast.literal_eval(value['options'])
		mcqvalues=json.dumps(mcqvalues)
		mcqvalues=json.loads(mcqvalues)
		#print(type(mcqvalues))
		mcq[key]['sr']=i
		mcq[key]['options'] = mcqvalues
		mcq[key]['type'] = "mcq"
		i=i+1	
	code = {}
	coding=ast.literal_eval(q_paper.coding)
	coding = json.dumps(coding)			
	coding= json.loads(coding)
	for key,value in coding.items():
		testcases=ast.literal_eval(value['testcases'])
		testcases=json.dumps(testcases)
		testcases=json.loads(testcases)		
		code[key]={'desc':value['desc'],'title':value['title'],'language':value['language'],'snippet':value['snippet'],"testcases":testcases,"sr":i,"type":"code"}
		i=i+1
	paper= {'title':q_paper.title_qp,'total':q_paper.total_question,'mcq':mcq,'coding':code,'max_time':q_paper.max_time}
	return paper

def save_answer(answer,userid,testid):	
	ans_split = answer.split("|")
	question = ans_split[0]
	ans=ans_split[1]
	testid = str(testid)
	#GETTING CANDIDATE OBJECT
	candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=testid))
	try:
		mcq_ans=ast.literal_eval(candidate.mcq_ans)
		mcq_ans=json.dumps(mcq_ans)
		mcq_ans=json.loads(mcq_ans)	
	except:
		mcq_ans={}
	mcq_ans[question] = {"answer":ans}
	candidate.mcq_ans = mcq_ans	
	candidate.save()
	return mcq_ans

def get_answered(userid,testid):
	candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=testid))
	try:
		mcq_ans=ast.literal_eval(candidate.mcq_ans)
		mcq_ans=json.dumps(mcq_ans)
		mcq_ans=json.loads(mcq_ans)
	except:
		mcq_ans={}
	return mcq_ans

def save_time(starttime,userid,testid):
	candidate = CandidateStatus.objects.get(Q(candidate=userid)&Q(question_paper=testid))
	candidate.starttime = starttime
	paper = get_question_paper(testid)
	endtime = starttime + timezone.timedelta(minutes=paper["max_time"])
	candidate.endtime = endtime
	candidate.save()
	return endtime

def get_remaining_time(seconds):
	h = seconds//(60*60)
	m = (seconds-h*60*60)//60
	s = seconds-(h*60*60)-(m*60)
	return h, m, s