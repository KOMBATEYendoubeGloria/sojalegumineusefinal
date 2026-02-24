from django.db import models

class Notification(models.Model):
    TYPES = [
        ('STOCK', 'Alerte Stock'),
        ('COMMANDE', 'Alerte Commande'),
    ]
    
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPES)
    target_id = models.IntegerField(null=True, blank=True, help_text="ID de l'objet lié (Stock ou Commande)")
    date_creation = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)
    
    @property
    def target_url(self):
        from django.urls import reverse
        if self.type == 'STOCK':
            return reverse('stock')
        elif self.type == 'COMMANDE':
            return reverse('commandes')
        return "#"

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {'Lue' if self.est_lu else 'Non lue'}"
