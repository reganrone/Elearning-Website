
from venv import logger
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import DiscussionPostForm, CommentForm
from .models import DiscussionPost, Comment
from teachers.models import Quiz, QuizQuestion, Lesson, Grade, RegisteredUser, Classroom
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import json

# Create your views here.


def students_home(request):
    return render(request, "students/home.html")

def my_classrooms(request):
    # Retrieve the list of classrooms the currently logged-in student is enrolled in
    student = request.user
    enrolled_classrooms = RegisteredUser.objects.filter(user=request.user)

    return render(request, 'students/my_classrooms.html', {'enrolled_classrooms': enrolled_classrooms})


def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    quizzes = Quiz.objects.filter(classroom=classroom)

    student = request.user

    # Fetch grades for the student in the selected classroom
    student_grades = Grade.objects.filter(student=student, quiz__classroom=classroom).select_related('quiz__classroom')

    # Calculate the weighted average grade for the student in this classroom
    total_weighted_grades = 0
    total_weights = 0
    for grade in student_grades:
        weighted_grade = float(grade.grade) * float(grade.quiz.weight)
        total_weighted_grades += weighted_grade
        total_weights += float(grade.quiz.weight)

    weighted_average_grade = total_weighted_grades / total_weights if total_weights > 0 else 0

    # Calculate the letter grade for the weighted average grade
    letter_grade = get_letter_grade(weighted_average_grade)  # Use the get_letter_grade function from before

    return render(request, 'students/classroom_detail.html', {'classroom': classroom, 'quizzes': quizzes, 'letter_grade': letter_grade})

def discussion_posts(request):
    posts = DiscussionPost.objects.all().order_by("-created_at")
    comments_with_posts = Comment.objects.select_related('discussion_post').all()
    return render(request, "students/discussion_posts.html", {"posts": posts, "comments_with_posts": comments_with_posts})

def create_discussion_post(request):
    if request.method == "POST":
        form = DiscussionPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("students:discussion_posts")
    else:
        form = DiscussionPostForm()
    return render(request, "students/create_discussion_post.html", {"form": form})

def discussion_post_detail(request, post_id):
    post = DiscussionPost.objects.get(id=post_id)
    comments = Comment.objects.filter(discussion_post=post)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            discussion_post = get_object_or_404(DiscussionPost, pk=post_id)
            new_comment.discussion_post = discussion_post
            new_comment.save()
            return redirect('students:discussion_post_detail', post_id=post_id)

    return render(request, 'students/discussion_post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'students/lesson_list.html', {'lessons': lessons})

def view_lessons(request):
    lessons = Lesson.objects.all().order_by('-created_at')
    return render(request, 'students/view_lessons.html', {'lessons': lessons})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'students/lesson_detail.html', {'lesson': lesson})

def quizHub(request, classroom_id):
    classroom = Classroom.objects.get(id = classroom_id)
    quizzes = Quiz.objects.filter(classroom=classroom)
    if request.method == 'POST':
        title = request.POST.get('title')
        Quiz.objects.create(
            title = title,
            classroom = classroom,
            author=request.user
        )
        return redirect(reverse('students:quizHub', args=[classroom_id]))
        
    context = {'quizzes': quizzes, 'classroom:': classroom}
    return render(request, "students/quizhub.html", context)

def quiz(request, id):
    quiz = Quiz.objects.get(pk=id)
    context = {"quiz":quiz}
    return render(request, "students/quiz.html", context)

def quizView(request, id):
    quiz = Quiz.objects.get(pk=id)
    questions = QuizQuestion.objects.filter(quiz=quiz)
    grade = None

    if request.method == 'POST':
        total_questions = len(questions)
        total_correct = 0

        for question in questions:
            selected_answer = int(request.POST.get(f"{question.id}"))
            question.selected_answer = selected_answer
            question.save()

            if selected_answer == question.correct_answer:
                total_correct += 1

        # Calculate grade
        total = (total_correct / total_questions) * 100

        # Save the grade
        Grade.objects.create(
            grade = total,
            quiz=quiz, 
            student=request.user
        )

        return redirect(reverse('students:quizResult', args=[id]))

    context = {"questions": questions, "quiz": quiz, "grade": grade}
    return render(request, "students/quizview.html", context)

