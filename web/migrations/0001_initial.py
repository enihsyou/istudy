# Generated by Django 2.0 on 2017-12-18 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='课程名')),
                ('detail', models.TextField(max_length=500, verbose_name='课程详情')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '课程',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='章节名')),
                ('learn_url', models.URLField(verbose_name='download link')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Course', verbose_name='课程')),
            ],
            options={
                'verbose_name': '章节',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '测试试卷',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='问题标题')),
                ('comment', models.TextField(verbose_name='问题主体')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('answer', models.TextField(verbose_name='问题答案')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Paper')),
            ],
            options={
                'verbose_name': '试卷问题',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255, verbose_name='学生姓名')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '学生',
            },
        ),
        migrations.CreateModel(
            name='TakeCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usual_behave_grade', models.IntegerField(verbose_name='平时成绩')),
                ('master_test_grade', models.IntegerField(verbose_name='期末成绩')),
                ('final_term_grade', models.IntegerField(verbose_name='最终成绩')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Course', verbose_name='课程id')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Student', verbose_name='学生id')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255, verbose_name='教师名')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '教师',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(through='web.TakeCourse', to='web.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Teacher', verbose_name='讲师'),
        ),
    ]
