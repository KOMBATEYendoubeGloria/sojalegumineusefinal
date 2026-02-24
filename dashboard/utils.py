from django.utils import timezone
from stock.models import Stock
from commandes.models import Commande
from .models import Notification

def check_and_create_alerts():
    """
    Vérifie les stocks et les commandes en retard pour créer des notifications.
    """
    today = timezone.now().date()
    
    # 1. Gestion des Alertes Stock Bas (<= 50kg)
    # Récupérer tous les stocks
    all_stocks = Stock.objects.all()
    for s in all_stocks:
        titre = "Stock Bas"
        if s.quantite_disponible <= 50:
            message = f"Le stock de {s.legumineuse.nom} est de {s.quantite_disponible} kg (seuil de 50 kg)."
            # Créer seulement si aucune notification (lue ou non) n'existe déjà pour ce légume
            if not Notification.objects.filter(type='STOCK', message__contains=s.legumineuse.nom).exists():
                Notification.objects.create(
                    titre=titre,
                    message=message,
                    type='STOCK',
                    target_id=s.id
                )
        else:
            # Si le stock est remonté (> 50kg), on supprime les anciennes notifications 
            # pour permettre une nouvelle alerte si ça redescend plus tard
            Notification.objects.filter(type='STOCK', message__contains=s.legumineuse.nom).delete()

    # 2. Gestion des Alertes Retard de Livraison
    # Récupérer les identifiants des commandes actuellement en retard
    commandes_en_retard = Commande.objects.filter(
        date_livraison_prevue__lt=today,
        statut__in=['En attente', 'Confirmée', 'En livraison']
    )
    commandes_en_retard_ids = list(commandes_en_retard.values_list('id', flat=True))

    for c in commandes_en_retard:
        titre = "Retard de Livraison"
        message = f"La commande #{c.id} pour {c.legumineuse.nom} (Client: {c.client_nom or c.client.username}) était prévue pour le {c.date_livraison_prevue}."
        # Créer seulement si aucune notification n'existe pour cette commande précise
        if not Notification.objects.filter(type='COMMANDE', message__contains=f"#{c.id}").exists():
            Notification.objects.create(
                titre=titre,
                message=message,
                type='COMMANDE',
                target_id=c.id
            )
    
    # Nettoyer les notifications de commandes qui ne sont plus en retard (livrées, annulées ou date modifiée)
    # On cherche les notifications de type COMMANDE dont l'ID de commande n'est plus dans la liste des retards
    # Note: On extrait l'ID du message "#ID"
    all_commande_notes = Notification.objects.filter(type='COMMANDE')
    for note in all_commande_notes:
        import re
        match = re.search(r'#(\d+)', note.message)
        if match:
            cmd_id = int(match.group(1))
            if cmd_id not in commandes_en_retard_ids:
                note.delete()
