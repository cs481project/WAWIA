from string import ascii_uppercase, digits
from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

SEASONS = ((0, "Winter"), (1,"Spring"), (2,"Summer"), (3,"Fall"))

class InstructorUser(AbstractUser):
    activeClass = models.OneToOneField('Classroom', blank = True, on_delete=models.SET_NULL, null=True)

class Classroom(models.Model):
    classNumber = models.CharField(max_length = 20, default="")
    className = models.CharField(max_length = 64, default=classNumber)
    classKey = models.CharField(max_length = 6, unique=True)
    quarter = models.IntegerField(choices=SEASONS)
    year = models.IntegerField(choices=[(i,i) for i in range(2018, datetime.now().year + 1)])
    instructor = models.ForeignKey(InstructorUser, on_delete=models.SET_NULL, null=True) #change on_delete
    def __str__(self):
        return self.className
    def __init__(self, *args, **kwargs):
        super(Classroom, self).__init__(*args, **kwargs)
        if(self.classKey == ''):
            chars = ascii_uppercase + digits
            self.classKey = ''.join(choices(chars, k=5))

    def duplicate(self, user, name, quarter, year):
        dupe = Classroom.objects.create(instructor = user,
                                        className=name,
                                        classNumber=self.classNumber,
                                        quarter=quarter, 
                                        year=year)
        dupe.save()
        for poll in Poll.objects.filter(classroom=self):
            newPoll = Poll.objects.create(
                                name=poll.name,
                                options=poll.options,
                                correct=poll.correct,
                                classroom=dupe,
                                )
            newPoll.save()

class Student(models.Model):
    name = models.CharField(max_length = 128)
    studentID = models.IntegerField(unique=True)
    phoneNumber = models.CharField(max_length = 20, null=True)
    classrooms = models.ManyToManyField(Classroom)
    def __str__(self):
        return self.name

class Poll(models.Model):
    name = models.CharField(max_length = 64)
    options = models.IntegerField()
    correct = models.IntegerField(default=1)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    startTime = models.DateTimeField(null=True)
    stopTime = models.DateTimeField(null=True)
            
    def __str__(self):
        return self.name
		
    def isActive(self):
        if(self.startTime < datetime.now()):
            if(self.stopTime is not null or (self.stopTime > datetime.now())):
                return True
        return False

class Answer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    value = models.IntegerField()
    timestamp = models.DateTimeField()
    def __str__(self):
        return '{} + {}'.format(self.student, self.poll)