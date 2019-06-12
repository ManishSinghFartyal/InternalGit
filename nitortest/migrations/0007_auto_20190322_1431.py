# Generated by Django 2.1.7 on 2019-03-22 09:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nitortest', '0006_auto_20190320_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionpaper',
            name='coding',
            field=models.CharField(max_length=100, null=True, validators=[django.core.validators.int_list_validator]),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='mcq',
            field=models.CharField(max_length=100, null=True, validators=[django.core.validators.int_list_validator]),
        ),
    ]
