from .models import Notification
from .utils import check_and_create_alerts
from django.utils import timezone
from stock.models import Stock
from commandes.models import Commande

def notifications_processor(request):
    if request.user.is_authenticated and request.user.is_staff:
        # On vérifie les alertes à chaque chargement de page
        check_and_create_alerts()
        
        today = timezone.now().date()
        
        # Alertes Stock Bas (Directement depuis le modèle)
        low_stock_qs = Stock.objects.filter(quantite_disponible__lte=50)
        stock_alerts_count = low_stock_qs.count()
        alert_stock_ids = list(low_stock_qs.values_list('id', flat=True))
        
        # Alertes Commandes en retard (Directement depuis le modèle)
        # Expirees mais pas encore livrées/annulées
        overdue_qs = Commande.objects.filter(
            date_livraison_prevue__lt=today
        ).exclude(statut__in=['Livrée', 'Annulée'])
        commande_alerts_count = overdue_qs.count()
        alert_commande_ids = list(overdue_qs.values_list('id', flat=True))
        
        notifications = Notification.objects.filter(est_lu=False)
        
        return {
            'global_notifications': notifications,
            'global_stock_alerts_count': stock_alerts_count,
            'global_commande_alerts_count': commande_alerts_count,
            'alert_stock_ids': alert_stock_ids,
            'alert_commande_ids': alert_commande_ids,
        }
    return {}
