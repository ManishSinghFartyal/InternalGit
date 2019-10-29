# Generated by Django 2.1.7 on 2019-03-20 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nitortest', '0005_auto_20190320_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatestatus',
            name='correct_ct',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='candidatestatus',
            name='correct_mcq',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='candidatestatus',
            name='score',
            field=models.CharField(default=0, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='candidatestatus',
            name='total_time',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]