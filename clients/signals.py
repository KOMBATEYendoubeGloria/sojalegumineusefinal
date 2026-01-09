from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfilClient

@receiver(post_save, sender=User)
def creer_profil_client(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        ProfilClient.objects.create(user=instance)
