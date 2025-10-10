from django.contrib import admin
from .models import Department, Role, DepartmentMember

class DepartmentMemberInline(admin.TabularInline):
    """
    Inline admin descriptor for DepartmentMember
    This allows editing of DepartmentMember from the Department admin page.
    """
    model = DepartmentMember
    extra = 1  # Number of empty forms to display

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'church', 'updated_at')
    list_filter = ('church',)
    search_fields = ('name', 'church__name')
    inlines = [DepartmentMemberInline]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(DepartmentMember)
class DepartmentMemberAdmin(admin.ModelAdmin):
    list_display = ('member', 'department', 'role', 'start_date', 'end_date')
    list_filter = ('department', 'role', 'start_date', 'end_date')