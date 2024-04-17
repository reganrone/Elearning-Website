from django.contrib import admin
from students.models import DiscussionPost, Comment

# Register your models here.
admin.site.register(DiscussionPost)
admin.site.register(Comment)