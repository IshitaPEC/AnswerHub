from django.test import TestCase
from finalproject.models import StudentInfo, Question, TeacherInfo, Answer
from django.contrib.auth.models import User

# Create your tests here.
# test_models.py

class StudentInfoModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
    	user = User.objects.create(username="User1", password="password")
    	StudentInfo.objects.create(user=user, contactNumber="1111111111", emailId="samplemail@domain.com")

    def test_string_method(self):
    	student = StudentInfo.objects.get(id=1)
    	expected_string = student.user.username + student.contactNumber
    	self.assertEqual(str(student), expected_string)


class QuestionModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
    	user = User.objects.create(username="User1", password="password")
    	student = StudentInfo.objects.create(user=user, contactNumber="1111111111", emailId="samplemail@domain.com")
    	Question.objects.create(student=student, questionTitle="Sample Title", subject="Cloud Computing", questionText="Question 1 Detailed Answers")

    def test_string_method(self):
    	question = Question.objects.get(id=1)
    	expected_string = question.student.user.username + question.subject + question.questionTitle
    	self.assertEqual(str(question), expected_string)

    def test_get_absolute_url(self):
    	question = Question.objects.get(id=1)
    	self.assertEqual(question.get_absolute_url(), "/1/answer/")


class TeacherInfoModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
    	user = User.objects.create(username="User1", password="password")
    	TeacherInfo.objects.create(user=user, subject="Cloud Computing", qualifications="BTECH", emailId="samplemail@domain.com", contactNumber="1111111111")


class AnswerModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
    	user = User.objects.create(username="User1", password="password")
    	student = StudentInfo.objects.create(user=user, contactNumber="1111111111", emailId="samplemail@domain.com")
    	question = Question.objects.create(student=student, questionTitle="Sample Title", subject="Cloud Computing", questionText="Question 1 Detailed Answers")
    	teacheruser = User.objects.create(username="User2", password="password2")
    	teacher = TeacherInfo.objects.create(user=teacheruser, subject="Cloud Computing", qualifications="BTECH", emailId="samplemail@domain.com", contactNumber="1111111111")
    	Answer.objects.create(question=question, teacher=teacher, answerText="Answer")

    def test_string_method(self):
    	answer = Answer.objects.get(id=1)
    	expected_string = answer.teacher.user.username + answer.teacher.subject + answer.question.questionTitle
    	self.assertEqual(str(answer), expected_string)
