from django.contrib import admin

from .models import CourseModule, Lesson, ModuleBadge, Pathway, Progress, Question


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 0
    fields = ("title", "order", "badge_name")


@admin.register(Pathway)
class PathwayAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "updated_at")
    search_fields = ("title", "slug")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CourseModuleInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ("title", "order", "requires_manual_validation", "passing_score")


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "pathway", "order", "badge_name")
    search_fields = ("title", "pathway__title")
    list_filter = ("pathway",)
    ordering = ("pathway", "order")
    inlines = [LessonInline]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ("order", "statement", "options", "correct_answer")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "requires_manual_validation", "passing_score")
    search_fields = ("title", "module__title", "module__pathway__title")
    list_filter = ("module__pathway", "requires_manual_validation")
    ordering = ("module__pathway", "module__order", "order")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("lesson", "order", "correct_answer")
    search_fields = ("lesson__title", "statement")
    list_filter = ("lesson__module__pathway",)
    ordering = ("lesson__module__pathway", "lesson__module__order", "lesson__order", "order")


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "status", "score", "quiz_passed", "instructor_validated", "completed_at")
    search_fields = ("user__username", "lesson__title")
    list_filter = ("status", "quiz_passed", "instructor_validated", "lesson__module__pathway")
    ordering = ("-updated_at",)


@admin.register(ModuleBadge)
class ModuleBadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "module", "awarded_at")
    search_fields = ("user__username", "module__title")
    list_filter = ("module__pathway",)
    ordering = ("-awarded_at",)
