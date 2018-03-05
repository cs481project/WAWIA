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
        #holdText = "Jane Doe 77777777 key999"#request.POST['Text']

        # register format is "Reg First Last ID classKey"
        #holdText = "Register George Washington 1337 key999"

        # update format is "Up First Last ID"
        #holdText = "Update Thomas Jefferson 548234327"

        # send an answer
        holdText = "T"

        #studentNumber = 5093313630#4252319279

        #holdText = "2"
        studentNumber = 1112223333#request.POST['src']#https://www.plivo.com/docs/api/message/

        #parse text into a list
        incoming_text = holdText.split(" ")

        print(len(incoming_text))

        if(len(incoming_text) == 4):  # Update takes 4 arguments
            #check if first element is "Update". if it is not, then return
            if(incoming_text[0].lower() == "update"):
                #update
                try:
                    Student.objects.filter(phoneNumber=studentNumber).update(name=incoming_text[1], studentID=incoming_text[3])  # remember to add last name when change models
                    print("student got updated")
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
                        return render(request, 'pollingSite/test.html',locals())
                    else:  # if the student doesnt exist, create the student
                        studentCreate = Student.objects.create(name=stdName, studentID=incoming_text[3], phoneNumber=studentNumber)
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
                return render(request, 'pollingSite/test.html',locals())

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
                start = start.replace(hour=(item.StartTime.hour), minute=(item.StartTime.minute))

                end = datetime.now()
                hour = item.EndTime.hour
                minutez = item.EndTime.minute
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
    return render(request, 'pollingSite/test.html',locals())

def landing(request):
    if request.user.is_authenticated:
        return redirect('pollingSite:index')
    else:
        return redirect('pollingSite:login')

@login_required
def index(request):
    first_name = ""
    last_name = ""
    username = ""
    if request.user.first_name == "":
        if request.user.last_name == "":
            username = request.user.get_username()
            return render(request, 'pollingSite/index.html',locals())
        else:
            last_name = request.user.last_name
            return render(request, 'pollingSite/index.html',locals())
    else:
        first_name = request.user.first_name
        if request.user.last_name == "":
            return render(request, 'pollingSite/index.html',locals())
        else:
            last_name = request.user.last_name
            return render(request, 'pollingSite/index.html',locals())

@login_required
def pollAdmin(request):
    return addSearchClass(request)

@login_required
def addSearchClass(request):
    classroom = Classroom.objects.filter(instructor=request.user).order_by("-year", "-quarter")
    return render(request, 'pollingSite/addSearchClass.html', locals())

@login_required
def copy(request, classroom):
    classroom = Classroom.objects.get(pk=classroom)
    classroom.duplicate(request.user, classroom.quarter, classroom.year)
    return redirect('pollingSite:pollAdmin')

@login_required
def settings(request):
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
            return HttpResponse('Changed Email')
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
                classNumber=form.cleaned_data['class_id'],
                quarter = form.cleaned_data['quarter'],
                year=form.cleaned_data['year'],
                instructor=request.user)
            return redirect('pollingSite:pollAdmin');
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
            Poll.objects.create(classroom = Classroom.objects.get(pk=classroom), name=form.cleaned_data['new_poll_name'], options=form.cleaned_data['possible_answers'], correct=form.cleaned_data['correct_answer'], startTime = datetime.now(), stopTime = datetime.now())
            return redirect('pollingSite:pollList', curClass1)
    else:
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
