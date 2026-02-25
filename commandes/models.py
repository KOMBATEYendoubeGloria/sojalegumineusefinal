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
        
        # Check if it's an existing instance to compare status and quantity
        if self.pk:
            try:
                old_instance = Commande.objects.get(pk=self.pk)
                old_statut = old_instance.statut
                old_quantite = old_instance.quantite
            except Commande.DoesNotExist:
                old_statut = 'En attente'
                old_quantite = 0
        else:
            old_statut = 'En attente'
            old_quantite = 0

        new_statut = self.statut
        new_quantite = self.quantite

        # States where stock is considered "taken" from inventory
        taken_states = ['Confirmée', 'En livraison', 'Livrée']
        # States where stock is considered "available" in inventory
        available_states = ['En attente', 'Annulée']

        stock_entry = Stock.objects.filter(legumineuse=self.legumineuse).first()

        if stock_entry:
            # Import MouvementStock here to avoid circular imports
            from stock.models import MouvementStock
            
            # Moving from AVAILABLE to TAKEN -> Deduct the new quantity
            if (old_statut in available_states) and (new_statut in taken_states):
                stock_entry.quantite_disponible -= new_quantite
                stock_entry.save()
                
                MouvementStock.objects.create(
                    legumineuse=self.legumineuse,
                    type_mouvement='SORTIE',
                    quantite=new_quantite,
                    motif=f"Commande confirmée - {self.client.username}"
                )
            
            # Moving from TAKEN to AVAILABLE -> Restore the old quantity
            elif (old_statut in taken_states) and (new_statut in available_states):
                stock_entry.quantite_disponible += old_quantite
                stock_entry.save()
                
                MouvementStock.objects.create(
                    legumineuse=self.legumineuse,
                    type_mouvement='ENTREE',
                    quantite=old_quantite,
                    motif=f"Commande annulée/remise en attente - {self.client.username}"
                )
            
            # Staying within TAKEN states but changing QUANTITY -> Adjust the difference
            elif (old_statut in taken_states) and (new_statut in taken_states) and (old_quantite != new_quantite):
                diff = new_quantite - old_quantite
                stock_entry.quantite_disponible -= diff
                stock_entry.save()
                
                MouvementStock.objects.create(
                    legumineuse=self.legumineuse,
                    type_mouvement='SORTIE' if diff > 0 else 'ENTREE',
                    quantite=abs(diff),
                    motif=f"Mise à jour quantité commande - {self.client.username}"
                )
        
        super().save(*args, **kwargs)
