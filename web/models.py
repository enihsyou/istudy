from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    name = models.CharField(max_length=255)
    point = models.CharField(max_length=50, verbose_name='教学特点')
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    REQUIRED_FIELDS = ('name',)

    def get_absolute_url(self):
        return "/teacher/%i/" % self.id
    class Meta:
        permissions = (
            ('create_course', "创建课程"),
        )
        verbose_name = '教师'

    @property
    def teaching_course_count(self):
        return self.course_set.filter(teacher_id=self.id).count()

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    user = models.OneToOneField(User, models.CASCADE)

    name = models.CharField(max_length=255)
    course = models.ManyToManyField(to="Course", through="TakeCourse", verbose_name="学生参加的课程")
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    REQUIRED_FIELDS = ('name',)

    def get_absolute_url(self):
        return "/student/%i/" % self.id
    @property
    def take_course_count(self):
        return self.takecourse_set.filter(student_id=self.id).count()

    def __str__(self):
        return str(self.name)

    class Meta:
        permissions = (
            ('join_course', "参加课程"),
        )
        verbose_name = "学生"


class Course(models.Model):
    # 每个课程有一个老师
    teacher = models.ForeignKey(Teacher, models.CASCADE, verbose_name='讲师')
    # students = models.ManyToManyField(to=Student, through="TakeCourse")
    name = models.CharField(max_length=50, verbose_name='课程名')
    detail = models.TextField(max_length=500, verbose_name='课程详情')
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    def get_absolute_url(self):
        return "/course/%i/" % self.id
    @property
    def student_count(self):
        return self.student_set.count()

    @property
    def lesson_count(self):
        return self.lesson_set.count()

    def __str__(self):
        return str(self.name)

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
    learn_url = models.URLField("download link")
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    def get_absolute_url(self):
        return "/course/%i/%i/" % (self.course.id, self.id)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '课程章节'

    # # 获取章节视频
    # def get_lesson_video(self):
    #     return self.video_set.all()


class TakeCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程id")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生id")
    usual_behave_grade = models.IntegerField("平时成绩", default=0)
    master_test_grade = models.IntegerField("期末成绩", default=0)

    @property
    def final_term_grade(self):
        return self.usual_behave_grade + self.master_test_grade

    def __str__(self):
        return "{}在{}课上取得了{}分".format(self.student.name, self.course.name, self.final_term_grade)


class Paper(models.Model):
    title = models.CharField("标题", max_length=50)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    last_modification = models.DateTimeField("最后更新时间", auto_now=True)

    def question_count(self):
        return self.question_set.count()

    def get_absolute_url(self):
        return "/paper/%i/" % self.id

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "测试试卷"


class Question(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    title = models.CharField("问题标题", max_length=255)
    comment = models.CharField("问题主体", max_length=255)
    answer = models.CharField("问题答案", max_length=255)
    last_modification = models.DateTimeField("最后更新时间", auto_now=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "试卷问题"

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
