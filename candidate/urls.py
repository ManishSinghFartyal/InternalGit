from django.conf.urls import url
from candidate import views
from django.views.generic.base import TemplateView

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^candidateHome/$',views.candidateHome,name='candidateHome'),
	url(r'^test/(?P<testid>\d+)$$',views.test,name='test'),
	url(r'^hello/',views.ajaxcall,name='ajaxcall'),
	url(r'^ex/',views.ex,name='ex'),

#	url(r'^addUser/$',views.add_user,name='addUser'),
]