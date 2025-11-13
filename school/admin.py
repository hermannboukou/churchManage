from django.contrib import admin
from .models import (
    Promotion, Session, Module, Student, Enrollment,
    Assignment, AssignmentSubmission, Exam, ExamResult
)

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

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    fields = ('session', 'status', 'final_grade', 'remarks')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_number', 'get_member_name', 'status', 'enrollment_date', 'updated_at')
    search_fields = ('student_number', 'member__first_name', 'member__last_name')
    list_filter = ('status', 'enrollment_date')
    inlines = [EnrollmentInline]
    
    def get_member_name(self, obj):
        return f"{obj.member.first_name} {obj.member.last_name}"
    get_member_name.short_description = "Nom du membre"

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'final_grade', 'enrollment_date')
    search_fields = ('student__student_number', 'student__member__first_name', 'student__member__last_name', 'session__name')
    list_filter = ('status', 'session', 'enrollment_date')

class AssignmentSubmissionInline(admin.TabularInline):
    model = AssignmentSubmission
    extra = 0
    fields = ('student', 'submitted_at', 'score', 'feedback')
    readonly_fields = ('submitted_at',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'due_date', 'max_score', 'created_at')
    search_fields = ('title', 'module__title', 'module__session__name')
    list_filter = ('module__session', 'due_date')
    inlines = [AssignmentSubmissionInline]

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'score', 'graded_by', 'is_late')
    search_fields = ('student__student_number', 'student__member__first_name', 'assignment__title')
    list_filter = ('submitted_at', 'graded_by')
    readonly_fields = ('submitted_at', 'is_late')

class ExamResultInline(admin.TabularInline):
    model = ExamResult
    extra = 0
    fields = ('student', 'score', 'remarks', 'graded_by')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'exam_date', 'duration', 'max_score', 'location')
    search_fields = ('title', 'module__title', 'module__session__name')
    list_filter = ('module__session', 'exam_date')
    inlines = [ExamResultInline]

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score', 'percentage', 'graded_by', 'graded_at')
    search_fields = ('student__student_number', 'student__member__first_name', 'exam__title')
    list_filter = ('exam__module', 'graded_at')
    readonly_fields = ('percentage',)
