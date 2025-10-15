from django import forms
from .models import Meeting, Event, Audiences, Attendance

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['name', 'infos']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'meeting', 'church', 'start_datetime', 'end_datetime', 'description']

class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audiences
        fields = ['meeting', 'church', 'day', 'men_count', 'women_count', 'youth_count', 'children_count', 'visitors_count']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['event', 'member', 'is_present', 'notes']