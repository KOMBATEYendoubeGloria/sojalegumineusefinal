from django.urls import path
from .views import liste_depenses, ajouter_depense, modifier_depense, supprimer_depense

urlpatterns = [
    path('depenses/', liste_depenses, name='depenses'),
    path('depenses/ajouter/', ajouter_depense, name='ajouter_depense'),
    path('depenses/modifier/<int:pk>/', modifier_depense, name='modifier_depense'),
    path('depenses/supprimer/<int:pk>/', supprimer_depense, name='supprimer_depense'),
]
