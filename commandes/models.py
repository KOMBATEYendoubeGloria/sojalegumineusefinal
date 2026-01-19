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
    
    def save(self, *args, **kwargs):
        # Import inside method to avoid potential circular imports
        from stock.models import Stock
        
        # Check if it's an existing instance to compare status
        if self.pk:
            old_instance = Commande.objects.get(pk=self.pk)
            old_statut = old_instance.statut
        else:
            old_statut = 'En attente' # Default for new

        new_statut = self.statut

        # Define states where stock should be deducted
        deducted_states = ['Confirmée', 'En livraison', 'Livrée']
        # Define states where stock should be present (not deducted)
        raw_states = ['En attente', 'Annulée']

        # Determine direction
        should_deduct = (new_statut in deducted_states) and (old_statut in raw_states)
        should_restore = (new_statut in raw_states) and (old_statut in deducted_states)

        stock_entry = Stock.objects.filter(legumineuse=self.legumineuse).first()

        if stock_entry:
            if should_deduct:
                stock_entry.quantite_disponible -= self.quantite
                stock_entry.save()
            elif should_restore:
                stock_entry.quantite_disponible += self.quantite
                stock_entry.save()
        
        super().save(*args, **kwargs)

