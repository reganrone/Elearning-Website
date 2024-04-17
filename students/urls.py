from django.urls import path, re_path
from . import views

app_name = "students"

urlpatterns = [
    # Define a URL pattern for the teacher homepage
    path("", views.students_home, name="home"),
    path('my_classrooms/', views.my_classrooms, name='my_classrooms'),
    path('students/classroom_detail/<uuid:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path("discussion/", views.discussion_posts, name="discussion_posts"),
    path("discussion/create/",views.create_discussion_post,name="create_discussion_post",),
    path('discussion/<int:post_id>/', views.discussion_post_detail, name='discussion_post_detail'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/', views.view_lessons, name='view_lessons'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path("quiz_hub/<uuid:classroom_id>/", views.quizHub, name="quizHub"),
    path("quiz/<str:id>/", views.quiz, name="quiz"),
    path("quiz_view/<str:id>/", views.quizView, name="quizView"),
    path('quiz_result/<str:id>/', views.quizResult, name='quizResult'),
    path('student_percentile/', views.studentPercentile, name='studentPercentile'),
    path('grades-chart/', views.grades_chart, name='grades-chart'),
    path('student_quiz_grades/', views.student_quiz_grades, name='student_quiz_grades'),
    re_path(r'^settings/(?P<url>.+)/$', views.settings, name='settings'),
    re_path(r'^change_username/(?P<url>.+)/$', views.changeUsername, name='changeUsername'),
    re_path(r'^change_password/settings/(?P<url>.+)/$', views.changePassword, name='changePassword'),
    
]
# Other URL patterns for your app
