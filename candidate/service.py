from nitortest.models import Profile,CandidateStatus,QuestionPaper

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