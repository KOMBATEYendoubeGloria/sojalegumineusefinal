from django.db import models

# Create your models here.
class Section(models.Model):
    nom = models.CharField(max_length=100)
    superficie = models.FloatField()

    def __str__(self):
        return self.nom

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    date_ajout = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nom
    

    
class Legumineuse(models.Model):
    nom = models.CharField(max_length=100)
    prix_unitaire = models.FloatField(null=True, blank=True, help_text="Prix unitaire en FCFA")

    def __str__(self):
        return self.nom
    
class Recolte(models.Model):
    legumineuse = models.ForeignKey(Legumineuse, on_delete=models.CASCADE)
    quantite = models.FloatField(help_text="Quantité en kg")
    date = models.DateField()
    qualite = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.legumineuse.nom} - {self.date}"

