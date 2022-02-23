from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
class ProfilePicForm(forms.Form):
    profile_pic = forms.ImageField()
    