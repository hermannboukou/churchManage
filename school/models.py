from django.db import models
from members.models import Member # For teacher in Module

class Promotion(models.Model):
    """Represents a group of students starting together (e.g., 'Promotion 2025')."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la promotion")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    description = models.TextField(blank=True, verbose_name="Description")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ['-start_date']

class Session(models.Model):
    """Represents a specific period of study within a promotion."""
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name="sessions", verbose_name="Promotion")
    name = models.CharField(max_length=100, verbose_name="Nom de la session")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    description = models.TextField(blank=True, verbose_name="Description")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.promotion.name})"

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
        unique_together = ('promotion', 'name') # Session name unique within a promotion
        ordering = ['-start_date']

class Module(models.Model):
    """Represents a course within a session."""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="modules", verbose_name="Session")
    title = models.CharField(max_length=200, verbose_name="Titre du module")
    description = models.TextField(blank=True, verbose_name="Description")
    teacher = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="taught_modules", verbose_name="Enseignant")
    resources = models.FileField(upload_to='school_resources/', null=True, blank=True, verbose_name="Ressources (PDF/Vidéo)")
    coefficient = models.DecimalField(max_digits=4, decimal_places=2, default=1.0, verbose_name="Coefficient")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.session.name})"

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        unique_together = ('session', 'title') # Module title unique within a session
        ordering = ['title']