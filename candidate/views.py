from django.shortcuts import render
from .service import get_id,get_test
from django.http import HttpResponseRedirect
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