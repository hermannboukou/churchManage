from django.contrib import admin
from .models import Country

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone_code', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
