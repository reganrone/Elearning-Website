import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    def __str__(self):
        return self.title
    
class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.IntegerField()  # 1 for option 1, 2 for option 2, and so on
    attempts_remaining = models.PositiveIntegerField(default=3)
    attempts_taken = models.PositiveIntegerField(default=0)
    selected_answer = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.question_text

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.CharField(
        choices=[('text', 'Text'), ('video', 'Video')],
        max_length=10,
        default='text'
    )
    content = models.TextField()  # For text content or video URL
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RegisteredUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

