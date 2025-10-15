from django.urls import path
from . import views

app_name = 'meetings'



urlpatterns = [

    path('', views.audiences_list, name='audiences_list'),

    path('summary/', views.audiences_summary, name='audiences_summary'),

    path('report/', views.audience_report, name='audience_report'),

    path('audiences/new/', views.AudienceCreateView.as_view(), name='audience_create'),

    path('audiences/<int:pk>/edit/', views.AudienceUpdateView.as_view(), name='audience_update'),

    path('audiences/<int:pk>/delete/', views.AudienceDeleteView.as_view(), name='audience_delete'),



    path('meetings/', views.MeetingListView.as_view(), name='meeting_list'),

    path('meetings/new/', views.MeetingCreateView.as_view(), name='meeting_create'),

    path('meetings/<int:pk>/edit/', views.MeetingUpdateView.as_view(), name='meeting_update'),

    path('meetings/<int:pk>/delete/', views.MeetingDeleteView.as_view(), name='meeting_delete'),



    path('events/', views.EventListView.as_view(), name='event_list'),

    path('events/new/', views.EventCreateView.as_view(), name='event_create'),

    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),

    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),



    path('attendances/', views.AttendanceListView.as_view(), name='attendance_list'),

    path('attendances/new/', views.AttendanceCreateView.as_view(), name='attendance_create'),

    path('attendances/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_update'),

    path('attendances/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),


]












