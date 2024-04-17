from django.contrib import admin
from .models import Quiz, QuizQuestion, Lesson, Classroom, RegisteredUser, Grade


admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(Lesson)
admin.site.register(Classroom)
admin.site.register(RegisteredUser)
admin.site.register(Grade)

