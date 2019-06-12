from nitortest.models import Profile
from django.db.models import Q

def login():
	try:
		user=Profile.objects.get(Q(userid='manish.fartyal@nitorinfotech.com')&Q(password='admin@12345'))
	except:
		print('No user found')

login()
