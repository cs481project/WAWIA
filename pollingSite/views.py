from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *

def landing(request):
    if request.user.is_anonymous:
        return redirect('pollingSite:login')
    else:
        return redirect('pollingSite:index')

def index(request):
    classroom = Classroom.objects.all()
    return render(request, 'pollingSite/index.html', locals())

def login(request):
    return render(request, 'pollingSite/login.html', locals())

def changePassword(request):
    return render(request, 'pollingSite/changePassword.html', locals())

def search(request):
    return render(request, 'pollingSite/search.html', locals())

def addClass(request):
    return render(request, 'pollingSite/addClass.html', locals())

def classroom(request, classroom):
    polls = Poll.objects.filter(classroom=classroom)
    return pollList(request, classroom)

def attendance(request, classroom):
    return render(request, 'pollingSite/attendance.html', locals())

def pollList(request, classroom):
    return render(request, 'pollingSite/pollList.html', locals())

def createPoll(request, classroom):
    return render(request, 'pollingSite/createPoll.html', locals())

def activePoll(request, poll, classroom):
    poll = Poll.objects.get(id=poll)
    options = range(1, poll.options + 1)
    return render(request, 'pollingSite/activePoll.html', locals())
