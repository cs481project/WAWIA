import uuid
import itertools
from datetime import datetime, timedelta,date
from django import template
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login as authLogin
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Trunc

from .models import *
from .forms import *

register = template.Library()

def classroomSecureWrapper(function):
    def decorator(request, *args, **kwargs):
        classroom = Classroom.objects.get(pk=kwargs['classroom'])
        if classroom.instructor == request.user:
            return function(request, *args, **kwargs)
        else:
            raise Http404
    return decorator

@csrf_exempt
def recieveSMS(request):
    if request.method == 'POST':
        #save inbound text into variable
        holdText = request.POST['Text']

        #parse text into a list
        incoming_text = holdText.split(", ")

        #create new object and update fields
        newStudent = Answer.objects.create(poll=Poll.objects.get(key=incoming_text[0]), value=incoming_text[1], timestamp=now(), student=Student.objects.get(name='FakeNews'))
        return HttpResponse("Message Received")

def landing(request):
    if request.user.is_authenticated:
        return redirect('pollingSite:index')
    else:
        return redirect('pollingSite:login')

@login_required
def index(request):
    classroom = Classroom.objects.filter(instructor=request.user).order_by("-year", "-quarter")
    return render(request, 'pollingSite/index.html', locals())

@login_required
def pollAdmin(request):
    return addSearchClass(request)

@login_required
def setActive(request, classroom):
    classroom = Classroom.objects.get(pk=classroom)
    request.user.activeClass = classroom
    request.user.save()
    return redirect('pollingSite:index')

@login_required
def addSearchClass(request):
    classroom = Classroom.objects.filter(instructor=request.user).order_by("-year", "-quarter")
    return render(request, 'pollingSite/addSearchClass.html', locals())

@login_required
def copyClass(request, classroom):
    classroom = Classroom.objects.get(pk=classroom)
    if request.method == 'POST':
        form = copyClassForm(request.POST)
        if form.is_valid():
            classroom.duplicate(request.user, form.cleaned_data['class_name'], form.cleaned_data['quarter'], form.cleaned_data['year'])
            return redirect('pollingSite:pollAdmin')
    else:
        form = copyClassForm(initial={'class_name':classroom.className, 'quarter':classroom.quarter, 'year':classroom.year})
        return render(request, 'pollingSite/copyClass.html', locals())

@login_required
def settings(request):
    message = None
    email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name
    if request.method == 'POST':
        form = settingForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.get_username())
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            message = "Changed Personal Settings"
            return render(request, 'pollingSite/setting.html', locals())
    else:
        form = settingForm(initial={'email':email, 'first_name':first_name, 'last_name':last_name})
        return render(request, 'pollingSite/setting.html', locals())

@login_required
def search(request):
    return render(request, 'pollingSite/search.html', locals())

@login_required
def report(request):
    return HttpResponse('Report')

@login_required
def addClass(request):
    if request.method == 'POST':
        form = createClassForm(request.POST)
        if form.is_valid():
            Classroom.objects.create(className=form.cleaned_data['class_name'],
                quarter = form.cleaned_data['quarter'],
                year=form.cleaned_data['year'],
                instructor=request.user)
            return redirect('pollingSite:index');
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
def attendanceForm(request, classroom):
    curClass=classroom
    
    totalnumbers = 0
    totalnumbers2 = 0
    
    
    students = []
    polllist = []
    polllist2 = []
    polls = Poll.objects.filter(classroom=curClass)
    if request.method == 'POST':
        form = attendanceFormForm(request.POST)
        if form.is_valid():
            start_t = form.cleaned_data['start_date']
            end_t = form.cleaned_data['end_date']
            students = Student.objects.filter(classrooms=curClass)
            for student1 in students:
                
                answers = []
                answers = Answer.objects.filter(student=student1,timestamp__gte=start_t, timestamp__lt=end_t + timedelta(days=1))
                for answer in answers:
                    if answer.timestamp.date() >= start_t and answer.timestamp.date() <= end_t:
                        polllist.append(answer)
                    for poll in polls:
                        correctAnswer = []
                        if poll.stopTime.date() >= start_t and poll.stopTime.date() <= end_t:
                            polllist2.append(poll)
                        if poll.startTime < answer.timestamp < poll.stopTime and answer.value == poll.correct:
                            correctAnswer.append(answer)
                        for a in range(len(polllist)):
                            for b in range(a+1, len(polllist)):
                                if (polllist[a].timestamp.date() == polllist[b].timestamp.date()):
                                    del polllist[a]

                        for c in range(len(polllist2)):
                            for d in range(c+1, len(polllist2)):
                                if (polllist2[c].stopTime.date()== polllist2[d].stopTime.date()):
                                    del polllist2[c]
            totalnumbers=(len(correctAnswer)/len(answers))*100
            totalnumbers2=(len(polllist)/len(polllist2))*100
            return render(request, 'pollingSite/attendance.html', locals())
    else:
        form = attendanceFormForm()
        return render(request, 'pollingSite/attendanceForm.html', locals())

@login_required
@classroomSecureWrapper
def pollList(request, classroom):
    polls = Poll.objects.filter(classroom=classroom)
    curClass = Classroom.objects.get(id=classroom)
    return render(request, 'pollingSite/pollList.html', locals())

@login_required
@classroomSecureWrapper
def createPoll(request, classroom):
    curClass1 = classroom
    if request.method == 'POST':
        form = createPollForm(request.POST)
        if form.is_valid():
            newPoll = Poll.objects.create(classroom = Classroom.objects.get(pk=classroom), name="", options=form.cleaned_data['possible_answers'], startTime = datetime.now(), stopTime = datetime.now())
            return redirect('pollingSite:activePoll', curClass1, newPoll.id)
    else:
        classroom = Classroom.objects.get(pk=classroom)
        form = createPollForm()
        return render(request, 'pollingSite/createPoll.html', locals())

@login_required
@classroomSecureWrapper
def activePoll(request, poll, classroom):
    poll = Poll.objects.get(id=poll)
    options = []
    totalSub = 0
    for option in range(1, poll.options+1):
        next = Answer.objects.filter(poll=poll, value=option).count()
        options.append(next)
        totalSub += next
        
    return render(request, 'pollingSite/activePoll.html', locals())
