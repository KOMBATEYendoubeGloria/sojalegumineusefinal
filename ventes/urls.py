from django.urls import path
from .views import liste_ventes

urlpatterns = [
    path('ventes/', liste_ventes, name='ventes'),
]
