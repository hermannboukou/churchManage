from django.contrib import admin
from .models import Promotion, Session, Module

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    # autocomplete_fields = ['promotion'] # Removed to avoid errors

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    # autocomplete_fields = ['session', 'teacher'] # Removed to avoid errors

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'updated_at')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')
    inlines = [SessionInline]

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'promotion', 'start_date', 'end_date', 'updated_at')
    search_fields = ('name', 'promotion__name')
    list_filter = ('promotion', 'start_date', 'end_date')
    inlines = [ModuleInline]
    # autocomplete_fields = ['promotion'] # Removed to avoid errors

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'teacher', 'coefficient', 'updated_at')
    search_fields = ('title', 'session__name', 'teacher__first_name', 'teacher__last_name')
    list_filter = ('session', 'teacher')
    # autocomplete_fields = ['session', 'teacher'] # Removed to avoid errors