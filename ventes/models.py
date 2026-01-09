from django.db import models

# Create your models here.
from django.db import models
from production.models import Legumineuse 

class Vente(models.Model):
    legumineuse = models.ForeignKey(Legumineuse, on_delete=models.CASCADE)
    quantite = models.FloatField(help_text="Quantité vendue en kg")
    prix_unitaire = models.FloatField(help_text="Prix par kg")
    client = models.CharField(max_length=100)
    date = models.DateField()
    commande = models.OneToOneField('commandes.Commande', null=True, blank=True, on_delete=models.SET_NULL, related_name='vente')
    client_telephone = models.CharField(max_length=20, blank=True, null=True)
    client_adresse = models.CharField(max_length=255, blank=True, null=True)

    def revenu(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.legumineuse.nom} - {self.client} - {self.date}"
