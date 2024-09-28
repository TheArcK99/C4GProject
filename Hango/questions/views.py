from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Event, Response, EventResponse
from .forms import QuestionForm, EventForm, UserUpdateForm, ImageUpdateForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request, 'questions/home.html')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        i_form = ImageUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and i_form.is_valid():
            u_form.save()
            i_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('questions:home')
    else:
        u_form = UserUpdateForm(instance=request.user)
        i_form = ImageUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'i_form': i_form
    }

    return render(request, 'questions/update_profile.html', context)



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    questions = user.question_set.all()
    events = user.event_set.all()
    questionResponses = user.response_set.all()
    eventResponses = user.eventresponse_set.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q == 'questions':
        context = {
            'user': user,
            'questions': questions,
            'events': events,
            'responses': questionResponses,
            'eresponses': eventResponses,
            'type': 'questions'
        }
        return render(request, 'questions/profile.html', context)
    elif q == 'events':
        context = {
            'user': user,
            'questions': questions,
            'events': events,
            'responses': questionResponses,
            'eresponses': eventResponses,
            'type': 'events'
        }
        return render(request, 'questions/profile.html', context)
    else:
        context = {
            'user': user,
            'questions': questions,
            'events': events,
            'responses': questionResponses,
            'eresponses': eventResponses,
        }
        return render(request, 'questions/profile.html', context)
"""
def listQuestions(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    questions = Question.objects.filter(
        Q(subject__icontains = q) |
        Q(title__icontains = q) |
        Q(description__icontains = q)
        ).order_by('-created')

    count = Question.objects.count()
    responses = Response.objects.filter(Q(question__subject__icontains = q))

    context = {
        'questions': questions,
        'questions_count': count,
        'responses': responses
    }

    return render(request, 'questions/questions_list.html', context)"""

def listEvents(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    e = request.GET.get('e') if request.GET.get('e') != None else ''
    count = Event.objects.count()
    responses = EventResponse.objects.filter(attending = True)

    
    if q == 'newest':
        events = Event.objects.filter(
            Q(title__icontains = e) |
            Q(description__icontains = e)
        ).order_by('-date')


        context = {
            'events': events,
            'event_count': count,
            'eresponses': responses
        }

        return render(request, 'questions/events_list.html', context)
    else:
        events = Event.objects.filter(
            Q(title__icontains = e) |
            Q(description__icontains = e)
        ).order_by('-date')
        context = {
            'events': events,
            'event_count': count,
            'eresponses': responses
        }

        return render(request, 'questions/events_list.html', context)



def question(request, pk):
    question = Question.objects.get(id = pk)
    question_responses = question.response_set.all().order_by('created')
    participants = question.participants.all()

    if request.method == 'POST':
        response = Response.objects.create(
            user = request.user,
            question = question,
            body = request.POST.get('response'),
        )
        question.participants.add(request.user)
        return redirect('questions:question', question.id)


    return render(request, 'questions/question.html', {'question': question, 'responses': question_responses, 'participants': participants})


def event(request, pk):
    event = Event.objects.get(id = pk)
    responses = EventResponse.objects.filter(event = event)
    attendees = responses.filter(attending = True)

    if request.method == 'POST':
        if EventResponse.objects.filter(user=request.user, event = event).exists():
            messages.error(request, 'You already submitted a response!')
            return redirect('questions:event', event.id)
            
        else:
            eventresponse = EventResponse.objects.create(
                user = request.user,
                event = event,
                attending = request.POST.get('attending'),
                notattending = request.POST.get('notattending')
            )
        return redirect('questions:event', event.id)

    return render(request, 'questions/event.html', {'event': event, 'attendees': attendees})



@login_required(login_url='questions:login')
def createQuestion(request):
    form = QuestionForm()


    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit = False)
            question.author = request.user
            question.save()

            return redirect('questions:list-questions')

    context = {
        'form' : form,

    }


    return render(request, 'questions/create_question.html', context)

@login_required(login_url="questions:login")
def updateQuestion(request, pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance = question)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance = question)
        if form.is_valid():
            form.save()
            return redirect('questions:list-questions')

    context = {
        'form': form
    }

    return render(request, 'questions/create_question.html', context)

@login_required(login_url="questions:login")
def deleteQuestion(request, pk):
    question = Question.objects.get(id=pk)

    if request.method == 'POST':
        question.delete()
        return redirect('questions:list-questions')
    
    context = {
        'question': question
    }

    return render(request, 'questions/delete_question.html', context)

@login_required(login_url='questions:login')
def createEvent(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            return redirect('questions:list-events')

    context = {
        'form' : form
    }

    return render(request, 'questions/create_event.html', context)


def updateEvent(request, pk):
    event = Event.objects.get(id = pk)
    form = EventForm(instance = event)


    if request.method == 'POST':
        form = EventForm(request.POST, instance = event)
        if form.is_valid():
            form.save()
            return redirect('questions:list-events')
    
    context = {
        'form': form
    }

    return render(request, 'questions/create_event.html', context)


def deleteEvent(request, pk):
    event = Event.objects.get(id = pk)
    if request.method == 'POST':
        event.delete()
        return redirect('questions:list-events')
    
    context = {
        'event': event
    }

    return render(request, 'questions/delete_event.html', context)



def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('questions:home')
        else:
            messages.error(request, 'An error occured when logging in!')

    context = {
        'form': form,
        'page': 'register'
    }    

    return render(request, 'questions/login_register.html', context)

def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('questions:home')

    return render(request, 'questions/logout.html')

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('questions:home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username) 
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('questions:home')
        else:
            messages.error(request, "User name or password does not exist")


    
    return render(request, 'questions/login_register.html')




