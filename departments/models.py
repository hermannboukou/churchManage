from django.db import models
from church.models import Church
from members.models import Member

class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom du département")
    description = models.TextField(blank=True, verbose_name="Description")
    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="departments", verbose_name="Église")
    members = models.ManyToManyField(Member, through='DepartmentMember', related_name='departments', verbose_name="Membres")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.church.name})"

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        unique_together = ('name', 'church')

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du rôle")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"

class DepartmentMember(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Membre")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Département")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name="Rôle")
    
    start_date = models.DateField(verbose_name="Date de prise de fonction")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin de fonction")

    class Meta:
        verbose_name = "Membre de département"
        verbose_name_plural = "Membres de départements"
        unique_together = ('member', 'department', 'role')

    def __str__(self):
        return f"{self.member} - {self.department.name} ({self.role.name})"