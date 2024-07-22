from django.forms import ModelForm
from .models import Question, Event, Profile
from django import forms
from django.contrib.auth.models import User


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ['author', 'participants', 'created']


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }
        exclude = ['host']

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ImageUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

