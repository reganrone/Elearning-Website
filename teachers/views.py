from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from django.urls import reverse

from students.views import quiz
from .models import Quiz, Grade, QuizQuestion, Lesson, Classroom, RegisteredUser, Student
from .forms import QuizForm, GradeForm, QuizQuestionForm, LessonForm,ClassroomForm, EnrollForm, StudentForm, SearchForm
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import FloatField
from django.db.models.functions import Cast
from collections import Counter

# Create your views here.

def teachers_home(request):
    return render(request, "teachers/home.html")

def create_classroom(request,):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user  # Associate the classroom with the current teacher
            classroom.save()
            return redirect('teachers:view_classrooms')  # Redirect to the list of classrooms
    else:
        form = ClassroomForm()
    
    return render(request, 'teachers/create_classroom.html', {'form': form})

def view_classrooms(request):
    classrooms = Classroom.objects.all()

    return render(request, 'teachers/view_classrooms.html', {'classrooms': classrooms})

def classroom_detail(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)

    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            # Get the selected users and enroll them in the classroom
            selected_users = form.cleaned_data['enrolled_users']
            for user in selected_users:
                RegisteredUser.objects.create(user=user, course=classroom)
            return redirect('teachers:view_classrooms')

    else:
        # Display the form to add students
        # Customize the queryset to exclude already enrolled users
        enrolled_users = RegisteredUser.objects.filter(course=classroom).values('user')
        form = EnrollForm(initial={'enrolled_users': User.objects.exclude(id__in=enrolled_users)})

    return render(request, 'teachers/classroom_detail.html', {'classroom': classroom, 'form': form})

def create_quiz(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)

    # Define the formset using inlineformset_factory
    QuizQuestionFormSet = inlineformset_factory(Quiz, QuizQuestion, fields=['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_answer'], extra=5)

    if request.method == "POST":
        form = QuizForm(request.POST)
        question_formset = QuizQuestionFormSet(request.POST)

        if form.is_valid() and question_formset.is_valid():
            quiz = form.save(commit=False)
            quiz.classroom = classroom
            quiz.save()

            for question_form in question_formset:
                question = question_form.save(commit=False)
                question.quiz = quiz
                question.save()

            return redirect('teachers:list_quizzes')
    else:
        form = QuizForm()
        question_formset = QuizQuestionFormSet()

    return render(request, 'teachers/create_quiz.html', {'form': form, 'question_formset': question_formset, 'classroom': classroom})

def record_grade(request):
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachers:view_grades')
    else:
        form = GradeForm()
    
    return render(request, 'teachers/record_grade.html', {'form': form})

def view_grades(request):
    form = SearchForm(request.GET)
    grades = Grade.objects.select_related('quiz__classroom').order_by('quiz__classroom__name', 'student__username')

    if form.is_valid():
        username = form.cleaned_data.get('keyword')
        if username:
            grades = grades.filter(student__username__icontains=username)

    sort_by = request.GET.get('sort', None)

    if sort_by == 'asc':
       grades = Grade.objects.all().order_by('grade')
    elif sort_by == 'desc':
        grades = Grade.objects.all().order_by('-grade')
        
    grouped_grades = {}
    current_classroom = None

    for grade in grades:
        if grade.quiz.classroom != current_classroom:
            current_classroom = grade.quiz.classroom
            grouped_grades[current_classroom] = []

        grouped_grades[current_classroom].append(grade)

    return render(request, 'teachers/view_grades.html', {'grouped_grades': grouped_grades, 'form': form})

from django.db.models import Max, Min, Avg

