"""  URLS setting for nitortest application"""


from django.conf.urls import url
from django.urls import path
from nitortest import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addUser/$', views.add_user, name='addUser'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^success/$', views.save_candidate, name='logout'),
    url(r'^listCandidate/$', views.list_candidates, name='candidateList'),
    url(r'^candidateProfile/(?P<userid>\d+)$', views.candidate_profile, name='candidateProfile'),
    url(r'^removeCandidate/(?P<userid>\d+)$', views.remove_candidate, name='removeCandidate'),
    url(r'^addQuestion/$', views.show_add_question, name='addCode'),
    url(r'^successQue/$', views.success_que, name='successQue'),
    url(r'^createQuePaper/$', views.create_que_paper, name='createQuePaper'),
    url(r'^questionPapers/$', views.question_papers, name='questionPapers'),
    url(r'^fetchQuestionPaper/(?P<questionid>\d+)', views.fetch_question_paper,\
        name='fetchQuestionPaper'),
    url(r'^candidatestatus/(?P<candidate_id>\d+)', views.candidate_status, name='candidatestatus'),
    path('remassigned/<cid>/<pid>/<tid>', views.rem_candidate_status, name='remcandidatestatus'),
    path('removeQuestionPaper/<pid>', views.remove_question_paper, name='removeQuestionPaper'),
    path('showscore/<cid>/<pid>/<tid>', views.show_score, name='showscore'),
    url(r'^listQuestions/$', views.list_questions, name='listQuestion'),
    url(r'^removeQue/(?P<queid>\d+)', views.remove_question, name='removeQue'),
    path('assignTest/<name>', views.assign_test2, name='assignTest'),
]
