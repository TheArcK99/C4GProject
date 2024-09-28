from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tutor(models.Model):
    class Subject(models.TextChoices):
        MATH = 'Math'
        SCIENCE = 'Science'
        SOCIAL_STUDIES = 'Social Studies'
        ELA = 'Ela'

    class Levels(models.TextChoices):
        ELEMENTARY = 'Elementary'
        MIDDLE = 'Middle'
        HIGH = 'High'
        COLLEGE = 'College'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    bio = models.TextField()
    subject = models.CharField(max_length=20, choices = Subject.choices, null=False, blank=False)
    level = models.CharField(max_length=20, choices = Levels.choices, null=False, blank=False)
    email = models.EmailField(max_length=100)

class Message(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=100)
