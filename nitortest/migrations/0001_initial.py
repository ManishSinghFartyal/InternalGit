# Generated by Django 2.1.7 on 2019-04-04 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.PositiveIntegerField(null=True)),
                ('exam_date', models.DateField()),
                ('question_paper', models.PositiveIntegerField(null=True)),
                ('attempted', models.BooleanField(default=False)),
                ('score', models.CharField(default=0, max_length=1000, null=True)),
                ('total_time', models.PositiveIntegerField(default=0, null=True)),
                ('correct_mcq', models.PositiveIntegerField(default=0, null=True)),
                ('correct_ct', models.PositiveIntegerField(default=0, null=True)),
                ('mcq_ans', models.CharField(default=0, max_length=1000, null=True)),
                ('code_ans', models.CharField(default=0, max_length=1000, null=True)),
                ('starttime', models.DateTimeField(auto_now_add=True, null=True)),
                ('endtime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=100, null=True)),
                ('skills', models.CharField(max_length=20, null=True)),
                ('education', models.CharField(max_length=50, null=True)),
                ('role', models.PositiveIntegerField(default=1, null=True)),
                ('experience', models.PositiveIntegerField(default=1, null=True)),
                ('contact', models.BigIntegerField(null=True)),
                ('department', models.CharField(max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtype', models.CharField(max_length=50, null=True)),
                ('subject', models.CharField(max_length=40, null=True)),
                ('language', models.CharField(max_length=40, null=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=500)),
                ('snippet', models.CharField(max_length=100, null=True)),
                ('options', models.CharField(max_length=500, null=True)),
                ('correct_option', models.CharField(max_length=2, null=True)),
                ('testcases', models.CharField(max_length=300, null=True)),
                ('level', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_qp', models.CharField(max_length=500, null=True)),
                ('total_question', models.PositiveIntegerField(null=True)),
                ('mcq', models.CharField(max_length=2000, null=True)),
                ('coding', models.CharField(max_length=2000, null=True)),
                ('max_time', models.PositiveIntegerField(null=True)),
            ],
        ),
    ]
