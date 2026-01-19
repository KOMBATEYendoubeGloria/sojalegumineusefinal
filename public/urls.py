from django.urls import path
from .views import accueil, apropos, produits, commande, contact

urlpatterns = [
    path('', accueil, name='accueil'),
    path('apropos/', apropos, name='apropos'),
    path('produits/', produits, name='produits'),
    path('info-commande/', commande, name='commande_public'),
    path('contact/', contact, name='contact'),
]
