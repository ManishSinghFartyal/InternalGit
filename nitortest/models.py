from django.db import models
from django.contrib.auth.models import User


#############################################################################################################
''' User profile admin and candidate '''
#############################################################################################################

class Profile(models.Model):
   #exporting user module
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   #additional fields
   userid=models.CharField(max_length=100,null=True)
   skills = models.CharField(max_length=20,null=True)
   education=models.CharField(max_length=50,null=True)
   role=models.PositiveIntegerField(default=1,null=True)
   experience=models.PositiveIntegerField(default=1,null=True)
   contact=models.BigIntegerField(null=True)
   department = models.CharField(max_length=30,null=True)
   




#############################################################################################################
''' Question model to store any type of question '''
#############################################################################################################

class Question(models.Model):
   qtype = models.CharField(max_length=50)
   title = models.CharField(max_length=50,null=True)
   description = models.CharField(max_length=500)
   snippet=models.CharField(max_length=100,null=True)
   options = models.CharField(max_length=500,null=True)
   correct_option=models.CharField(max_length=2,null=True)
   testcases=models.CharField(max_length=300,null=True)     
   level=models.CharField(max_length=10,null=True)