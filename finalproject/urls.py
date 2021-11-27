# pages/urls.py
from django.urls import path
from .views import HomePage, StudentRegisteration, PostQuestion, StudentLogin, StudentPortal, TeacherRegisteration, TeacherLogin, TeacherPortal, QuestionDetail, SubmitAnswer, AnswerDetail

urlpatterns = [
    path("", HomePage, name="homepage"),
    path("register", StudentRegisteration, name="studentregisteration"),
    path("login", StudentLogin, name="studentlogin"),
    path("portal", StudentPortal.as_view(), name="studentportal"),
    path("postquestion", PostQuestion, name="postquestion"),
    path('<int:pk>/answer/viewdetail/', AnswerDetail, name='answerDetail'),
    path("teacherregister", TeacherRegisteration, name="teacherregisteration"),
    path("teacherlogin", TeacherLogin, name="teacherlogin"),
    path("teacherportal", TeacherPortal.as_view(), name="teacherportal"),
    path('<int:pk>/answer/', QuestionDetail.as_view(), name='question'),
    path('<int:pk>/answer/submit', SubmitAnswer, name='answer'),
]
