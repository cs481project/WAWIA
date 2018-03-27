import uuid
import itertools
import operator
import hashlib

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
        

        #holdText = "2"
        studentNumber = hashlib.sha224(request.POST['From'].encode('utf-8')).hexdigest()

        #parse text into a list
        incoming_text = holdText.split(" ")
        if(len(incoming_text) == 3):  # Update takes 3 arguments
            #check if first element is "Update". if it is not, then return
            if(incoming_text[0].lower() == "update"):
                #update
                try:
                    stud = Student.objects.get(phoneNumber=studentNumber)
                    stud.name=incoming_text[1]
                    stud.last_name=incoming_text[2]
                    stud.save()
                    #print("student {0} got updated".format(stud.name))
                    return HttpResponse("Message Recieved")
                except:
                    return HttpResponse("Message Not Recieved")
                    #print("An error occured when trying to update student")
                    #traceback.print_exc()

        elif(len(incoming_text) == 4):
            if(incoming_text[0].lower() == "register"):  # Register takes 4 arguments
                # check if the student is already registered
                # get the classroom connected to the class key the student entered
                try:
                    #check if the class they want to register to exists. if so save it
                    #print(Classroom.objects.filter(classKey=incoming_text[4].upper()).count())
                    if(Classroom.objects.filter(classKey=incoming_text[3].upper()).count() > 0):
                        classWantToRegisterTo = Classroom.objects.get(classKey=incoming_text[3].upper())
                        #print(classWantToRegisterTo)
                        # try to get the existing student from that class to later update it with new info
                        if(Student.objects.filter(phoneNumber=studentNumber).count() > 0): #if student exists
                            tempStudent = Student.objects.get(phoneNumber=studentNumber)
                            #print(tempStudent)
                            # if class exists
                            if(Classroom.objects.filter(students__phoneNumber__startswith=studentNumber).count() > 0):
                                allStudentClasses = Classroom.objects.filter(students__phoneNumber__startswith=studentNumber)
                                #print(allStudentClasses)
                                for item in allStudentClasses:
                                    if(item == classWantToRegisterTo):
                                        #print("Student already in class")
                                        pass
                                    else:
                                        classWantToRegisterTo.students.add(tempStudent)
                                        classWantToRegisterTo.save()
                                        return HttpResponse("Message Recieved")
                                        #print("added student to class")
                        else:
                            #print("The student did not exist. Will now try to create student with info")
                            try:
                                # if the student doesnt exist, try creating a new student and adding it to the class
                                studentCreate = Student.objects.create(name=incoming_text[1], lastname=incoming_text[2], phoneNumber=studentNumber)
                                #print("student: {}".format(studentCreate))
                                # save class the student wants to register to
                                classWantToRegisterTo = Classroom.objects.get(classKey=incoming_text[3].upper())
                                #print("class want to register to: {}".format(classWantToRegisterTo))
                                # add student to that class
                                classWantToRegisterTo.students.add(studentCreate)
                                classWantToRegisterTo.save()
                                return HttpResponse("Message Recieved")
                                #print("The student was added successfully")
                            except:
                                return HttpResponse("Message Not Recieved")
                    else:
                        #print("class does not exist. Will return message not recieved")
                        return HttpResponse("Message Not Recieved")
                except:
                    #print("An error occured. Will return message not recieved")
                    #traceback.print_exc()
                    return HttpResponse("Message Not Recieved")
        elif(len(incoming_text) != 1):
            #print("Not correct number of arguments needed. 1 argument needed")
            #return render(request, 'pollingSite/test.html',locals())
            return HttpResponse("Message Not Recieved")
        else:  # so if argument is 1
            studentAnswerLetter = holdText#incoming_text[0]
            #print(studentAnswerLetter)
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
                #print("The argument is not valid")
                return HttpResponse("Message Not Recieved")

            #try to get student depending on phone number
            try:
                studentIdentifier = Student.objects.get(phoneNumber=studentNumber)
                #print(studentIdentifier)
            except:
                #print("The student does not exist (has not registered)")
                return HttpResponse("Message Not Recieved")

            studentClassroom = Classroom.objects.filter(students=studentIdentifier)
            #print("student classroom: {}".format(studentClassroom))

            currentTime = datetime.now()
            #currentTime = currentTime.replace(hour=19, minute=1) #comment before final
            #currentTime = datetime.combine(currentTime, datetime.min.time())
            thereIsAClassCurrently = False

            for current_class in studentClassroom:
                #print("Current Class (checking): {}".format(current_class))
                # get classroom start time
                classroom_start = datetime.now()
                classroom_start = classroom_start.replace(hour=(current_class.start_time.hour), minute=(current_class.start_time.minute))

                # get classroom end time
                classroom_end = datetime.now()
                classroom_end = classroom_end.replace(hour=current_class.end_time.hour, minute=current_class.end_time.minute)
                #print("classroom start time: {}".format(classroom_start))
                #print("current time: {}".format(currentTime))
                #print("classroom end time: {}".format(classroom_end))
                if(currentTime > classroom_start and currentTime < classroom_end):
                    thereIsAClassCurrently = True;
                    #print("current class name: {}".format(current_class.className))
                    # get poll from that current class
                    currentPolls = Poll.objects.filter(classroom=current_class)
                    #print("current polls for {0} are: {1}".format(current_class.className, currentPolls))

                    # checks all the list of polls
                    for itemPoll in currentPolls:
                        if(itemPoll.isPollActive):  #if the poll is active
                            #print("current active Poll: {}".format(itemPoll))  # create an answer to that poll
                            #print(studentIdentifier)
                            # check if the student has already responded to the poll. if so try to update the poll
                            # need to get all the answer objects that belong to that poll first then loop through them and

                            # now loop through them and see
                            if(Answer.objects.filter(student=studentIdentifier, poll=itemPoll).count() == 0):
                                try:
                                    newAnswer = Answer.objects.create(poll=itemPoll, student=studentIdentifier, value=studentAnswer, timestamp=currentTime)
                                    newAnswer.save()
                                    #print("New answer: {}".format(newAnswer))
                                except:
                                    #print("Error trying to create Answer")
                                    return HttpResponse("Message Not Recieved")
                            else:
                                try:
                                    # get answer and update it with current input data
                                    currentAnswer = Answer.objects.get(student=studentIdentifier, poll=itemPoll)
                                    currentAnswer.value=studentAnswer
                                    currentAnswer.timestamp=currentTime
                                    currentAnswer.save()
                                    return HttpResponse("Message Recieved")
                                except:
                                    #print("Error could not get Answer. Does not exist")
                                    return HttpResponse("Message Not Recieved")

            if(thereIsAClassCurrently == False):
                #print("No class currently")
                return HttpResponse("Message Not Recieved")
    #return HttpResponse("Message Not Received")
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
        form = reportForm(request.POST, user=request.user)
        if form.is_valid():
            start_t = form.cleaned_data['start_date']
            end_t = form.cleaned_data['end_date']
            curClass=form.cleaned_data['choose_class']
            students = Student.objects.filter(classroom=curClass)
            students = sorted(students, key=operator.attrgetter('lastname'))
            for student1 in students:
                students_length = len(students)
                correctAnswer = []
                answers = []
                polllist = []
                totalnumbers = 0.0
                totalnumbers2 = 0.0
                answers = Answer.objects.filter(student=student1)
                polls = Poll.objects.filter(classroom=curClass)
                for poll in polls:
                    answerstopolls = []
                    if poll.startTime.date() >= start_t and poll.stopTime.date() <= end_t:
                        polllist.append(poll)
                        for answer in answers:
                            if answer.timestamp.date() >= start_t and answer.timestamp.date() <= end_t+ timedelta(days=1) and curClass == answer.poll.classroom:
                                answerstopolls.append(answer)
                            if poll.startTime <= answer.timestamp and answer.timestamp <= poll.stopTime and answer.value == poll.correct and student1.name==answer.student.name and student1.lastname == answer.student.lastname:
                                correctAnswer.append(answer)
                        if(len(answerstopolls)!=0):
                            totalnumbers='%.2f'%((len(correctAnswer)/len(answerstopolls))*100)
                        if(len(polllist)!=0):
                            totalnumbers2='%.2f'%((len(answerstopolls)/len(polllist))*100)
                items += list(itertools.zip_longest([correctAnswer],[answerstopolls],[polllist],[student1],[totalnumbers],[totalnumbers2],fillvalue='-'))
            enumerated_items = enumerate(items)
        return render(request, 'pollingSite/report.html', locals())
    else:
        form = reportForm(initial={'choose_class': request.user.activeClass},user=request.user)
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
        form = createPollForm(request.POST, user=request.user)
        if form.is_valid():
            newPoll = Poll.objects.create(classroom = Classroom.objects.get(pk=classroom), options=form.cleaned_data['possible_answers'], startTime = datetime.now(), stopTime = datetime.now())
            newPoll.startTime = timezone.now()
            newPoll.save()

            return redirect('pollingSite:activePoll', curClass1, newPoll.id)
    elif classroom is 'None':
        return redirect('pollingSite:addClass')
    else:
        classroom = Classroom.objects.get(pk=classroom)
        form = createPollForm(initial={'choose_class': request.user.activeClass}, user=request.user)
        return render(request, 'pollingSite/createPoll.html', locals())

