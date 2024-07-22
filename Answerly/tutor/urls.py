from django.contrib import admin
from django.urls import path
from .views import createTutor, findTutor, createMessage, displayMessages

app_name = 'tutor'
urlpatterns = [
    path('create/', createTutor, name = 'create-tutor'),
    path('find/', findTutor, name='find-tutor'),
    path('create-message/', createMessage, name='create-message'),
    path('display-messages/<str:pk>', displayMessages, name ='display-messages')
   
]

