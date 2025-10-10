from django.contrib import admin
from .models import Meeting, Event, Audiences, Attendance # Import all models

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at')
    search_fields = ('name',)
    list_filter = ('updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'meeting', 'church', 'start_datetime', 'end_datetime')
    search_fields = ('title', 'church__name')
    list_filter = ('start_datetime', 'meeting', 'church')
    ordering = ('-start_datetime',)
    # autocomplete_fields = ('meeting', 'church') # Removed to avoid errors

@admin.register(Audiences)
class AudiencesAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'day', 'church', 'total', 'men_count', 'women_count', 'youth_count', 'children_count', 'visitors_count')
    list_filter = ('meeting', 'day', 'church')
    search_fields = ('meeting__name', 'church__name')
    date_hierarchy = 'day'
    readonly_fields = ('created_at', 'updated_at')

    def total(self, obj):
        return obj.total
    total.short_description = "Total"

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('event', 'member', 'is_present', 'notes', 'updated_at')
    list_filter = ('event', 'member', 'is_present')
    search_fields = ('event__title', 'member__first_name', 'member__last_name')
    readonly_fields = ('created_at', 'updated_at')
    # autocomplete_fields = ('event', 'member') # Removed to avoid errors