from string import ascii_uppercase, digits
from random import choices
from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
    classNumber = models.CharField(max_length = 20, unique=True)
    className = models.CharField(max_length = 64, default=classNumber)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.className

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
    key = models.CharField(max_length = 6, unique=True, default='')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    startTime = models.DateTimeField(null=True)
    stopTime = models.DateTimeField(null=True)
    def __init__(self, *args, **kwargs):
        super(Poll, self).__init__(*args, **kwargs)
        chars = ascii_uppercase + digits
        self.key = ''.join(choices(chars, k=5))

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