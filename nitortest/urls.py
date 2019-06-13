"""  URLS setting for nitortest application"""


from django.conf.urls import url
from django.urls import path
from nitortest import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adminHome/', views.admin_home, name='admin_home'),
    path('addUser/', views.add_user, name='addUser'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('success/', views.save_candidate, name='save_candidate'),
    path('listCandidate/', views.list_candidates, name='list_candidates'),
    path('candidateProfile/<user_id>', views.candidate_profile, name='candidateProfile'),
    path('removeCandidate/<user_id>', views.remove_candidate, name='removeCandidate'),
    path('addQuestion/', views.show_add_question, name='addQuestion'),
    path('successQue/', views.success_que, name='successQue'),
    path('createQuePaper/', views.create_que_paper, name='createQuePaper'),
    path('questionPapers/', views.question_papers, name='questionPapers'),
    path('fetchQuestionPaper/<question_id>', views.fetch_question_paper,
         name='fetchQuestionPaper'),
    path('candidatestatus/<candidate_id>', views.candidate_status, name='candidate_status'),

    # url(r'^$', views.index, name='index'),
    # url(r'^adminHome/$', views.admin_home, name='admin_home'),
    # url(r'^addUser/$', views.add_user, name='addUser'),
    # url(r'^login/$', views.login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^success/$', views.save_candidate, name='save_candidate'),
    # url(r'^listCandidate/$', views.list_candidates, name='candidateList'),
    # url(r'^candidateProfile/(?P<userid>\d+)$', views.candidate_profile, name='candidateProfile'),
    # url(r'^removeCandidate/(?P<userid>\d+)$', views.remove_candidate, name='removeCandidate'),
    # url(r'^addQuestion/$', views.show_add_question, name='addCode'),
    # url(r'^successQue/$', views.success_que, name='successQue'),
    # url(r'^createQuePaper/$', views.create_que_paper, name='createQuePaper'),
    # url(r'^questionPapers/$', views.question_papers, name='questionPapers'),
    # url(r'^fetchQuestionPaper/(?P<question_id>\d+)', views.fetch_question_paper,\
    #   name='fetchQuestionPaper'),
    # url(r'^candidatestatus/(?P<candidate_id>\d+)', views.candidate_status, name='candidatestatus'),
    path('remassigned/<cid>/<pid>/<tid>', views.rem_candidate_status, name='remcandidatestatus'),
    path('removeQuestionPaper/<pid>', views.remove_question_paper, name='removeQuestionPaper'),
    path('showscore/<cid>/<pid>/<tid>', views.show_score, name='showscore'),
    path('listQuestions/', views.list_questions, name='listQuestion'),
    path('removeQue/<que_id>', views.remove_question, name='remove_question'),
    # url(r'^listQuestions/$', views.list_questions, name='listQuestion'),
    # url(r'^removeQue/(?P<que_id>\d+)', views.remove_question, name='removeQue'),
    path('assignTest/<name>', views.assign_test2, name='assignTest'),
]
