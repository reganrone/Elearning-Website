from django import forms
from .models import DiscussionPost, Comment

class DiscussionPostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ["title", "content", "file_upload"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']




