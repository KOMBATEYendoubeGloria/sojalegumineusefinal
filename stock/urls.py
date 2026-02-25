from django.urls import path
from .views import liste_stock, ajouter_stock, modifier_stock, supprimer_stock, liste_mouvements

urlpatterns = [
    path('stock/', liste_stock, name='stock'),
    path('stock/mouvements/', liste_mouvements, name='liste_mouvements'),
    path('stock/ajouter/', ajouter_stock, name='ajouter_stock'),
    path('stock/modifier/<int:pk>/', modifier_stock, name='modifier_stock'),
    path('stock/supprimer/<int:pk>/', supprimer_stock, name='supprimer_stock'),
]
