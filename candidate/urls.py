""" URL SETTING """

from django.conf.urls import url
from candidate import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('hello/<question_id>', views.ajax_call, name='ajax_call'),
    path('rules/<pid>/<tid>', views.rules, name='rules'),
    path('savetest/<pid>/<tid>', views.save_test, name='save_test'),
    path('starttest/<question_paper_id>/<candidate_status_id>', views.start_test, name='start_test'),
    path('test/<question_paper_id>/<candidate_status_id>', views.test, name='test'),
    path('candidateHome/', views.candidate_home, name='candidate_home'),
    path('logout/', views.user_logout, name='logout'),
]
