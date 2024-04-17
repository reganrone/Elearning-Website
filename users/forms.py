from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class AuthenticationFormWithRole(AuthenticationForm):
    role = forms.ChoiceField(
        choices=(('teacher', 'Teacher'), ('student', 'Student')),
        widget=forms.RadioSelect,
    )

class CustomUserForm(forms.ModelForm):
    class meta:
        model = CustomUser
        fields = ['is_teacher']