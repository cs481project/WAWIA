from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def landing(request):
    if request.user.is_anonymous:
        return redirect('account_login')
    else:
        return redirect('index')

def index(request):
    classroom = Classroom.objects.all()
    return render(request, 'pollingSite/index.html', locals())

def search(request):
    return render(request,'pollingSite/studentSearch.html', locals())

def classroom(request, classroom):
    polls = Poll.objects.filter(classroom=classroom)
    return HttpResponse(classroom)

def attendance(request, classroom):
    return render(request, 'pollingSite/attendance.html', locals())

def createPoll(request, classroom):
    return render(request, 'pollingSite/createPoll.html', locals())

def activePoll(request, poll, classroom):
    poll = Poll.objects.get(id=poll)
    options = range(1, poll.options + 1)
    return render(request, 'pollingSite/activePoll.html', locals())

def account_login(request):
    return render(request, 'pollingSite/login.html', locals())