def quizResult(request, id):
    quiz = Quiz.objects.get(pk=id)
    questions = QuizQuestion.objects.filter(quiz=quiz)
    grade = Grade.objects.filter(quiz=quiz, student=request.user)

    if grade.exists():
        grade = grade.order_by('-id').first()  # Get the most recent grade
        previous_attempts = Grade.objects.filter(quiz=quiz, student=request.user).count()
    else:
        previous_attempts = 0

    context = {"questions": questions, "quiz": quiz, "grade": grade, "previous_attempts": previous_attempts}
    return render(request, "students/quizresult.html", context)


def changeUsername(request, url):
    if request.method == 'POST':
        new_username = request.POST['new_username']
        user = User.objects.get(username=request.user.username)
        try:
            user.username = new_username
            user.save()
            messages.success(request, 'Username changed successfully.')
        except Exception as e:
            messages.error(request, "Username taken")
            
        return redirect(reverse('students:settings', args=[url]))  
    


def changePassword(request, url):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent logging the user out
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Could Not change password, Please Check length')
            return redirect(reverse('students:settings', args=[url]))  
        
def settings(request, url):
    context = {"url":url}
    return render(request, "students/settings.html", context)

from django.shortcuts import render
from teachers.models import Quiz, Grade
from django.db.models import Count, F, FloatField, ExpressionWrapper, Q

def studentPercentile(request):
    quizzes = Quiz.objects.all()
    student = request.user

    quiz_percentiles = []

    for quiz in quizzes:
        grade = Grade.objects.filter(quiz=quiz, student=student).order_by('-grade').first()

        if grade:
            grades_list = Grade.objects.filter(quiz=quiz).exclude(grade__isnull=True).order_by('grade').values_list('grade', flat=True)
            total_grades = len(grades_list)
            max_grade = max(grades_list)
            max_grade_count = sum(1 for grade_value in grades_list if grade_value == max_grade)

            if max_grade_count == 1:
                percentile = (sum(1 for grade_value in grades_list if grade_value < grade.grade) / total_grades) * 100
            else:
                percentile = ((sum(1 for grade_value in grades_list if grade_value <= grade.grade) - 0.5 * max_grade_count) / total_grades) * 100

            student_percentile = round(percentile, 2)
        else:
            student_percentile = None

        quiz_percentiles.append({'quiz': quiz, 'student_percentile': student_percentile})

        
    context = {'quiz_percentiles': quiz_percentiles}
    return render(request, 'students/student_percentile.html', context)

import json
from django.http import JsonResponse

def grades_chart(request):
    student = request.user  # Fetch student ID from request
    labels = []
    data = []

    # Retrieve the student's grades for each classroom
    student_grades = Grade.objects.filter(student=student).select_related('quiz__classroom')

    # Organize grades by classroom
    classroom_grades = {}
    for grade in student_grades:
        classroom_name = grade.quiz.classroom.name
        if classroom_name not in classroom_grades:
            classroom_grades[classroom_name] = []

        classroom_grades[classroom_name].append(float(grade.grade))

    # Prepare data for the bar chart
    labels = list(classroom_grades.keys())
    data = [sum(grades) / len(grades) for grades in classroom_grades.values()]

    # Return data as JSON response
    return JsonResponse(data={'labels': labels, 'data': data})

def student_quiz_grades(request):
    return render(request, 'students/student_quiz_grades.html')


def get_letter_grade(average_grade):
    # Define your grading scale criteria
    if average_grade >= 90:
        return 'A'
    elif average_grade >= 80:
        return 'B'
    elif average_grade >= 70:
        return 'C'
    elif average_grade >= 60:
        return 'D'
    else:
        return 'F'

