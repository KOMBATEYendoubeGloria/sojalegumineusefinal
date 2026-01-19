from django.urls import path
from .views import liste_stock, ajouter_stock, modifier_stock, supprimer_stock

urlpatterns = [
    path('stock/', liste_stock, name='stock'),
    path('stock/ajouter/', ajouter_stock, name='ajouter_stock'),
    path('stock/modifier/<int:pk>/', modifier_stock, name='modifier_stock'),
    path('stock/supprimer/<int:pk>/', supprimer_stock, name='supprimer_stock'),
]
