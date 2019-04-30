from django import forms
from django.forms import ModelForm
from .models import Profile
try:
    from string import letters
except ImportError:
    from string import ascii_letters as letters
from string import punctuation, digits
from .models import Profile
from django.forms import ValidationError
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings
from .service import generate_Password,generate_userid
languages = (
    ("select", "Select Language"),
    ("python", "Python"),
    ("c", "C Language"),
    ("cpp", "C++ Language"),
    ("java", "Java Language"),
    ("javascript", "Javascript"),
)

education =(
    ('select','select education'),
    ('btech','B-Tech'),
    ('mtech','M-Tech'),
    ('mca','MCA'),
    ('bca','BCA'),
    ('mcs','MCS'),
    ('bsc','BCS'),
    ('msc','MSC'),    
    ('other','Other'),
    )
department =(
    ('select','select department'),
    ('cs','Computer science'),
    ('management','Management'),
    ('it','Information technology'),
    ('finace','Finance'),
    ('hr','Human resource'),
    ('legal','Legal'),
    ('other','Other'),    
    )
experience = (
    ('select','select experience'),
    ('0','0'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),        
    ('10','10'),
    )

questiontype = (
    ('select','select question type'),
    ('mcq','Multiple choice questionn'),
    ('ct','Coding test'),
    ('tha','Theoretical'),
    )
correct_option = (
    ('select','select correct option'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    )

level = (
    ('select','select level'),
    ('easy','Easy'),
    ('medium','Medium'),
    ('hard','Hard'),
    )


sub = (
    ('select','select subject'),
    ('sql','Sql'),
    ('code','Code'),
    ('networking','Networking'),
    ('aptitude','Aptitude'),
    ('english','English'),
    ('gk','Computer awareness'),   

    )

valid_username = letters + '._' + digits
valid_password = letters + digits + punctuation


#####################################
''' User Registration form  '''
#####################################

class UserRegisterForm(forms.Form):
    #username = forms.CharField(max_length=30, help_text='Letters, digits,\
    #           period and underscores only.')
    
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()     
    education = forms.ChoiceField(choices=education)
    department = forms.ChoiceField(choices=department)
    skill=forms.ChoiceField(choices=languages)
    experience = forms.ChoiceField(choices=experience)
    contact = forms.DecimalField()    
    def clean_first_name(self): 
        first_name=self.cleaned_data['first_name']
        if first_name.strip(letters):
            raise forms.ValidationError('First Name is invalid')
        return first_name
    def clean_last_name(self): 
        last_name=self.cleaned_data['last_name']
        if last_name.strip(letters):
            raise forms.ValidationError('Last Name is invalid')
        return last_name
    def clean_email(self):
        user_email = self.cleaned_data['email']
        if User.objects.filter(email=user_email).exists():
            raise forms.ValidationError("This email already exists, Please use different email")
        return user_email
    def save(self,commit=True,*args,**kwargs):
        cleaned_data=self.cleaned_data
        email=cleaned_data['email']
        first_name=cleaned_data['first_name']
        last_name=cleaned_data['last_name']
        username = email
        password=generate_Password()
        newUser=User.objects.create_user(username,email,password)
        newUser.first_name = first_name
        newUser.last_name=last_name
        newUser.save()
        userid=email
        print("userid =",userid)
        education=cleaned_data['education']
        department=cleaned_data['department']
        experience=cleaned_data['experience']
        contact=cleaned_data['contact']
        skills=cleaned_data['skill']
        role=2
        newUserProfile = Profile(user=newUser,userid=userid,education=education,department=department,experience=experience,contact=contact,skills=skills,role=role)
        newUserProfile.save()
        return newUserProfile





    
#####################################
''' User login form  '''
#####################################
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean(self):        
        super(UserLoginForm, self).clean()
        try:
            u_name, pwd = self.cleaned_data["username"],\
                          self.cleaned_data["password"]
            user = authenticate(username=u_name, password=pwd)            
        except Exception:
            raise forms.ValidationError(
                "Username and/or Password is not entered"
            )
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return user


#####################################
'''Add Question  forms'''
#####################################

# MCQ question form
class addMcqForm(forms.Form):
    subject = forms.ChoiceField(choices=sub)
    question = forms.CharField(max_length=500,help_text='(Question)',widget=forms.Textarea )    
    correct_option=forms.ChoiceField(choices=correct_option)
    total_options = forms.CharField(max_length=20,widget = forms.TextInput(attrs={'readonly':'readonly'})) #,widget=forms.HiddenInput()

    # To create extra fields    
    def __init__(self,*args,**kwargs):
        extra_options = kwargs.pop('extra',0)
        super(addMcqForm,self).__init__(*args,**kwargs)
        self.fields['total_options'].initial = extra_options

        for index in range(int(extra_options)):
            self.fields['option_{index}'.format(index=index)]=forms.CharField()

    def clean_question(self):
        question = self.cleaned_data['question']
        if question:
            question = self.cleaned_data['question']
        else:
            raise forms.ValidationError('*Question missing.')
        return question
    

    def clean_total_options(self):
        options = int(self.cleaned_data['total_options'])
        if options <2:
            raise forms.ValidationError('*Atleast needs two options for a question.')
        return options



# coding test form
class addCodingTestForm(forms.Form):
    title = forms.CharField(max_length=1500)
    description = forms.CharField(max_length=1500,widget=forms.Textarea)
    snippet=forms.CharField(max_length=1500,widget=forms.Textarea)
    language=forms.ChoiceField(choices=languages)
    total_testcases_count=forms.CharField(max_length=300,widget = forms.TextInput(attrs={'readonly':'readonly'})) #widget=forms.HiddenInput()
    level=forms.ChoiceField(choices=level)

    def __init__(self, *args, **kwargs):      
        extra_fields = kwargs.pop('extra', 0)
        super(addCodingTestForm, self).__init__(*args, **kwargs)
        self.fields['total_testcases_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['testcases_{index}'.format(index=index)] = forms.CharField()
            self.fields['outputs_{index}'.format(index=index)] =  forms.CharField()

    def clean_title(self):        
        title = self.cleaned_data['title']
        if title:
            title = self.cleaned_data['title']
        else:
            raise forms.ValidationError('*Title missing.')
        return title





class createQuestionPaper(forms.Form):
    """docstring for createQuestionPaper"forms.rm def __init__(self, arg):
        super (createQuestionPaper,forms.Form.__init__()
        sexlf.arg = arg""" 
    title_qp = forms.CharField(max_length=500,help_text="Question paper explanation like (For candidates/Level of difficulty etc.)",label='Title')  
    totalquestions = forms.CharField(max_length=10,widget = forms.TextInput(attrs={'readonly':'readonly'}),initial=0,label='Total questions you have selected.')
    max_time = forms.DecimalField(label='Maximum time to solve test(minutes)',initial=0)
