from django.urls import path
from .views import dashboard , statistiques, commandes_livraisons

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('commandes/', commandes_livraisons, name='dashboard_commandes'),
    path('statistiques/', statistiques, name='statistiques'),
]
