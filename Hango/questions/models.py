from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#from django.utils.timezone import utc
#from datetime import timezone
# Create your models here.




class Question(models.Model):
    class Subject(models.TextChoices):
        MATH = 'Math'
        SCIENCE = 'Science'
        SOCIAL_STUDIES = 'Social Studies'
        ELA = 'Ela'

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=20, choices = Subject.choices, null=False, blank=False )
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='default.jpg', upload_to='question_images', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:30]

class Event(models.Model):
    title = models.CharField(max_length=200)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    location = models.CharField(max_length=200)


    def __str__(self):
        return self.title

class EventResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    attending = models.BooleanField(null=True, blank=True)
    notattending = models.BooleanField(null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    

