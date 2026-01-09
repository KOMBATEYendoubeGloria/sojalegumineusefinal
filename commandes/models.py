from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
from production.models import Legumineuse

class Commande(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Confirmée', 'Confirmée'),
        ('En livraison', 'En livraison'),
        ('Livrée', 'Livrée'),
        ('Annulée', 'Annulée')
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    legumineuse = models.ForeignKey(Legumineuse, on_delete=models.CASCADE)
    quantite = models.FloatField(help_text="Quantité commandée en kg")
    date_commande = models.DateTimeField(default=timezone.now)
    date_livraison_prevue = models.DateField(null=True, blank=True, help_text="Date de livraison prévue")
    date_livraison_reelle = models.DateField(null=True, blank=True, help_text="Date de livraison réelle")
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='En attente')
    notes_staff = models.TextField(blank=True, help_text="Notes internes pour le staff")
    prix_unitaire = models.FloatField(null=True, blank=True, help_text="Prix unitaire en FCFA")
    client_nom = models.CharField(max_length=255, blank=True, null=True, help_text="Nom du client au moment de la commande")
    client_telephone = models.CharField(max_length=20, blank=True, null=True, help_text="Téléphone du client")
    client_adresse = models.CharField(max_length=255, blank=True, null=True, help_text="Adresse de livraison du client")
    
    class Meta:
        ordering = ['-date_commande']
        verbose_name_plural = "Commandes"

    def __str__(self):
        return f"{self.client.username} - {self.legumineuse.nom} - {self.statut}"
    
    def prix_total(self):
        if self.prix_unitaire:
            return self.quantite * self.prix_unitaire
        return 0
    
    def est_en_retard(self):
        if self.date_livraison_prevue and self.statut != 'Livrée':
            return self.date_livraison_prevue < timezone.now().date()
        return False

