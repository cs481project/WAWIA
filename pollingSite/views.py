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
        #holdText = "Register John Doe 84638212 KEY000"
        #holdText = "register El M 85443344 KEY000"
        #holdText = "Register Klye Dish 11122222 KEY01"

        # update format is "Up First Last ID"
        ##holdText = "Update Thomas Jefferson 548234327"

        # send an answer
       # holdText = "T"

        #studentNumber = 4252319279#1029384756

        #holdText = "2"
        studentNumber = hash(request.POST['From'])

        #parse text into a list
        incoming_text = holdText.split(" ")

        print(len(incoming_text))

        if(len(incoming_text) == 4):  # Update takes 4 arguments
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
                # check if the student is already registered
                # get the classroom connected to the class key the student entered
                try:
                    #check if the class they want to register to exists. if so save it
                    print(Classroom.objects.filter(classKey=incoming_text[4].upper()).count())
                    if(Classroom.objects.filter(classKey=incoming_text[4].upper()).count() > 0):
                        classWantToRegisterTo = Classroom.objects.get(classKey=incoming_text[4].upper())
                        print(classWantToRegisterTo)

                        # try to get the existing student from that class to later update it with new info
                        if(Student.objects.filter(phoneNumber=studentNumber).count() > 0): #if student exists
                            tempStudent = Student.objects.get(phoneNumber=studentNumber)
                            print(tempStudent)
                            # if class exists
                            if(Classroom.objects.filter(students__phoneNumber__startswith=studentNumber).count() > 0):
                                allStudentClasses = Classroom.objects.filter(students__phoneNumber__startswith=studentNumber)
                                print(allStudentClasses)
                                for item in allStudentClasses:
                                    if(item == classWantToRegisterTo):
                                        print("Student already in class")
                                    else:
                                        classWantToRegisterTo.students.add(tempStudent)
                                        print("added student to class")
                        #
                        else:
                            print("The student did not exist. Will now try to create student with info")
                            try:
                                # if the student doesnt exist, try creating a new student and adding it to the class
                                studentCreate = Student.objects.create(name=incoming_text[1], lastname=incoming_text[2], studentID=incoming_text[3], phoneNumber=studentNumber)
                                print(studentCreate)

                                # save class the student wants to register to
                                classWantToRegisterTo = Classroom.objects.get(classKey=incoming_text[4].upper())
                                print(classWantToRegisterTo)

                                # add student to that class
                                classWantToRegisterTo.students.add(studentCreate)

                                print("The student was added successfully")
                            except:
                                print("Error")
                                print("Could not create a student with the entered data")
                                traceback.print_exc()
                    else:
                        print("class does not exist. Will return message not recieved")
                        return HttpResponse("Message Not Recieved")
                except:
                    print("An error occured. Will return message not recieved")
                    traceback.print_exc()
                    return HttpResponse("Message Not Recieved")
        elif(len(incoming_text) != 1):
            print("Not correct number of arguments needed. 1 argument needed")
            #return render(request, 'pollingSite/test.html',locals())
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

            #return HttpResponse("Message Received")
    return render(request, 'pollingSite/test.html',locals())

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
def setActive(request, classroom):
    classroom = Classroom.objects.get(pk=classroom)
    request.user.activeClass = classroom
    request.user.save()
    return redirect('pollingSite:index')

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
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
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
def edit(request, classroom):
    thisClass = Classroom.objects.get(id=classroom)
    if request.method == 'POST':
        form = editClassForm(request.POST, instance=thisClass)
        if form.is_valid():
            editClass = Classroom.objects.get(id=classroom)
            editClass.className = form.cleaned_data['className']
            editClass.quarter = form.cleaned_data['quarter']
            editClass.year = form.cleaned_data['year']
            editClass.start_date = form.cleaned_data['start_date']
            editClass.end_date = form.cleaned_data['end_date']
            editClass.start_time = form.cleaned_data['start_time']
            editClass.end_time = form.cleaned_data['end_time']
            editClass.save()
            return redirect('pollingSite:index')
    else:
        form = editClassForm(instance=thisClass)
        return render(request, 'pollingSite/editClass.html', locals())

@login_required
def pollLanding(request):
    if request.user.activeClass == None:
        return redirect('pollingSite:addClass')
    else:
        return redirect('pollingSite:createPoll', request.user.activeClass.id)

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
        form = correctAnswerForm(request.POST)
        if form.is_valid():
            charval = form.cleaned_data['correct_answer']
            poll.correct = ord(charval.upper()) - 64
            poll.save(update_fields=['correct'])
            return render(request, 'pollingSite/activePoll.html', locals())
        else:
            poll.stopTime = timezone.now()
            poll.isPollActive=False;
            poll.save()
            return render(request, 'pollingSite/activePoll.html', locals())
    else:
        form = correctAnswerForm()
        otherPolls = Poll.objects.filter(classroom=Classroom.objects.get(id=classroom))
        for poll in otherPolls:
            poll.isPollActive = False
            poll.save(update_fields=['isPollActive'])

        poll.isPollActive=True
        poll.save(update_fields=['isPollActive'])
        return render(request, 'pollingSite/activePoll.html', locals())
