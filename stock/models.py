from django.db import models

# Create your models here.
from django.db import models
from production.models import Legumineuse

class Stock(models.Model):
    legumineuse = models.ForeignKey(Legumineuse, on_delete=models.CASCADE)
    quantite_disponible = models.FloatField(help_text="Quantité en kg")
    date_mise_a_jour = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.legumineuse.nom} - {self.quantite_disponible} kg"
