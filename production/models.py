from django.db import models

# Create your models here.
class Section(models.Model):
    nom = models.CharField(max_length=100)
    superficie = models.FloatField()
    employe = models.ForeignKey('Employe', on_delete=models.SET_NULL, null=True, blank=True, related_name='sections')

    def __str__(self):
        return self.nom

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    date_ajout = models.DateField(auto_now_add=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')

    def __str__(self):
        return self.nom
    

    
class Legumineuse(models.Model):
    nom = models.CharField(max_length=100)
    prix_unitaire = models.FloatField(null=True, blank=True, help_text="Prix unitaire en FCFA")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='legumineuses_cultures')

    def __str__(self):
        return self.nom
    
class Recolte(models.Model):
    legumineuse = models.ForeignKey(Legumineuse, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name='recoltes')
    quantite = models.FloatField(help_text="Quantité en kg")
    date = models.DateField()
    qualite = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.legumineuse.nom} - {self.date}"

