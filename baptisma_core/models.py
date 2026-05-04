from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify


class Pathway(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Titre")
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Parcours"
        verbose_name_plural = "Parcours"
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseModule(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="modules", verbose_name="Parcours")
    title = models.CharField(max_length=200, verbose_name="Titre")
    order = models.PositiveIntegerField(default=1, verbose_name="Ordre")
    description = models.TextField(blank=True, verbose_name="Description")
    illustration = models.ImageField(upload_to="baptisma/modules/", null=True, blank=True, verbose_name="Image")
    badge_name = models.CharField(max_length=100, blank=True, verbose_name="Nom du badge")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ["pathway", "order", "title"]
        unique_together = (("pathway", "order"), ("pathway", "title"))

    def __str__(self):
        return f"{self.pathway.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name="lessons", verbose_name="Module")
    title = models.CharField(max_length=200, verbose_name="Titre")
    order = models.PositiveIntegerField(default=1, verbose_name="Ordre")
    content = models.TextField(blank=True, verbose_name="Contenu")
    key_verse_reference = models.CharField(max_length=150, blank=True, verbose_name="Référence du verset clé")
    key_verse_text = models.TextField(blank=True, verbose_name="Texte du verset clé")
    requires_manual_validation = models.BooleanField(
        default=False,
        verbose_name="Validation manuelle requise (instructeur)"
    )
    passing_score = models.PositiveSmallIntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Score minimal (%)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Leçon"
        verbose_name_plural = "Leçons"
        ordering = ["module__order", "order", "title"]
        unique_together = (("module", "order"), ("module", "title"))

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions", verbose_name="Leçon")
    statement = models.TextField(verbose_name="Énoncé")
    options = models.JSONField(default=list, verbose_name="Options")
    correct_answer = models.CharField(max_length=255, verbose_name="Bonne réponse")
    explanation = models.TextField(blank=True, verbose_name="Explication")
    order = models.PositiveIntegerField(default=1, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["lesson", "order"]
        unique_together = (("lesson", "order"),)

    def clean(self):
        if not isinstance(self.options, list) or len(self.options) < 2:
            raise ValidationError({"options": "Les options doivent contenir au moins deux choix."})
        normalized_options = [str(option).strip() for option in self.options]
        if str(self.correct_answer).strip() not in normalized_options:
            raise ValidationError({"correct_answer": "La bonne réponse doit faire partie des options."})

    def is_correct(self, answer):
        return str(answer).strip() == str(self.correct_answer).strip()

    def __str__(self):
        return f"Q{self.order} - {self.lesson.title}"


class Progress(models.Model):
    class Status(models.TextChoices):
        LOCKED = "LOCKED", "Locked"
        CURRENT = "CURRENT", "Current"
        COMPLETED = "COMPLETED", "Completed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress_entries")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.LOCKED, verbose_name="Statut")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Score")
    quiz_passed = models.BooleanField(default=False, verbose_name="Quiz validé")
    instructor_validated = models.BooleanField(default=False, verbose_name="Validation instructeur")
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_learning_steps",
        verbose_name="Validé par"
    )
    validated_at = models.DateTimeField(null=True, blank=True, verbose_name="Validé le")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Terminé le")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Progression"
        verbose_name_plural = "Progressions"
        ordering = ["lesson__module__order", "lesson__order", "lesson__title"]
        unique_together = (("user", "lesson"),)

    def __str__(self):
        return f"{self.user} - {self.lesson} ({self.status})"

    def mark_completed(self, save=True):
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        if save:
            self.save(update_fields=["status", "completed_at", "updated_at"])

    def mark_quiz_result(self, score):
        self.score = score
        self.quiz_passed = score >= self.lesson.passing_score

        if self.quiz_passed and not self.lesson.requires_manual_validation:
            self.mark_completed(save=False)

        self.save(update_fields=["score", "quiz_passed", "status", "completed_at", "updated_at"])

        if self.status == self.Status.COMPLETED:
            self._unlock_next_lesson()
            self._award_module_badge_if_ready()

    def validate_manually(self, instructor):
        self.instructor_validated = True
        self.validated_by = instructor
        self.validated_at = timezone.now()
        self.mark_completed(save=False)
        self.save(
            update_fields=[
                "instructor_validated",
                "validated_by",
                "validated_at",
                "status",
                "completed_at",
                "updated_at",
            ]
        )
        self._unlock_next_lesson()
        self._award_module_badge_if_ready()

    def _unlock_next_lesson(self):
        lessons = list(
            Lesson.objects.filter(module__pathway=self.lesson.module.pathway)
            .select_related("module")
            .order_by("module__order", "order", "id")
        )
        lesson_ids = [item.id for item in lessons]

        if self.lesson_id not in lesson_ids:
            return

        current_idx = lesson_ids.index(self.lesson_id)
        next_idx = current_idx + 1
        if next_idx >= len(lesson_ids):
            return

        next_lesson = lessons[next_idx]
        next_progress, created = Progress.objects.get_or_create(
            user=self.user,
            lesson=next_lesson,
            defaults={"status": Progress.Status.CURRENT},
        )
        if not created and next_progress.status == Progress.Status.LOCKED:
            next_progress.status = Progress.Status.CURRENT
            next_progress.save(update_fields=["status", "updated_at"])

    def _award_module_badge_if_ready(self):
        module_lessons = list(self.lesson.module.lessons.values_list("id", flat=True))
        if not module_lessons:
            return
        completed_count = Progress.objects.filter(
            user=self.user,
            lesson_id__in=module_lessons,
            status=Progress.Status.COMPLETED,
        ).count()
        if completed_count == len(module_lessons):
            ModuleBadge.objects.get_or_create(user=self.user, module=self.lesson.module)


class ModuleBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="module_badges")
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name="badges")
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Badge module"
        verbose_name_plural = "Badges modules"
        unique_together = (("user", "module"),)
        ordering = ["-awarded_at"]

    def __str__(self):
        return f"{self.user} - {self.module.badge_name or self.module.title}"


def initialize_user_progress(user, pathway):
    lessons = list(
        Lesson.objects.filter(module__pathway=pathway)
        .select_related("module")
        .order_by("module__order", "order", "id")
    )
    if not lessons:
        return

    with transaction.atomic():
        existing_progress = {
            progress.lesson_id: progress
            for progress in Progress.objects.select_for_update().filter(user=user, lesson__in=lessons)
        }

        for index, lesson in enumerate(lessons):
            if lesson.id in existing_progress:
                continue
            Progress.objects.create(
                user=user,
                lesson=lesson,
                status=Progress.Status.CURRENT if index == 0 else Progress.Status.LOCKED,
            )

        has_current = Progress.objects.filter(
            user=user,
            lesson__in=lessons,
            status=Progress.Status.CURRENT
        ).exists()
        if not has_current:
            first_progress = Progress.objects.filter(user=user, lesson=lessons[0]).first()
            if first_progress and first_progress.status == Progress.Status.LOCKED:
                first_progress.status = Progress.Status.CURRENT
                first_progress.save(update_fields=["status", "updated_at"])