@login_required
@classroomSecureWrapper
def activePoll(request, poll, classroom):
    poll = Poll.objects.get(id=poll)
    options = []
    totalSub = 0
    poll.save(update_fields=['isPollActive'])
    for option in range(1, poll.options+1):
        next = Answer.objects.filter(poll=poll, value=option).count()
        options.append(next)
        totalSub += next
    if request.method == 'POST':
        form = correctAnswerForm(request.POST)
        poll.isPollActive=False
        poll.save(update_fields=['isPollActive'])
        if form.is_valid():
            charval = form.cleaned_data['correct_answer']
            poll.correct = ord(charval.upper()) - 64
            poll.save(update_fields=['correct'])
            poll.stopTime = timezone.now()
            poll.save(update_fields=['stopTime'])
            poll.submit = True
            poll.save(update_fields=['submit'])
            return render(request, 'pollingSite/activePoll.html', locals())
    else:
        form = correctAnswerForm()
        otherPolls = Poll.objects.filter(classroom=Classroom.objects.get(id=classroom))
        for Opoll in otherPolls:
            Opoll.isPollActive = False
            Opoll.save(update_fields=['isPollActive'])
        if(poll.submit==False):
            poll.isPollActive=True
            poll.save(update_fields=['isPollActive'])
        else:
            poll.isActive=False
            poll.save(update_fields=['isPollActive'])
        
    return render(request, 'pollingSite/activePoll.html', locals())