from .models import Profile,Question,CandidateStatus,QuestionPaper
from django.contrib.auth.models import User


'''
# Function to create random id and password for
user who has been registered by admin
'''
import string
import secrets as sc
import json
import ast


'''
To automatically generate user password using the choice method from secret 
package which combines aal the possible permutation and combination for 
ascii letters and digits and return the string with length 8
'''

def generate_Password():	
	keys2=string.ascii_letters + string.digits
	pwd = ''.join(sc.choice(keys2) for i in range(8))
	return pwd



'''
To automatically generate user id using the choice method from secret 
package which combines all the possible permutation and combination for 
symbols and return the string with length 4 + the username
'''
def generate_userid(username):	
	keys2='!@#$%&*()?'
	userid = username +'_'+''.join(sc.choice(keys2) for i in range(3))
	print('User_id  = ',userid)
	return userid




'''
To get all the candidates list from database
'''
def list_of_candidates():
	candidates={}
	try:
		allProfiles = Profile.objects.all()
	except:
		return candidates
	for profile in allProfiles:
		if profile.role == 2:
			try:
				user= User.objects.get(id=profile.user_id)
				candidates[profile.userid] = {'id':user.id,'fname':user.first_name,'lname':user.last_name,'email':user.email,'skill':profile.skills,'education':profile.education,'experience':profile.experience,'contact':profile.contact,'department':profile.department}
			except:
				continue
	return candidates



# Show candidate profile
def candidate_profile(userid):
	candidate={}
	try:
		profile = Profile.objects.get(user_id=userid)
		if CandidateStatus.objects.filter(candidate=userid).count() >= 1:
			cs='Already Assigned'
		else:
			cs = 'Not assigned'
		user= User.objects.get(id=userid)
		candidate = {'id':user.id,'fname':user.first_name,'lname':user.last_name,'email':user.email,'skill':profile.skills,'education':profile.education,'experience':profile.experience,'contact':profile.contact,'department':profile.department,'status':cs}
	except:
		return candidate
	return candidate


# Save MCQ question
def saveMCQ(request):
	test_options={}
	description=request.POST.get('description')
	total_options=int(request.POST.get('total_options'))
	if total_options:
		total_options+=1
		for index in range(1,total_options):
			option='option_'+str(index)							
			test_options[option]=request.POST.get(option)
	options = test_options
	correct_option = request.POST.get('correct_option')
	question=Question(qtype=type,description=description,options=options,correct_option=correct_option)					
	question.save()	


# Create question object with string as json
def createQuestionObject():
	try:
		questions = Question.objects.all()
	except:
		return que
	que={}
	js=None
	tc= None
	for question in questions:
		if question.options:
			#question.options.replace("'",'"')
			js=ast.literal_eval(question.options)
			js = json.dumps(js)			
			js= json.loads(js)
		if question.testcases:
			#question.testcases.replace("'",'"')
			tc = ast.literal_eval(question.testcases)
			tc = json.dumps(tc)			
			tc= json.loads(tc)
		desc= question.description
		l = len(desc)
		if question.title:
			pre = question.title
			post= desc
		else:
			pre = desc[:25]
			post =desc[:l]
		que[question.id] = {"qtype":question.qtype,"subject":question.subject or None,"language":question.language or None,"title":question.title or None,"description":question.description or None,"snippet":question.snippet or None,"options":js,"correct_option":question.correct_option or None,"testcases":tc,"level":question.level or None,"pre":pre,"post":post}	
		
	return que

'''
 Function takes input mixed questions list and part them into mcq and coding test
'''
def getCategorizedQuestions(questions):
	mcq = {}
	ct= {}
	for question in questions:
		que = Question.objects.get(id=question)
		qtype = que.qtype
		if qtype == 'mcq':
			mcq[que.id] = {'desc':que.description,'options': que.options}
		elif qtype == 'ct':
			ct[que.id] = que.description
	return mcq,ct


'''
To get all candidates list
'''
def getAllCandidates():
	candidate_dict = {}	
	try:
		candidates_list = Profile.objects.all()
	except:
		return candidates_dict
	for candidate in candidates_list:
		if candidate.role == 2:
			print(candidate.user_id)		
			candidate_dict[candidate.id] = candidate_profile(candidate.user_id)
	return candidate_dict

'''
To get all question paper details
'''
def getQuestionPaper():
	q_paper={}
	try:
		q_paper_db = QuestionPaper.objects.all()
		for paper in q_paper_db:			
			q_paper[paper.id] = {'title':paper.title_qp,'total_q':paper.total_question,'mcq':paper.mcq,'coding':paper.coding,'max_time':paper.max_time}
	except:
		return q_paper
	return q_paper

def getPaper(q_paper):
	paper = {}
	mcqjson={}
	mcq=ast.literal_eval(q_paper.mcq)
	mcq = json.dumps(mcq)			
	mcq= json.loads(mcq)
	for key,value in mcq.items():
		mcqvalues=ast.literal_eval(value['options'])
		mcqvalues=json.dumps(mcqvalues)
		mcqvalues=json.loads(mcqvalues)
		#print(type(mcqvalues))
		mcq[key]['options'] = mcqvalues
	
	coding=ast.literal_eval(q_paper.coding)
	coding = json.dumps(coding)			
	coding= json.loads(coding)
	paper= {'title':q_paper.title_qp,'total':q_paper.total_question,'mcq':mcq,'coding':coding,'max_time':q_paper.max_time}
	return paper

def getCandidateStatus(candidateid):
	candidate_status = {}
	try:		
		status=CandidateStatus.objects.filter(candidate=candidateid)
		for i in status:
			paper = QuestionPaper.objects.filter(id=i.question_paper)
			title = ""
			for p in paper:
				title = p.title_qp
			candidate_status[i.id] = {'paperId':i.question_paper,'paper_title':title,'date':i.exam_date,'attempted':i.attempted,'score':i.score,'time_taken':i.total_time,'mcq_correct':i.correct_mcq,'coding_correct':i.correct_ct}
	except:
		candidate_status = {}
	return candidate_status

