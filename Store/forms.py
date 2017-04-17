import json
from django.views.generic import FormView
from django.forms import forms, models
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.forms import PasswordChangeForm
from django.forms.models import modelform_factory

from .models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('website', 'picture')



