from django.urls import path
from .views import accueil, apropos, produits, commande, contact

urlpatterns = [
    path('', accueil, name='accueil'),
    path('apropos/', apropos, name='apropos'),
    path('produits/', produits, name='produits'),
    path('commande/', commande, name='commande'),
    path('contact/', contact, name='contact'),
]
