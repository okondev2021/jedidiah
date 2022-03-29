from django.db import models
from django.forms import fields
from .models import Create
from django import forms

class UserImage(forms.ModelForm):
    class meta:
        fields = '__all__'