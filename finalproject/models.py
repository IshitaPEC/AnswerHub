from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator


# Set up Default Field Values
class DefaultUser:
    username = "dummy"
    password = "123"
    contactNumber = "9999999999"
    questionText = "SampleQuestion"
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")


def get_default_user():
    return User.objects.get(username=DefaultUser.username, password=DefaultUser.password)


def get_default_student():
    return StudentInfo.objects.get(user=get_default_user, contactNumber=DefaultUser.contactNumber)


def get_default_question():
    return TeacherInfo.objects.get(questionText=DefaultUser.questionText)


def get_default_teacher():
    return TeacherInfo.objects.get(contactNumber=DefaultUser.contactNumber)


# Student Information
# Added regex validation for phone numbers
# Added email field
class StudentInfo(models.Model):
    user = models.ForeignKey(User, default=get_default_user, on_delete=models.CASCADE)
    contactNumber = models.CharField(validators=[DefaultUser.phoneNumberRegex], max_length=16, unique=True)
    emailId = models.EmailField(max_length=254)

    def __str__(self) -> str:
        return self.user.username + self.contactNumber

# Question Details
class Question(models.Model):
    student = models.ForeignKey(StudentInfo, default=get_default_student, on_delete=models.CASCADE)
    questionTitle = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    questionText = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.student.user.username + self.subject + self.questionTitle

    def get_absolute_url(self):
        return reverse('question', kwargs={'pk': self.pk})


# Teacher Information
# Added regex validation for phone numbers
# Added email field
class TeacherInfo(models.Model):
	user = models.ForeignKey(User, default=get_default_user, on_delete=models.CASCADE)
	subject = models.CharField(max_length=100)
	qualifications = models.CharField(max_length=100)
	emailId = models.EmailField(max_length=254)
	phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
	contactNumber = models.CharField(validators=[DefaultUser.phoneNumberRegex], max_length=16, unique=True)


# Answer Details
class Answer(models.Model):
    question = models.ForeignKey(Question, default=get_default_question, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherInfo, default=get_default_teacher, on_delete=models.CASCADE)
    answerText = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.teacher.user.username + self.teacher.subject + self.question.questionTitle
