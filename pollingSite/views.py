import uuid
import itertools
import operator

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
    students = []
    w = 7
    items = []
    if request.method == 'POST':
        form = reportForm(request.POST)
        if form.is_valid():
            start_t = form.cleaned_data['start_date']
            end_t = form.cleaned_data['end_date']
            curClass=form.cleaned_data['choose_class']
            students = Student.objects.filter(classrooms=curClass)
            students = sorted(students, key=operator.attrgetter('lastname'))
            print(curClass)
            for student1 in students:
                correctAnswer = []
                answers = []
                polllist = []
                totalnumbers = 0.0
                totalnumbers2 = 0.0
                answers = Answer.objects.filter(student=student1)
                polls = Poll.objects.filter(classroom=curClass)
                print(answers)
                for poll in polls: 
                    answerstopolls = [] 
                    if poll.startTime.date() >= start_t and poll.stopTime.date() <= end_t:
                        polllist.append(poll) 
                        for answer in answers:
                            print(start_t)
                            print(answer.timestamp.date())
                            print(end_t)
                            if answer.timestamp.date() >= start_t and answer.timestamp.date() <= end_t+ timedelta(days=1) and curClass == answer.poll.classroom:
                                answerstopolls.append(answer)
                            if poll.startTime <= answer.timestamp and answer.timestamp <= poll.stopTime and answer.value == poll.correct and student1.name==answer.student.name:
                                correctAnswer.append(answer)
                        if(len(answerstopolls)!=0):
                            totalnumbers=((len(correctAnswer)/len(answerstopolls))*100)
                        if(len(polllist)!=0):
                            totalnumbers2=((len(answerstopolls)/len(polllist))*100)
                items += list(itertools.zip_longest([correctAnswer],[answerstopolls],[polllist],[student1],[totalnumbers],[totalnumbers2],fillvalue='-'))
            enumerated_items = enumerate(items)
        return render(request, 'pollingSite/report.html', locals())
    else:
        form = reportForm(initial={'choose_class': request.user.activeClass})
        return render(request, 'pollingSite/report.html', locals())

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
    if request.method == 'POST':
        form = correctAnswerForm(request.POST)
        if form.is_valid():
            poll.correct= form.cleaned_data['correct_answer']
            poll.save(update_fields=['correct'])
            return render(request, 'pollingSite/activePoll.html', locals())
    else:
        form = correctAnswerForm()        
        return render(request, 'pollingSite/activePoll.html', locals())