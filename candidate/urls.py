from django.conf.urls import url
from candidate import views
from django.views.generic.base import TemplateView

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^candidateHome/$',views.candidateHome,name='candidateHome'),	
#	url(r'^addUser/$',views.add_user,name='addUser'),
]