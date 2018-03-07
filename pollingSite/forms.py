from django import forms
from datetime import datetime
from .models import SEASONS, Classroom
from django.contrib.auth.models import User
from django.db.models import Count

class createClassForm(forms.Form):
    class_name = forms.CharField(max_length=50)
    quarter = forms.ChoiceField(choices=SEASONS)
    year = forms.ChoiceField(choices=[(i,i) for i in range(2018, datetime.now().year + 2)])
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    start_time = forms.TimeField(widget=forms.TimeInput({"placeholder":"HH:MM"},format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput({"placeholder":"HH:MM"},format='%H:%M'))

class editClassForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['className', 'quarter', 'year', 'start_date', 'end_date', 'start_time', 'end_time']

    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

class copyClassForm(forms.Form):
    class_name = forms.CharField(max_length=50)
    quarter = forms.ChoiceField(choices=SEASONS)
    year = forms.ChoiceField(choices=[(i,i) for i in range(2018, datetime.now().year + 2)])

class createPollForm(forms.Form):
    choose_class = forms.ModelChoiceField(queryset=Classroom.objects.annotate(class_count=Count('className')))
    possible_answers = forms.ChoiceField(choices=[(i,i) for i in range(2,13)], label="# of options for this poll")

class correctAnswerForm(forms.Form):
    correct_answer = forms.ChoiceField()
    def __init__(self, *args, **kwargs):
        super(correctAnswerForm, self).__init__()
        if 'choices' in kwargs:
            choices = kwargs.pop('choices')
            self.fields['correct_answer'].choices=[(i,chr(64+i)) for i in range(1,choices+1)]

class attendanceFormForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

class activePollForm(forms.Form):
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    
class settingForm(forms.Form):
    email = forms.CharField(max_length=50, required=False)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

class reportForm(forms.Form):
    choose_class = forms.ModelChoiceField(queryset=Classroom.objects.annotate(class_count=Count('className')))
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
