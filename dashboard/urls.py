from django.urls import path
from .views import dashboard, statistiques, commandes_livraisons, marquer_notification_lue

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('commandes/', commandes_livraisons, name='dashboard_commandes'),
    path('statistiques/', statistiques, name='statistiques'),
    path('notification/lue/<int:pk>/', marquer_notification_lue, name='marquer_notification_lue'),
]
