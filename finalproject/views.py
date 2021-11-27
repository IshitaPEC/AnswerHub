from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from finalproject.models import StudentInfo, Question, TeacherInfo, Answer
from .forms import UserForm
from django.urls import reverse
from django.contrib.auth import authenticate
from django.views.generic import ListView, DetailView
from django.contrib.auth import login as auth_login


# Home Page
def HomePage(request):
    return render(request, 'homePage.html')


# Student Registeration
def StudentRegisteration(request):
    # Form Class with username and password details of the user
    form_class = UserForm
    form = form_class(request.POST)
    user = None

    if request.method == 'POST':
        form = UserForm(data=request.POST)
        # checks for implicit errors
        if form.is_valid():
            user = form.save()
            # hash the password
            user.set_password(user.password)
            # save
            user.save()
            contactNumber = request.POST.get('contactNumber')
            emailId = request.POST.get('emailId')
            student = StudentInfo.objects.create(contactNumber=contactNumber, emailId=emailId, user=user)
            student.save()
        return HttpResponseRedirect(reverse('studentlogin'))

    return render(request, 'studentregisteration.html',  {'user_form': form})


# Student Login
def StudentLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        # We are using the inbuilt django function of authentication
        user = authenticate(username=uname, password=passw)
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('studentportal'))
            else:
                return HttpResponse("User is inactive")
        else:
            return render(request, 'studentlogin.html', {'err': 'Invalid User Credentials!'})

    else:
        return render(request, 'studentlogin.html')


# List of all questions that have been asked by the student with answers from teachers
class StudentPortal(ListView):
    model = Question
    context_object_name = 'studentQuestions'
    template_name = 'studentportal.html'

    def get_queryset(self):
        user = self.request.user
        student = StudentInfo.objects.get(user=user)
        queryset = super(StudentPortal, self).get_queryset()
        queryset = queryset.filter(student=student)
        return queryset


# View to ask a new Question
def PostQuestion(request):
    user = request.user
    student = StudentInfo.objects.get(user=user)
    if request.method == 'POST':
        subject = request.POST.get('subject')
        questionTitle = request.POST.get('questionTitle')
        questionText = request.POST.get('questionText')
        question = Question.objects.create(student=student, subject=subject, questionTitle=questionTitle, questionText=questionText)
        question.save()
        return render(request, 'postquestion.html', {'details': 'Thank you for your question'})
    else:
        return render(request, 'postquestion.html')


# Displays answers for every question asked previously by the user
def AnswerDetail(request, pk):
    question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question=question)
    return render(request, 'studentanswers.html', {'answers': answers})


# Teacher Registeration
def TeacherRegisteration(request):
    form_class = UserForm
    form = form_class(request.POST)
    user = None
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        # checks for implicit errors
        if form.is_valid():
            user = form.save()
            # hash the password
            user.set_password(user.password)
            # save
            user.save()
            contactNumber = request.POST.get('contactNumber')
            emailId = request.POST.get('emailId')
            qualifications = request.POST.get('qualifications')
            subject = request.POST.get('subject')
            teacher = TeacherInfo.objects.create(user=user, contactNumber=contactNumber, subject=subject, emailId=emailId, qualifications=qualifications)
            teacher.save()

        return HttpResponseRedirect(reverse('teacherlogin'))
    return render(request, 'teacherregisteration.html', {'user_form': form})


# Teacher Login
def TeacherLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(username=uname, password=passw)
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('teacherportal'))
            else:
                return HttpResponse("User is inactive")
        else:
            return render(request, 'teacherlogin.html', {'err': 'Invalid User Credentials!'})

    else:
        return render(request, 'teacherlogin.html')


# List of all questions asked by different students in the subject chosen by the teacher
class TeacherPortal(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'teacherportal.html'

    def get_queryset(self):
        user = self.request.user
        teacher = TeacherInfo.objects.get(user=user)
        queryset = super(TeacherPortal, self).get_queryset()
        queryset = queryset.filter(subject=teacher.subject)
        return queryset


# Details of the Question asked by the student, which the teacher intends answering
class QuestionDetail(DetailView):
    model = Question
    context_object_name = 'question_detail'
    template_name = 'question.html'


# Displays form to answer the question
def SubmitAnswer(request, pk):
    user = request.user
    teacher = TeacherInfo.objects.get(user=user)
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        answerText = request.POST.get('answerText')
        ans = Answer.objects.create(teacher=teacher, question=question, answerText=answerText)
        ans.save()
        return render(request, 'answer.html', {'details': 'Thank you for your answer'})
    else:
        return render(request, 'answer.html')
