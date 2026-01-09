from django.db import models
from django.contrib.auth.models import User
from commandes.models import Commande
from django.utils import timezone

class Chauffeur(models.Model):
    """Modèle pour les chauffeurs/livreurs"""
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_livraison', 'En livraison'),
        ('indisponible', 'Indisponible'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    numero_permis = models.CharField(max_length=50, unique=True)
    date_embauche = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')
    vehicule = models.CharField(max_length=100, blank=True, help_text="Marque et modèle du véhicule")
    immatriculation = models.CharField(max_length=20, unique=True, blank=True)
    numero_contact_urgence = models.CharField(max_length=20, blank=True)
    actif = models.BooleanField(default=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name_plural = "Chauffeurs"
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def nombre_livraisons_aujourd_hui(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.livraisons.filter(date_livraison__date=today).count()


class Livraison(models.Model):
    """Modèle pour suivre les livraisons"""
    STATUT_CHOICES = [
        ('planifiée', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('livrée', 'Livrée'),
        ('échouée', 'Échouée'),
        ('annulée', 'Annulée'),
    ]
    
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, related_name='livraison')
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.SET_NULL, null=True, blank=True, related_name='livraisons')
    date_planifiee = models.DateTimeField()
    date_livraison = models.DateTimeField(null=True, blank=True, help_text="Date/heure réelle de livraison")
    adresse_livraison = models.TextField()
    notes_livraison = models.TextField(blank=True, help_text="Notes du chauffeur sur la livraison")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifiée')
    signature_client = models.TextField(blank=True, help_text="Données de signature en base64")
    photo_preuve = models.ImageField(upload_to='livraisons_photos/', blank=True, null=True)
    temperature = models.FloatField(null=True, blank=True, help_text="Température du produit à la livraison")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_planifiee']
        verbose_name_plural = "Livraisons"
    
    def __str__(self):
        return f"Livraison de {self.commande.legumineuse.nom} - {self.statut}"
    
    def delai_respectable(self):
        """Vérifie si la livraison a été effectuée dans les délais"""
        if self.date_livraison and self.commande.date_livraison_prevue:
            return self.date_livraison.date() <= self.commande.date_livraison_prevue
        return None


class HistoriqueLivraison(models.Model):
    """Modèle pour tracer l'historique des modifications de livraison"""
    livraison = models.ForeignKey(Livraison, on_delete=models.CASCADE, related_name='historique')
    ancien_statut = models.CharField(max_length=20)
    nouveau_statut = models.CharField(max_length=20)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_modification']
        verbose_name_plural = "Historiques de livraison"
    
    def __str__(self):
        return f"{self.livraison} - {self.ancien_statut} → {self.nouveau_statut}"
