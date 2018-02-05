from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.crypto import get_random_string
from datetime import datetime
import uuid


from .models import *
from .forms import *

def landing(request):
    if request.user.is_anonymous:
        return redirect('pollingSite:login')
    else:
        return redirect('pollingSite:index')

def index(request):
    classroom = Classroom.objects.filter(instructor=request.user)
    return render(request, 'pollingSite/index.html', locals())

def login(request):
    return render(request, 'pollingSite/login.html', locals())

def changePassword(request):
    return render(request, 'pollingSite/changePassword.html', locals())

def search(request):
    return render(request, 'pollingSite/search.html', locals())

def addClass(request):
    if request.method == 'POST':
        form = createClassForm(request.POST)
        if form.is_valid():
            Classroom.objects.create(className=form.cleaned_data['class_name'], classNumber=form.cleaned_data['class_id'], instructor=request.user)
            return index(request);
    else:
        form = createClassForm()
        return render(request, 'pollingSite/addClass.html', locals())

def classroom(request, classroom):
    polls = Poll.objects.filter(classroom=classroom)
    curClass = classroom
    return render(request, 'pollingSite/pollList.html', locals())

def attendance(request, classroom):
    return render(request, 'pollingSite/attendance.html', locals())

def pollList(request, classroom):
    polls = Poll.objects.filter(classroom=classroom)
    curClass = classroom
    return render(request, 'pollingSite/pollList.html', locals())

def createPoll(request, classroom):
    curClass1 = classroom
    if request.method == 'POST':
        form = createPollForm(request.POST)
        if form.is_valid():
            Poll.objects.create(classroom = Classroom.objects.get(pk=classroom), name=form.cleaned_data['new_poll_name'], options=form.cleaned_data['possible_answers'], correct=form.cleaned_data['correct_answer'], startTime = datetime.now(), stopTime = datetime.now())
            return redirect('pollingSite:pollList', curClass1)
    else:
        form = createPollForm()
        return render(request, 'pollingSite/createPoll.html', locals())

def activePoll(request, classroom, poll):
    poll = Poll.objects.get(id=poll)
    options = range(1, poll.options + 1)
    return render(request, 'pollingSite/activePoll.html', locals())
