from nitortest.models import Profile,CandidateStatus,QuestionPaper
import ast
import json

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