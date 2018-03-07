import uuid
import itertools
import operator

from datetime import datetime, timedelta,date
from django import template
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login as authLogin
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Trunc

from .models import *
from .forms import *

import traceback

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

        # register format is "Reg First Last ID classKey"
        #holdText = "Register George Washington 1337 key999"

        # update format is "Up First Last ID"
        #holdText = "Update Thomas Jefferson 548234327"

        # send an answer
       # holdText = "T"

        #studentNumber = 5093313630#4252319279

        #holdText = "2"
        studentNumber = request.POST['From'] #https://www.plivo.com/docs/api/message/

        #parse text into a list
        incoming_text = holdText.split(" ")

        print(len(incoming_text))

        if(len(incoming_text) == 3):  # Update takes 4 arguments
            #check if first element is "Update". if it is not, then return
            if(incoming_text[0].lower() == "update"):
                #update
                try:
                    stud = Student.objects.get(phoneNumber=studentNumber)
                    stud.name=incoming_text[1]
                    stud.last_name=incoming_text[2]
                    stud.save()
                    print("student got updated")
                    return HttpResponse("Message Recieved")
                except:
                    print("An error occured when trying to update student")
                    traceback.print_exc()

        elif(len(incoming_text) == 5):
            if(incoming_text[0].lower() == "register"):  # Register takes 5 arguments
                stdName = incoming_text[1] + incoming_text[2]
                # create new student
                print(Student.objects.filter(phoneNumber=studentNumber).exists())  # does the student exist?
                try:
                    if(Student.objects.filter(phoneNumber=studentNumber).exists()):  # if the student exists, dont do anything
                        print("An error occured. The student already exists")
                        return HttpResponse("Message Recieved")#return render(request, 'pollingSite/test.html',locals())
                    else:  # if the student doesnt exist, create the student
                        studentCreate = Student.objects.create(name=incoming_text[1], last_name=incoming_text[2], studentID=incoming_text[3], phoneNumber=studentNumber)
                        print(studentCreate)
                        # get classroom with that class key
                        Classroom.objects.get(classKey=incoming_text[4].upper()).students.add(studentCreate)
                        print("Created a student")
                except:
                    print("An error occured when trying to add a student")
                    traceback.print_exc()
                    # now only need to add the student to the class
                    #return render(request, 'pollingSite/test.html',locals

        elif(len(incoming_text) != 1):
            print("Not correct number of arguments needed. 1 argument needed")
            return render(request, 'pollingSite/test.html',locals())
        else:  # so if argument is 1
            studentAnswerLetter = holdText#incoming_text[0]
            print(studentAnswerLetter)
            studentAnswer = 0  #initilize studentAnswer

            if(studentAnswerLetter == "A"):
                studentAnswer = 1
            elif(studentAnswerLetter == "B"):
                studentAnswer = 2
            elif(studentAnswerLetter == "C"):
                studentAnswer = 3
            elif(studentAnswerLetter == "D"):
                studentAnswer = 4
            elif(studentAnswerLetter == "E"):
                studentAnswer = 5
            elif(studentAnswerLetter == "F"):
                studentAnswer = 6
            elif(studentAnswerLetter == "G"):
                studentAnswer = 7
            elif(studentAnswerLetter == "H"):
                studentAnswer = 8
            elif(studentAnswerLetter == "I"):
                studentAnswer = 9
            elif(studentAnswerLetter == "J"):
                studentAnswer = 10
            elif(studentAnswerLetter == "K"):
                studentAnswer = 11
            elif(studentAnswerLetter == "L"):
                studentAnswer = 12
            elif(studentAnswerLetter == "M"):
                studentAnswer = 13
            elif(studentAnswerLetter == "N"):
                studentAnswer = 14
            elif(studentAnswerLetter == "O"):
                studentAnswer = 15
            elif(studentAnswerLetter == "P"):
                studentAnswer = 16
            elif(studentAnswerLetter == "Q"):
                studentAnswer = 17
            elif(studentAnswerLetter == "R"):
                studentAnswer = 18
            elif(studentAnswerLetter == "S"):
                studentAnswer = 19
            elif(studentAnswerLetter == "T"):
                studentAnswer = 20
            elif(studentAnswerLetter == "U"):
                studentAnswer = 21
            elif(studentAnswerLetter == "V"):
                studentAnswer = 22
            elif(studentAnswerLetter == "W"):
                studentAnswer = 23
            elif(studentAnswerLetter == "X"):
                studentAnswer = 24
            elif(studentAnswerLetter == "Y"):
                studentAnswer = 25
            elif(studentAnswerLetter == "Z"):
                studentAnswer = 26
            else:
                #return (answer was not valid)
                print("The argument is not valid")
                #return render(request, 'pollingSite/test.html',locals())

            studentIdentifier = Student.objects.get(phoneNumber=studentNumber)
            print(studentNumber)
            print(studentIdentifier.studentID)

            studentClassroom = Classroom.objects.filter(students=studentIdentifier)
            print(studentClassroom)

            currentTime = datetime.now()
            #currentTime = currentTime.replace(hour=19, minute=1) #comment before final
            #currentTime = datetime.combine(currentTime, datetime.min.time())
            print(currentTime)

            for item in studentClassroom:
                start = datetime.now()
                start = start.replace(hour=(item.start_time.hour), minute=(item.start_time.minute))

                end = datetime.now()
                hour = item.end_time.hour
                minutez = item.end_time.minute
                end = end.replace(hour=hour, minute=minutez)

                if(currentTime > start and currentTime < end):
                    print(item.className)
                    # get poll from that current class
                    currentClass = item
                    currentPolls = Poll.objects.filter(classroom=item)

                    print(currentPolls)

                    # checks all the list of polls
                    for itemPoll in currentPolls:
                        if(itemPoll.isPollActive):  #if the poll is active
                            print(itemPoll)  # create an answer to that poll
                            Answer.objects.create(poll=itemPoll, student=studentIdentifier, value=studentAnswer, timestamp=currentTime)

                    #print(classActivePoll)
                    #create answer
                    #newAnswer = Answer.objects.create(poll=Poll.objects.get(key=incoming_text[0]), value=incoming_text[1], timestamp=now(), student=Student.objects.get(name=studentIdentifier))
                else:
                    print("No class currently")

            #create new object and update fields
            #newStudent = Answer.objects.create(poll=Poll.objects.get(key=incoming_text[0]), value=incoming_text[1], timestamp=now(), student=Student.objects.get(name='FakeNews'))
            #return HttpResponse("Message Received")
    #return render(request, 'pollingSite/test.html',locals())

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
            students = Student.objects.filter(classroom=curClass)
            students = sorted(students, key=operator.attrgetter('lastname'))
            print(curClass)
            for student1 in students:
                students_length = len(students)
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
            classroom = Classroom.objects.create(className=form.cleaned_data['class_name'],
                quarter = form.cleaned_data['quarter'],
                year=form.cleaned_data['year'],
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                instructor=request.user)
            if request.user.activeClass == None:
                request.user.activeClass = classroom
                request.user.save()
                return redirect('pollingSite:index')
            else:
                return redirect('pollingSite:index')
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
def pollLanding(request):
    if request.user.activeClass == None:
        return redirect('pollingSite:addClass')
    else:
        return redirect('pollingSite:createPoll', request.user.activeClass.id)

@login_required
@classroomSecureWrapper
def info(request, classroom):
    classroom = Classroom.objects.get(id=classroom)
    return render(request, 'pollingSite/info.html', locals())

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
            newPoll.startTime = timezone.now()
            newPoll.save()

            return redirect('pollingSite:activePoll', curClass1, newPoll.id)
    elif classroom is 'None':
        return redirect('pollingSite:addClass')
    else:
        classroom = Classroom.objects.get(pk=classroom)
        form = createPollForm(initial={'choose_class': request.user.activeClass})
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
        form = correctAnswerForm(request.POST, poll.options)
        if form.is_valid():
            poll.correct = form.cleaned_data['correct_answer']
            poll.save(update_fields=['correct'])
            
            return render(request, 'pollingSite/activePoll.html', locals())
        else:
            poll.stopTime = timezone.now()
            poll.save()
            return render(request, 'pollingSite/activePoll.html', locals())
    else:
        form = correctAnswerForm(poll.options)        
        return render(request, 'pollingSite/activePoll.html', locals())