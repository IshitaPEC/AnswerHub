from django.contrib import admin
from .models import Question, StudentInfo, TeacherInfo, Answer


admin.site.register(Question)
admin.site.register(StudentInfo)
admin.site.register(TeacherInfo)
admin.site.register(Answer)