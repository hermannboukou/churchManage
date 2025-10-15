# Create your models here.
from django.db import models


# Create your models here.
class Country(models.Model):
    # Nom du pays
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du pays")

    # Code du pays (exemple : "FR" pour la France, "US" pour les États-Unis)
    code = models.CharField(max_length=2, unique=True, verbose_name="Code du pays",
                            help_text="Code ISO à 2 lettres (ex: FR, US)")

    # Indicatif téléphonique du pays (optionnel)
    phone_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="Indicatif téléphonique",
                                  help_text="Exemple: +33 pour la France")

    # Date de création et de mise à jour
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"
        ordering = ['name']  # Trier les pays par nom par défaut
