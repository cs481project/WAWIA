from django.contrib import admin

from .models import *

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'studentID')

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('className', 'classNumber', 'instructor')

class PollAdmin(admin.ModelAdmin):
    readonly_fields=('key',)
    list_display = ('name', 'classroom', 'startTime', 'stopTime')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('poll', 'student', 'timestamp')


admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Answer, AnswerAdmin)