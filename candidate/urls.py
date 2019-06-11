""" URL SETTING """

from django.conf.urls import url
from candidate import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^candidateHome/$', views.candidate_home, name='candidateHome'),
    url(r'^hello/(?P<pid>\d+)$$', views.ajaxcall, name='ajaxcall'),
    url(r'^ex/', views.ex, name='ex'),
    path('rules/<pid>/<tid>', views.rules, name='rules'),
    path('savetest/<pid>/<tid>', views.savetest, name='savetest'),
    path('starttest/<pid>/<tid>', views.starttest, name='starttes'),
    path('test/<pid>/<tid>', views.test, name='test'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
