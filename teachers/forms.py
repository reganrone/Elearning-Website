from django import forms
from django.contrib.auth.models import User
from .models import Classroom, Student, Quiz, Grade, QuizQuestion, Lesson
from django.forms import formset_factory

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, label='Search')


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'description']

class EnrollForm(forms.Form):
    enrolled_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']
        widgets = {
            'classroom': forms.HiddenInput(),
        }
from django import forms

from django import forms
from .models import Quiz, QuizQuestion

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']  # Include title and description fields

    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), label="Select Classroom")

QuizFormSet = formset_factory(QuizForm, extra=3)  

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_answer']
    
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'quiz', 'grade']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content_type', 'content', 'classroom']

    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), label="Select Classroom")
