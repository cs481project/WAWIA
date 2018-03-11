from django import forms
from datetime import datetime
from .models import SEASONS, Classroom
from django.contrib.auth.models import User
from django.db.models import Count, Q

class createClassForm(forms.Form):
    class_name = forms.CharField(max_length=50)
    quarter = forms.ChoiceField(choices=SEASONS)
    year = forms.ChoiceField(choices=[(i,i) for i in range(2018, datetime.now().year + 2)])
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    start_time = forms.TimeField(label="Start Time (24hr)", widget=forms.TimeInput({"placeholder":"HH:MM"},format='%H:%M'))
    end_time = forms.TimeField(label="Start Time (24hr)", widget=forms.TimeInput({"placeholder":"HH:MM"},format='%H:%M'))

class editClassForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['className', 'quarter', 'year', 'start_date', 'end_date', 'start_time', 'end_time']

    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    start_time = forms.TimeField(label="Start Time (24hr)", widget=forms.TimeInput({"placeholder":"HH:MM"}, format='%H:%M'))
    end_time = forms.TimeField(label="Start Time (24hr)", widget=forms.TimeInput({"placeholder":"HH:MM"}, format='%H:%M'))

class createPollForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(createPollForm, self).__init__(*args, **kwargs)
        self.fields['choose_class'] = forms.ModelChoiceField(queryset=Classroom.objects.filter(instructor=user))

    choose_class = forms.ModelChoiceField(queryset=Classroom.objects.none())
    possible_answers = forms.ChoiceField(choices=[(i,i) for i in range(2,13)], label="# of options for this poll")

class correctAnswerForm(forms.Form):
    correct_answer = forms.CharField(max_length=1)

class reportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(reportForm, self).__init__(*args, **kwargs)
        self.fields['choose_class'] = forms.ModelChoiceField(queryset=Classroom.objects.filter(instructor=user))

    choose_class = forms.ModelChoiceField(queryset=Classroom.objects.none())
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
