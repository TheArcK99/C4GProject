from django.shortcuts import render, redirect
from .forms import TutorForm, MessageForm
from django.http import HttpResponseRedirect
from .models import Tutor, Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
# Create your views here.

@login_required(login_url='questions:login')
def createTutor(request):
    form = TutorForm()


    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('questions:home'))
        
    context = {
        'form': form
    }
        
    return render(request, 'tutor/tutor_signup.html', context)


@login_required(login_url='questions:login')
def findTutor(request):
    if request.method == 'POST':
        course = request.POST.get('subject')
        lvl = request.POST.get('level')

        tutors = Tutor.objects.all()
        potential_tutors = tutors.filter(subject = course)
        tutor = potential_tutors.filter(level = lvl)

        context = {
            'type': 'tutor',
            'tutors': tutor
        }

        return render(request, 'tutor/find_tutor.html', context)

        
    context = {
        'type': 'search'
    }
    return render(request, 'tutor/find_tutor.html', context)



@login_required(login_url='questions:login')
def createMessage(request):
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.sender = request.user.username
            form.save()

            return HttpResponseRedirect(reverse('questions:home'))
        
    context = {
        'form': form
    }
    return render(request, 'tutor/create_message.html', context)


def displayMessages(request, pk):
    messages = Message.objects.all()

    context = {
        'messages': messages.filter(recipient=request.user).order_by('-sent')
    }

    return render(request, 'tutor/list_messages.html', context)