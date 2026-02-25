from django.db import models

# Create your models here.
from django.db import models
from production.models import Legumineuse

class Stock(models.Model):
    legumineuse = models.ForeignKey(Legumineuse, on_delete=models.CASCADE)
    quantite_disponible = models.FloatField(help_text="Quantité en kg")
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.legumineuse.nom} - {self.quantite_disponible} kg"

class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]
    legumineuse = models.ForeignKey(Legumineuse, on_delete=models.CASCADE)
    type_mouvement = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantite = models.FloatField(help_text="Quantité en kg")
    date = models.DateTimeField(auto_now_add=True)
    motif = models.CharField(max_length=255, help_text="Ex: Récolte, Vente, Ajustement manuel")

    def __str__(self):
        return f"{self.type_mouvement} - {self.legumineuse.nom} - {self.quantite} kg"
