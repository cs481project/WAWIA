from django import forms
from datetime import datetime
from .models import SEASONS

class createClassForm(forms.Form):
    class_name = forms.CharField(max_length=50)
    class_id = forms.CharField(max_length=50)
    quarter = forms.ChoiceField(choices=SEASONS)
    year = forms.ChoiceField(choices=[(i,i) for i in range(2018, datetime.now().year + 2)])

class createPollForm(forms.Form):
    new_poll_name = forms.CharField(max_length=100)
    possible_answers = forms.IntegerField()
    correct_answer = forms.IntegerField()
    #start_time = forms.DateTimeField()
    #end_time = forms.DateTimeField()

class attendanceFormForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

class settingForm(forms.Form):
    email = forms.CharField(max_length=50, required=False)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