def score_summary(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    
    highest = Grade.objects.filter(quiz=quiz).aggregate(Max('grade'))
    lowest = Grade.objects.filter(quiz=quiz).aggregate(Min('grade'))
    average = Grade.objects.filter(quiz=quiz).aggregate(Avg('grade'))

    context = {
        'quiz': quiz,
        'highest': highest['grade__max'],
        'lowest': lowest['grade__min'],
        'average': average['grade__avg'],
    }
    return render(request, 'teachers/score_summary.html', context)


def view_quiz_details(request, grade_id):
    try:
        grade = Grade.objects.select_related('quiz__classroom').get(pk=grade_id)
        questions = QuizQuestion.objects.filter(quiz=grade.quiz)
    except Grade.DoesNotExist:
        # Handle the case where the grade doesn't exist
        pass

    attempt_number = Grade.objects.filter(quiz=grade.quiz, student=grade.student, id__lte=grade.id).count()

    return render(request, 'teachers/view_quiz_details.html', {'grade': grade, 'questions': questions, 'attempt_number': attempt_number})

def list_quizzes(request):
    quizzes = Quiz.objects.all()
    return render(request, 'teachers/list_quizzes.html', {'quizzes': quizzes})

def quiz_detail_view(request, id):
    quiz = Quiz.objects.get(pk=id)
    questions = QuizQuestion.objects.filter(quiz=quiz)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_answer = request.POST.get('correct_answer')

    
    context = {"quiz":quiz, "questions":questions}
    return render(request, "teachers/quiz_detail.html", context)

def create_lesson(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)  # Get the classroom object based on classroom_id
    form = LessonForm()
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.classroom = classroom
            lesson.author = request.user
            lesson.save()
            return redirect('teachers:home')
        else:
            form = LessonForm()
            classrooms = Classroom.objects.all()
    return render(request, 'teachers/create_lesson.html', {'form': form, 'classroom': classroom})

from django.shortcuts import render, get_object_or_404
from .models import Grade, Classroom, Quiz
from django.db.models import Avg

def student_average_grades(request, student_id):
    student = get_object_or_404(User, id=student_id)

    # Fetch grades for the student, including related quiz and classroom
    student_grades = Grade.objects.filter(student=student).select_related('quiz__classroom')

    # Calculate weighted average grades per classroom
    average_grades = {}
    for grade in student_grades:
        classroom_name = grade.quiz.classroom.name
        if classroom_name not in average_grades:
            average_grades[classroom_name] = {'total_weighted_grades': 0, 'total_weights': 0}

        weighted_grade = float(grade.grade) * float(grade.quiz.weight)
        average_grades[classroom_name]['total_weighted_grades'] += weighted_grade
        average_grades[classroom_name]['total_weights'] += float(grade.quiz.weight)

    for classroom, values in average_grades.items():
        if values['total_weights'] > 0:
            values['weighted_average_grade'] = values['total_weighted_grades'] / values['total_weights']
            values['letter_grade'] = get_letter_grade(values['weighted_average_grade'])
        else:
            values['weighted_average_grade'] = 0
            values['letter_grade'] = 'N/A'  # Not applicable if no grades

    return render(request, 'teachers/student_average_grades.html', {'student': student, 'average_grades': average_grades})

from django.http import HttpResponseRedirect, JsonResponse
from decimal import Decimal

def update_quiz_weight(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        new_weight = request.POST.get('quiz_weight')
        quiz.weight = Decimal(new_weight)  # Convert to Decimal explicitly
        quiz.save()
        # Redirect back to the quiz details page or any other page
        return HttpResponseRedirect('/teachers/list_quizzes/')  # Redirect to appropriate URL

    return render(request, 'teachers/quiz_detail.html', {'quiz': quiz})

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
    
def pie_chart(request):
    # Fetch all students
    all_students = User.objects.all()  # Assuming is_teacher is a flag distinguishing teachers from students

    # Calculate letter grade distribution for all students
    student_letter_grades = {}
    for student in all_students:
        student_grades = Grade.objects.filter(student=student).select_related('quiz__classroom')
        grades_counter = Counter()
        for grade in student_grades:
            weighted_grade = float(grade.grade) * float(grade.quiz.weight)
            letter_grade = get_letter_grade(weighted_grade)
            grades_counter[letter_grade] += 1
        student_letter_grades[student.id] = dict(grades_counter)

    # Aggregate letter grade data for all students
    letter_grades_data = Counter()
    for grades in student_letter_grades.values():
        letter_grades_data += Counter(grades)

    labels = list(letter_grades_data.keys())
    data = list(letter_grades_data.values())

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def letter_grades(request):
    return render(request, "teachers/letter_grades.html")



