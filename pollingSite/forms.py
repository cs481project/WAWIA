from django import forms
from datetime import datetime
from .models import SEASONS

class createClassForm(forms.Form):
    class_name = forms.CharField(max_length=50)
    quarter = forms.ChoiceField(choices=SEASONS)
    year = forms.ChoiceField(choices=[(i,i) for i in range(2018, datetime.now().year + 2)])

class copyClassForm(forms.Form):
    class_name = forms.CharField(max_length=50)
    quarter = forms.ChoiceField(choices=SEASONS)
    year = forms.ChoiceField(choices=[(i,i) for i in range(2018, datetime.now().year + 2)])

class createPollForm(forms.Form):
    possible_answers = forms.ChoiceField(choices=[(i,i) for i in range(2,13)], label="# of options for this poll")

class attendanceFormForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

class settingForm(forms.Form):
    email = forms.CharField(max_length=50, required=False)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
