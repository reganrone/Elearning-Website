from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.teachers_home, name="home"),
    path('create_classroom/', views.create_classroom, name='create_classroom'),
    path('view_classrooms/', views.view_classrooms, name='view_classrooms'),
    path('classroom/<uuid:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('create_quiz/<uuid:classroom_id>/', views.create_quiz, name='create_quiz'),
    path('record_grade/', views.record_grade, name='record_grade'),
    path('view_grades/', views.view_grades, name='view_grades'),
    path('list_quizzes/', views.list_quizzes, name='list_quizzes'),
    path('quiz_detail/<str:id>/', views.quiz_detail_view, name='quiz_detail'),
    path('lessons/create/<uuid:classroom_id>/', views.create_lesson, name='create_lesson'),
    path('view_quiz_details/<str:grade_id>/', views.view_quiz_details, name='view_quiz_details'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('quiz/<uuid:quiz_id>/summary/', views.score_summary, name='score_summary'),
    path('student/<int:student_id>/', views.student_average_grades, name='student_average_grades'),
    path('quiz/update_weight/<uuid:quiz_id>/', views.update_quiz_weight, name='update_quiz_weight'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('letter_grades/', views.letter_grades, name='letter_grades'),

    
]

    # Other URL patterns for your app

