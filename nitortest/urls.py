from django.conf.urls import url
from nitortest import views
from django.views.generic.base import TemplateView

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^addUser/$',views.add_user,name='addUser'),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.userLogout,name='logout'),
	url(r'^success/$',views.saveCandidate,name='logout'),
	url(r'^listCandidate/$',views.listCandidates,name='candidateList'),
	url(r'^candidateProfile/(?P<userid>\d+)$',views.candidateProfile,name='candidateProfile'),
	url(r'^removeCandidate/(?P<userid>\d+)$',views.removeCandidate,name='removeCandidate'),
	url(r'^addCode/$',views.showAddCode,name='addCode'),
	url(r'^successQue/$',views.successQue,name='successQue'),
	url(r'^createQuePaper/$',views.createQuePaper,name='createQuePaper'),
	url(r'^assignTest/$',views.assignTest,name='assignTest'),
]