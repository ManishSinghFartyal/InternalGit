from .models import Profile,Question
from django.contrib.auth.models import User


'''
# Function to create random id and password for
user who has been registered by admin
'''
import string
import secrets as sc


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
	allProfiles = Profile.objects.all()
	for profile in allProfiles:
		if profile.role == 2:
			user= User.objects.get(username=profile.userid)
			candidates[profile.userid] = {'id':user.id,'fname':user.first_name,'lname':user.last_name,'email':user.email,'skill':profile.skills,'education':profile.education,'experience':profile.experience,'contact':profile.contact,'department':profile.department}
	#print(candidates['Prashant_??&']['fname'],'  ',candidates['Prashant_??&']['lname'],'  ',candidates['Prashant_??&']['email'])
	return candidates



# Show candidate profile
def candidate_profile(userid):
	candidate={}
	profile = Profile.objects.get(user_id=userid)
	user= User.objects.get(id=userid)
	candidate = {'id':user.id,'userid':profile.userid,'fname':user.first_name,'lname':user.last_name,'email':user.email,'skill':profile.skills,'education':profile.education,'experience':profile.experience,'contact':profile.contact,'department':profile.department}
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
	print(options)
	correct_option = request.POST.get('correct_option')
	question=Question(qtype=type,description=description,options=options,correct_option=correct_option)					
	question.save()	