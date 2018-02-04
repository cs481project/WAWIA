from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login as authLogin
from django.http import HttpResponse, Http404

from .models import *

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
    return render(request, 'pollingSite/addClass.html', locals())

@login_required
@classroomSecureWrapper
def classroom(request, classroom):
    polls = Poll.objects.filter(classroom=classroom)
    return render(request, 'pollingSite/pollList.html', locals())

@login_required
@classroomSecureWrapper
def attendance(request, classroom):
    return render(request, 'pollingSite/attendance.html', locals())

@login_required
@classroomSecureWrapper
def pollList(request, classroom):
    return render(request, 'pollingSite/pollList.html', locals())

@login_required
@classroomSecureWrapper
def createPoll(request, classroom):
    return render(request, 'pollingSite/createPoll.html', locals())

@login_required
@classroomSecureWrapper
def activePoll(request, poll, classroom):
    poll = Poll.objects.get(id=poll)
    options = range(1, poll.options + 1)
    return render(request, 'pollingSite/activePoll.html', locals())
