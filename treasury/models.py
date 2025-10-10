from django.db import models
from church.models import Church
from members.models import Member
from departments.models import Department # Assuming Department model is available
from simple_history.models import HistoricalRecords # New import

class CollectionType(models.Model):
    """Defines different types of collections (e.g., Dîmes, Offrandes, Projets)."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du type de collecte")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Type de collecte"
        verbose_name_plural = "Types de collecte"

class PaymentMethod(models.Model):
    """Defines different payment methods (e.g., Espèces, Mobile Money, Chèque, Virement)."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la méthode de paiement")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Méthode de paiement"
        verbose_name_plural = "Méthodes de paiement"

class Collection(models.Model):
    """Records individual collection entries."""
    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="collections", verbose_name="Église")
    collection_type = models.ForeignKey(CollectionType, on_delete=models.PROTECT, verbose_name="Type de collecte")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    date = models.DateField(verbose_name="Date de la collecte")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name="Méthode de paiement")
    
    # Donor can be a member or an guest (anonymous)
    donor_member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Donateur (Membre)")
    donor_guest_name = models.CharField(max_length=200, blank=True, verbose_name="Donateur (Invité)")
    
    # Optional link to a department
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Département associé")
    
    receipt_number = models.CharField(max_length=50, blank=True, unique=True, verbose_name="Numéro de reçu")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Who recorded the entry
    recorded_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="recorded_collections", verbose_name="Enregistré par")

    history = HistoricalRecords() # Add historical records
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        donor = self.donor_member if self.donor_member else self.donor_guest_name
        return f"{self.collection_type.name} - {self.amount} le {self.date} par {donor}"

    class Meta:
        verbose_name = "Collecte"
        verbose_name_plural = "Collectes"
        ordering = ['-date', '-created_at']