# Generated by Django 2.0 on 2017-12-18 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='takecourse',
            name='final_term_grade',
        ),
        migrations.AlterField(
            model_name='takecourse',
            name='master_test_grade',
            field=models.IntegerField(default=0, verbose_name='期末成绩'),
        ),
        migrations.AlterField(
            model_name='takecourse',
            name='usual_behave_grade',
            field=models.IntegerField(default=0, verbose_name='平时成绩'),
        ),
    ]
