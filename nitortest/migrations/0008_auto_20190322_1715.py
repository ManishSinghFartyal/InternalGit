# Generated by Django 2.1.7 on 2019-03-22 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nitortest', '0007_auto_20190322_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionpaper',
            name='coding',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='mcq',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
