from django.db import models
from core.models import Country

# Create your models here.
class Church(models.Model):
    name = models.CharField(max_length=200, unique=True)
    responsable = models.CharField(max_length=200, null=True, blank=True)
    
    # Assuming Pays is another model  
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False, default=1)
    
    # Self-referential ForeignKey for hierarchical structure
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    ville = models.CharField(max_length=200)
    quartier = models.CharField(max_length=200)
    nombre = models.IntegerField()
    creation = models.DateField()
    resume = models.TextField(null=True, blank=True, max_length=255)
    infos = models.TextField(null=True, blank=True, max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Church"
        verbose_name_plural = "Churches"