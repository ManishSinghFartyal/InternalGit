""" FORMS HAVE BEEN CREATED"""

try:
    from string import letters
except ImportError:
    from string import ascii_letters as letters
from string import punctuation, digits
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from .models import Profile
# from django.core.mail import send_mail
# from Onlinetest import settings
from .service import generate_password
LANGUAGES = (
    ("select", "Select Language"),
    ("python", "Python"),
    ("c", "C Language"),
    ("cpp", "C++ Language"),
    ("java", "Java Language"),
    ("javascript", "Javascript"),
)
EDUCATION = (
    ('select', 'select education'),
    ('btech', 'B-Tech'),
    ('mtech', 'M-Tech'),
    ('mca', 'MCA'),
    ('bca', 'BCA'),
    ('mcs', 'MCS'),
    ('bsc', 'BCS'),
    ('msc', 'MSC'),
    ('other', 'Other'),
    )
DEPARTMENT = (
    ('select', 'select department'),
    ('cs', 'Computer science'),
    ('management', 'Management'),
    ('it', 'Information technology'),
    ('finace', 'Finance'),
    ('hr', 'Human resource'),
    ('legal', 'Legal'),
    ('other', 'Other'),
    )
EXPERIENCE = (
    ('select', 'select experience'),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    )

QUESTION_TYPE = (
    ('select', 'select question type'),
    ('mcq', 'Multiple choice questionn'),
    ('ct', 'Coding test'),
    ('tha', 'Theoretical'),
    )
CORRECT_OPTION = (
    ('select', 'select correct option'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    )

LEVEL = (
    ('select', 'select level'),
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
    )

SUB = (
    ('select', 'select subject'),
    ('sql', 'Sql'),
    ('code', 'Code'),
    ('networking', 'Networking'),
    ('aptitude', 'Aptitude'),
    ('english', 'English'),
    ('gk', 'Computer awareness'),
    ('ds', 'Data Structure'),
    ('dp', 'Design Pattern'),
    ('py', 'Python'),
    ('java', 'Java'),
    ('c', 'C'),
    ('net', '.Net'),
    )

VALID_USERNAME = letters + '._' + digits
VALID_PASSWORD = letters + digits + punctuation


class UserRegisterForm(forms.Form):
    """ User Registration form  """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    education = forms.ChoiceField(choices=EDUCATION)
    department = forms.ChoiceField(choices=DEPARTMENT)
    skill = forms.ChoiceField(choices=LANGUAGES)
    experience = forms.ChoiceField(choices=EXPERIENCE)
    contact = forms.DecimalField()

    def clean_first_name(self):
        """Validation"""
        first_name = self.cleaned_data['first_name']
        if first_name.strip(letters):
            raise forms.ValidationError('First Name is invalid')
        return first_name

    def clean_last_name(self):
        """Validation"""
        last_name = self.cleaned_data['last_name']
        if last_name.strip(letters):
            raise forms.ValidationError('Last Name is invalid')
        return last_name

    def clean_email(self):
        """Validation"""
        user_email = self.cleaned_data['email']
        if User.objects.filter(email=user_email).exists():
            raise forms.ValidationError("This email already exists,  Please use different email")
        return user_email

    def save(self):
        """Validation"""
        cleaned_data = self.cleaned_data
        email = cleaned_data['email']
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        username = email
        password = generate_password()
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        education = cleaned_data['education']
        _department = cleaned_data['department']
        _experience = cleaned_data['experience']
        contact = cleaned_data['contact']
        skills = cleaned_data['skill']
        new_user_profile = Profile(user=new_user, userid=email,
                                   education=education, department=_department,
                                   experience=_experience, contact=contact, skills=skills,
                                   role=2)
        password_msg = "Password for test : "+password
        # email = EmailMessage(
        # subject='Password',
        # body=password_msg,
        # from_email='manishfartyal9090@gmail.com',
        # to=[email],
        # )
        # send_mail('Password', 'password_msg',  settings.EMAIL_HOST_USER, [email])
        email = EmailMessage('Password', 'password_msg', to=[email])
        email.send()
        new_user_profile.save()
        return new_user_profile


class UserLoginForm(forms.Form):

    """ User login form  """
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean(self):
        """ Validation  """
        super(UserLoginForm, self).clean()
        try:
            u_name, pwd = self.cleaned_data["username"], self.cleaned_data["password"]
            user = authenticate(username=u_name, password=pwd)
        except Exception:
            raise forms.ValidationError(
                "Username and/or Password is not entered"
            )
        if not user:

            raise forms.ValidationError("Invalid username/password")
        return user


class AddMcqForm(forms.Form):
    """Add Question  forms"""
    subject = forms.ChoiceField(choices=SUB)
    question = forms.CharField(max_length=500, help_text='(Question)', widget=forms.Textarea)
    correct_option = forms.ChoiceField(choices=CORRECT_OPTION)
    total_options = forms.CharField(max_length=20, widget=forms.TextInput(\
        attrs={'readonly':'readonly'}))

    # To create extra fields
    def __init__(self, *args, **kwargs):
        """ Validation  """
        extra_options = kwargs.pop('extra', 0)
        super(AddMcqForm, self).__init__(*args, **kwargs)
        self.fields['total_options'].initial = extra_options

        for index in range(int(extra_options)):
            self.fields['option_{index}'.format(index=index)] = forms.CharField()

    def clean_question(self):
        """ validation"""
        question = self.cleaned_data['question']
        if question:
            question = self.cleaned_data['question']
        else:
            raise forms.ValidationError('*Question missing.')
        return question

    def clean_total_options(self):
        """ validation"""

        options = int(self.cleaned_data['total_options'])
        if options < 2:
            raise forms.ValidationError('*Atleast needs two options for a question.')
        return options



# coding test form
class AddCodingTestForm(forms.Form):
    """coding test form"""
    title = forms.CharField(max_length=1500)
    description = forms.CharField(max_length=1500, widget=forms.Textarea)
    snippet = forms.CharField(max_length=1500, widget=forms.Textarea)
    language = forms.ChoiceField(choices=LANGUAGES)
    total_testcases_count = forms.CharField(max_length=300, \
        widget=forms.TextInput(attrs={'readonly':'readonly'}))
    level = forms.ChoiceField(choices=LEVEL)

    def __init__(self, *args, **kwargs):
        """ Testcases """
        extra_fields = kwargs.pop('extra', 0)
        super(AddCodingTestForm, self).__init__(*args, **kwargs)
        self.fields['total_testcases_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['testcases_{index}'.format(index=index)] = forms.CharField()
            self.fields['outputs_{index}'.format(index=index)] = forms.CharField()

    def clean_title(self):
        """Check title is not empty"""
        title = self.cleaned_data['title']
        if title:
            title = self.cleaned_data['title']
        else:
            raise forms.ValidationError('*Title missing.')
        return title

class CreateQuestionPaper(forms.Form):
    """docstring for createQuestionPaper forms.rm def __init__(self,  arg):
        super (createQuestionPaper, forms.Form.__init__()
        sexlf.arg  =  arg"""
    title_qp = forms.CharField(max_length=500, \
        help_text="Question paper explanation like (For candidates/Level of difficulty etc.)",\
        label='Title')
    totalquestions = forms.CharField(max_length=10,\
    widget=forms.TextInput(attrs={'readonly':'readonly'}), initial=0,\
    label='Total questions you have selected.')
    max_time = forms.DecimalField(label='Maximum time to solve test(minutes)', initial=0)
