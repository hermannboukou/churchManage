from django.contrib import admin
from .models import Member
# from simple_history.admin import HistoricalModelAdmin # New import

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'status', 'is_active', 'country', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active', 'status', 'gender', 'country', 'updated_at')
    ordering = ('last_name', 'first_name')
    
    # date_hierarchy = 'created_at'
    # readonly_fields = ('created_at', 'updated_at')

# @admin.register(Member.history.model) # Register the historical model
# class HistoricalMemberAdmin(HistoricalModelAdmin):
#     list_display = ('history_date', 'history_type', 'history_user', 'first_name', 'last_name', 'email')
#     list_filter = ('history_type', 'history_date', 'history_user')
#     search_fields = ('first_name', 'last_name', 'email')
