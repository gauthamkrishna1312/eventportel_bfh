from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, fields
from django import forms
from . import models


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DatePicker(forms.DateInput):
    input_type = 'date'

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = models.EventDetails
        fields = ['title', 'description', 'eventdate', 'location', 'lastdatetoreg', 'maxparticipants']
        widgets = {
            'eventdate':DatePicker(),
            'lastdatetoreg':DatePicker(),
        }