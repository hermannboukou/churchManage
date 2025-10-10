from django.db import models
from django.contrib.auth.models import User
from core.models import Country
from datetime import date, timedelta # New import
from simple_history.models import HistoricalRecords # New import

class MemberQuerySet(models.QuerySet):
    def birthdays_in_next_days(self, days=7):
        today = date.today()
        upcoming_birthdays = []

        for member in self.filter(date_of_birth__isnull=False):
            # Get the member's birthday for the current year
            member_birthday_this_year = member.date_of_birth.replace(year=today.year)

            # If the birthday has already passed this year, consider next year's birthday
            if member_birthday_this_year < today:
                member_birthday_this_year = member_birthday_this_year.replace(year=today.year + 1)

            # Calculate the difference
            days_until_birthday = (member_birthday_this_year - today).days

            if 0 <= days_until_birthday <= days:
                upcoming_birthdays.append(member)
        return upcoming_birthdays

class Member(models.Model):
    objects = MemberQuerySet.as_manager() # Add the custom manager
    history = HistoricalRecords() # Add historical records
    # Link to the Django's built-in User model for authentication
    # This is optional, as not every member will have a login account.
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Compte utilisateur")

    # Basic Information
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    photo = models.ImageField(upload_to='member_photos/', null=True, blank=True, verbose_name="Photo")
    gender = models.CharField(max_length=10, choices=[('Male', 'Homme'), ('Female', 'Femme')], verbose_name="Sexe")
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    
    # Contact Information
    email = models.EmailField(max_length=254, unique=True, verbose_name="Adresse e-mail")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="Pays de nationalité")

    # Church-related Information
    class MemberStatus(models.TextChoices):
        PASTOR = 'PASTOR', 'Pasteur'
        ELDER = 'ELDER', 'Ancien'
        DEACON = 'DEACON', 'Diacre'
        LEADER = 'LEADER', 'Responsable'
        MEMBER = 'MEMBER', 'Membre'
        ASPIRANT = 'ASPIRANT', 'Aspirant'
        NOTHING = 'NOTHING', 'Nothing'

    status = models.CharField(
        max_length=20,
        choices=MemberStatus.choices,
        default=MemberStatus.MEMBER,
        verbose_name="Statut"
    )

    is_active = models.BooleanField(default=True, verbose_name="Membre actif")

    # Other Information
    profession = models.CharField(max_length=100, blank=True, verbose_name="Profession")
    
    class MaritalStatus(models.TextChoices):
        SINGLE = 'SINGLE', 'Célibataire'
        MARRIED = 'MARRIED', 'Marié(e)'
        DIVORCED = 'DIVORCED', 'Divorcé(e)'
        WIDOWED = 'WIDOWED', 'Veuf(ve)'

    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatus.choices,
        blank=True,
        verbose_name="État civil"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ['last_name', 'first_name']