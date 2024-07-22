from django.contrib import admin
from django.urls import path

from .views import (home, createQuestion, updateQuestion, deleteQuestion, 
registerUser, logoutUser, loginUser, createEvent, updateEvent, deleteEvent, listEvents, question, event, userProfile, profile)


app_name = 'questions'
urlpatterns = [
    path('', home, name='home'),
    path('register/', registerUser, name = 'register'),
    path('profile/<str:pk>', userProfile, name = 'profile'),
    path('logout/', logoutUser, name = 'logout'),
    path('login/', loginUser, name = 'login'),

    
    path('create-question/', createQuestion, name='create-question' ),
    path('update-question/<str:pk>', updateQuestion, name='update-question' ),
    path('delete-question/<str:pk>', deleteQuestion, name='delete-question' ),
    path('create-event/', createEvent, name = 'create-event'),
    path('update-event/<str:pk>', updateEvent, name = 'update-event'),
    path('delete-event/<str:pk>', deleteEvent, name = 'delete-event'),
    path('event-list/', listEvents, name='list-events'),
    #path('question-list/', listQuestions, name='list-questions'),
    path('question/<str:pk>', question, name = 'question'),
    path('event/<str:pk>', event, name = 'event'),
    path('profile-update/', profile, name='update-profile')
] 