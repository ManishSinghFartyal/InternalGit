""" URL SETTING """

from django.conf.urls import url
from candidate import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^candidateHome/$', views.candidate_home, name='candidateHome'),
    url(r'^hello/(?P<pid>\d+)$$', views.ajax_call, name='ajax_call'),
    path('rules/<pid>/<tid>', views.rules, name='rules'),
    path('savetest/<pid>/<tid>', views.save_test, name='save_test'),
    path('starttest/<pid>/<tid>', views.start_test, name='start_test'),
    path('test/<pid>/<tid>', views.test, name='test'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
