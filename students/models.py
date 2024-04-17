from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from teachers.models import Lesson, Quiz, QuizQuestion

class DiscussionPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    file_upload = models.FileField(upload_to='uploads/', default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    discussion_post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE,  related_name='comments')

    def __str__(self):
        return self.content
    




