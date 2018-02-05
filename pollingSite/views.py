from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.crypto import get_random_string
from datetime import datetime
import uuid
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login as authLogin

from .models import *
from .forms import *

def classroomSecureWrapper(function):
    def decorator(request, *args, **kwargs):
        classroom = Classroom.objects.get(pk=kwargs['classroom'])
        if classroom.instructor == request.user:
            return function(request, *args, **kwargs)
        else:
            raise Http404
    return decorator

@login_required
def index(request):
    classroom = Classroom.objects.filter(instructor=request.user)
    return render(request, 'pollingSite/index.html', locals())

@login_required
def changePassword(request):
    return render(request, 'pollingSite/changePassword.html', locals())

@login_required
def search(request):
    return render(request, 'pollingSite/search.html', locals())

@login_required
def addClass(request):
    if request.method == 'POST':
        form = createClassForm(request.POST)
        if form.is_valid():
            Classroom.objects.create(className=form.cleaned_data['class_name'], classNumber=form.cleaned_data['class_id'], instructor=request.user)
            return index(request);
    else:
        form = createClassForm()
        return render(request, 'pollingSite/addClass.html', locals())

@login_required
@classroomSecureWrapper
def classroom(request, classroom):
    polls = Poll.objects.filter(classroom=classroom)
    curClass = classroom
    return render(request, 'pollingSite/pollList.html', locals())

@login_required
@classroomSecureWrapper
def attendance(request, classroom):
    return render(request, 'pollingSite/attendance.html', locals())

@login_required
@classroomSecureWrapper
def pollList(request, classroom):
    polls = Poll.objects.filter(classroom=classroom)
    curClass = classroom
    return render(request, 'pollingSite/pollList.html', locals())

@login_required
@classroomSecureWrapper
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

@login_required
@classroomSecureWrapper
def activePoll(request, poll, classroom):
    poll = Poll.objects.get(id=poll)
    options = range(1, poll.options + 1)
    return render(request, 'pollingSite/activePoll.html', locals())
