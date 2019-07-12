"""  URLS setting for nitortest application"""


from django.conf.urls import url
from django.urls import path
from nitortest import views
from django.conf.urls import include

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
    path('remassigned/<cid>/<pid>/<tid>', views.rem_candidate_status, name='remcandidatestatus'),
    path('removeQuestionPaper/<pid>', views.remove_question_paper, name='removeQuestionPaper'),
    path('showscore/<cid>/<pid>/<tid>', views.show_score, name='showscore'),
    path('listQuestions/', views.list_questions, name='listQuestions'),
    path('removeQue/<que_id>', views.remove_question, name='remove_question'),
    path('assignTest/<name>', views.assign_test2, name='assignTest'),
    path('health/', include('health_check.urls')),
]
