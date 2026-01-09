from django.urls import path
from .views import liste_commandes, passer_commande, mes_commandes, changer_statut_commande

urlpatterns = [
    path('commandes/', liste_commandes, name='commandes'),
    path('passer/', passer_commande, name='passer_commande'),
    path('mes/', mes_commandes, name='mes_commandes'),
    path('<int:commande_id>/statut/', changer_statut_commande, name='changer_statut'),
]
