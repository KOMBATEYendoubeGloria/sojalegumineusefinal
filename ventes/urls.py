from django.urls import path
from .views import liste_ventes, supprimer_vente

urlpatterns = [
    path('ventes/', liste_ventes, name='ventes'),
    path('ventes/supprimer/<int:pk>/', supprimer_vente, name='supprimer_vente'),
]
