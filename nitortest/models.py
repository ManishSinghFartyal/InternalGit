'''MODEL FORMS'''

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    ''' User profile admin and candidate '''
    #exporting user module
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #additional fields
    userid = models.CharField(max_length=100, null=True)
    skills = models.CharField(max_length=20, null=True)
    education = models.CharField(max_length=50, null=True)
    role = models.PositiveIntegerField(default=1, null=True)
    experience = models.PositiveIntegerField(default=1, null=True)
    contact = models.BigIntegerField(null=True)
    department = models.CharField(max_length=30, null=True)


class Question(models.Model):
    ''' Question model to store any type of question '''
    qtype = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=40, null=True)
    language = models.CharField(max_length=40, null=True)
    title = models.CharField(max_length=1500, null=True)
    description = models.CharField(max_length=1500)
    snippet = models.CharField(max_length=1500, null=True)
    options = models.CharField(max_length=1500, null=True)
    correct_option = models.CharField(max_length=2, null=True)
    testcases = models.CharField(max_length=1300, null=True)
    level = models.CharField(max_length=10, null=True)



class QuestionPaper(models.Model):
    ''' Question paper model to create question paper for exam '''
    title_qp = models.CharField(max_length=500, null=True)
    total_question = models.PositiveIntegerField(null=True)
    mcq = models.CharField(max_length=2000, null=True)
    coding = models.CharField(max_length=2000, null=True)
    max_time = models.PositiveIntegerField(null=True)


class CandidateStatus(models.Model):
    ''' Candidate status for test '''
    candidate = models.PositiveIntegerField(null=True)
    exam_date = models.DateField()
    question_paper = models.PositiveIntegerField(null=True)
    attempted = models.BooleanField(default=False)
    score = models.CharField(max_length=1000, null=True, default=0)
    total_time = models.PositiveIntegerField(null=True, default=0)
    correct_mcq = models.PositiveIntegerField(null=True, default=0)
    correct_ct = models.PositiveIntegerField(null=True, default=0)
    mcq_ans = models.CharField(max_length=1000, null=True, default=0)
    code_ans = models.CharField(max_length=1000, null=True, default=0)
    starttime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    endtime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    total_mcq_score = models.PositiveIntegerField(null=True, default=0)
    total_code_score = models.PositiveIntegerField(null=True, default=0)
    mcq_score = models.PositiveIntegerField(null=True, default=0)
    code_score = models.PositiveIntegerField(null=True, default=0)
    total_score = models.PositiveIntegerField(null=True, default=0)
