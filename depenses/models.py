from django.db import models

# Create your models here.
from django.db import models
from production.models import Legumineuse

class Depense(models.Model):
    type_depense = models.CharField(max_length=100)
    montant = models.FloatField()
    date = models.DateField()
    legumineuse = models.ForeignKey(Legumineuse, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.type_depense} - {self.montant} FCFA"
