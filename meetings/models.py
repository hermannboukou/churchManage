from django.db import models
from django.core.validators import MinValueValidator # For Audiences model
from church.models import Church
from members.models import Member # For Attendance model

# Create your models here.
class Meeting(models.Model):
    # Nom de la réunion (unique pour éviter les doublons)
    name = models.CharField(max_length=200, unique=True, verbose_name="Nom de la réunion")
    
    # Informations supplémentaires sur la réunion (optionnel)
    infos = models.TextField(null=True, blank=True, max_length=255, verbose_name="Informations supplémentaires")
    
    # Date et heure de création (automatiquement ajoutée à la création)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    # Date et heure de mise à jour (automatiquement mise à jour à chaque modification)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    # Méthode pour afficher le nom de la réunion dans l'interface admin et autres endroits
    def __str__(self):
        return self.name

    class Meta:
        # Nom pluriel pour l'interface d'administration
        verbose_name_plural = "Meetings"
        
        # Trier les réunions par date de création par défaut
        ordering = ['-created_at']


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de l'événement")
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT, verbose_name="Type de réunion")
    church = models.ForeignKey(Church, on_delete=models.CASCADE, verbose_name="Église")
    
    start_datetime = models.DateTimeField(verbose_name="Date et heure de début")
    end_datetime = models.DateTimeField(verbose_name="Date et heure de fin")
    
    description = models.TextField(blank=True, verbose_name="Description / Ordre du jour")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} @ {self.church.name}"

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-start_datetime']


class Audiences(models.Model):
    men_count = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Nombre d'hommes"
    )
    women_count = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Nombre de femmes"
    )
    youth_count = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Nombre de jeunes"
    )
    children_count = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Nombre d'enfants"
    )
    visitors_count = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Nombre de visiteurs"
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Réunion"
    )
    day = models.DateField(verbose_name="Date")
    
    church = models.ForeignKey(
        Church,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Église"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return f"Audience for {self.meeting} on {self.day}"

    class Meta:
        ordering = ['-day']
        verbose_name = 'Audience'
        verbose_name_plural = 'Audiences'
        unique_together = ('meeting', 'day', 'church')

    @property
    def total(self):
        return self.men_count + self.women_count + self.youth_count + self.children_count + self.visitors_count

    def get_counts(self):
        return [
            self.men_count,
            self.women_count,
            self.youth_count,
            self.children_count,
            self.visitors_count,
            self.total
        ]

class Attendance(models.Model):
    """Records the attendance of a member at an event."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendances", verbose_name="Événement")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="attendances", verbose_name="Membre")
    is_present = models.BooleanField(default=True, verbose_name="Présent(e)")
    notes = models.TextField(blank=True, verbose_name="Notes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Présence"
        verbose_name_plural = "Présences"
        unique_together = ('event', 'member')
        ordering = ['event__start_datetime', 'member__last_name']

    def __str__(self):
        status = "Présent" if self.is_present else "Absent"
        return f"{self.member} - {self.event.title} ({status})"