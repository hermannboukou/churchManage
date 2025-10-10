from django.contrib import admin
from .models import Church

@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ('name', 'responsable', 'country', 'ville', 'parent', 'updated_at')
    search_fields = ('name', 'ville', 'responsable', 'country__name')
    list_filter = ('country', 'ville', 'created_at')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
