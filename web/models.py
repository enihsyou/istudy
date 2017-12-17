from django.contrib.auth.models import User
from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name='教师名')
    point = models.CharField(max_length=50, verbose_name='教学特点')
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    class Meta:
        verbose_name = '教师'

    def __str__(self):
        return self.name
    #
    # def get_course_nums(self):
    #     return self.course_set.all().count()
    #


class Student(models.Model):
    name = models.CharField("学生姓名", max_length=255)
    password = models.CharField("密码", max_length=255)
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    # gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='female')
    # mobile = models.CharField(max_length=11)

    # def get_image_upload_path(self, file_name):
    #     print(self),
    #     return 'avatar/user_{0}/{1}'.format(self.email, file_name)
    #
    # avatar_image = models.ImageField(
    #     upload_to=get_image_upload_path,
    #     default=u'image/default_avatar.png',
    #     height_field=100, width_field=100)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "学生"


class Course(models.Model):
    teacher = models.ForeignKey(Teacher, models.CASCADE, verbose_name='讲师')
    name = models.CharField(max_length=50, verbose_name='课程名')
    detail = models.CharField(max_length=300, verbose_name='课程详情')
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程'

    #
    # def get_lesson_nums(self):
    #     """获取课程章节数"""
    #     return self.lesson_set.all().count()
    #
    # get_lesson_nums.short_description = '章节数'
    #
    # # 获取该课程学习用户
    # def get_users_courses(self):
    #     return self.usercourse_set.all()[:5]
    #
    # # 获取讲师数
    # def get_teacher_nums(self):
    #     return self.course_org.teacher_set.all().count()
    #
    # # 获取课程章节
    # def get_course_lesson(self):
    #     return self.lesson_set.all().order_by('name')


class Lesson(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '章节'

    # # 获取章节视频
    # def get_lesson_video(self):
    #     return self.video_set.all()


class TakeCourse(models.Model):
    student_uid = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生id")
    course_uid = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程id")
    usual_behave_grade = models.IntegerField("平时成绩")
    master_test_grade = models.IntegerField("期末成绩")
    final_term_grade = models.IntegerField("最终成绩")

    def __str__(self):
        return self.final_term_grade

#
# class Paper(models.Model):
#     create_time = models.DateTimeField("创建时间", auto_now_add=True)
#     last_modification = models.DateTimeField("最后更新时间", auto_now=True)
#     questions = models.ManyToOneRel
#
#     def __str__(self):
#         return self.question_set
#
#     class Meta:
#         verbose_name = "测试试卷"
#
#
# class Question(models.Model):
#     belong_to = models.ForeignKey(Paper, on_delete=models.CASCADE)
#     title = models.CharField("问题标题", max_length=255)
#     comment = models.TextField("问题主体")
#     last_modification = models.DateTimeField("最后更新时间", auto_now=True)
#     answer = models.TextField("问题答案")
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = "试卷问题"


# class UserCourse(models.Model):
#     user = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='用户')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
#     add_time = models.DateTimeField("添加时间", auto_now_add=True)
#
#     class Meta:
#         verbose_name = u'用户课程'
#         verbose_name_plural = verbose_name


# class CourseResource(models.Model):
#     course = models.ForeignKey(Course, models.CASCADE, verbose_name='课程')
#     name = models.CharField(max_length=100, verbose_name='名称')
#     download = models.URLField(upload_to='course/resource/%Y/%m', verbose_name='资源文件')
#     add_time = models.DateTimeField("添加时间", auto_now_add=True)
#
#     class Meta:
#         verbose_name = '课程资源'
#
#     def __str__(self):
#         return self.name
