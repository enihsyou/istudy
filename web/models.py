from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, password=None, **extra_fields):
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password, **extra_fields):
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField('名字', max_length=255, null=False, unique=True)
    add_time = models.DateTimeField("添加时间", auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    USERNAME_FIELD = 'name'

    # objects = MyUserManager()
    class Meta:
        verbose_name = "用户"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Teacher(MyUser):
    point = models.CharField(max_length=50, verbose_name='教学特点')


    class Meta:
        verbose_name = '教师'

    @property
    def teaching_course_count(self):
        return self.course_set.filter(teacher_id=self.id).count()

    def __str__(self):
        return str(self.name)
    #
    # def get_course_nums(self):
    #     return self.course_set.all().count()
    #


class Student(MyUser):
    course = models.ManyToManyField(to="Course", through="TakeCourse", verbose_name="学生参加的课程")

    mobile = models.CharField(max_length=11)


    # def get_image_upload_path(self, file_name):
    #     print(self),
    #     return 'avatar/user_{0}/{1}'.format(self.email, file_name)
    #
    # avatar_image = models.ImageField(
    #     upload_to=get_image_upload_path,
    #     default=u'image/default_avatar.png',
    #     height_field=100, width_field=100)
    @property
    def take_course_count(self):
        return self.takecourse_set.filter(student_id=self.id).count()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "学生"


class Course(models.Model):
    # 每个课程有一个老师
    teacher = models.ForeignKey(Teacher, models.CASCADE, verbose_name='讲师')
    # students = models.ManyToManyField(to=Student, through="TakeCourse")
    name = models.CharField(max_length=50, verbose_name='课程名')
    detail = models.TextField(max_length=500, verbose_name='课程详情')
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

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

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "测试试卷"


class Question(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    title = models.CharField("问题标题", max_length=255)
    comment = models.TextField("问题主体")
    last_modification = models.DateTimeField("最后更新时间", auto_now=True)
    answer = models.TextField("问题答案")

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
