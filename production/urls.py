from django.urls import path
from .views import (
    liste_employes, liste_legumineuses, liste_recoltes, liste_sections,
    ajouter_employe, modifier_employe, supprimer_employe,
    ajouter_legumineuse, modifier_legumineuse, supprimer_legumineuse,
    ajouter_recolte, modifier_recolte, supprimer_recolte,
    ajouter_section, modifier_section, supprimer_section, details_section
)
    
urlpatterns = [
    # Employes
    path('employes/', liste_employes, name='employes'),
    path('employes/ajouter/', ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:pk>/', modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:pk>/', supprimer_employe, name='supprimer_employe'),

    # Legumineuses
    path('legumineuses/', liste_legumineuses, name='legumineuses'),
    path('legumineuses/ajouter/', ajouter_legumineuse, name='ajouter_legumineuse'),
    path('legumineuses/modifier/<int:pk>/', modifier_legumineuse, name='modifier_legumineuse'),
    path('legumineuses/supprimer/<int:pk>/', supprimer_legumineuse, name='supprimer_legumineuse'),

    # Recoltes
    path('recoltes/', liste_recoltes, name='recoltes'),
    path('recoltes/ajouter/', ajouter_recolte, name='ajouter_recolte'),
    path('recoltes/modifier/<int:pk>/', modifier_recolte, name='modifier_recolte'),
    path('recoltes/supprimer/<int:pk>/', supprimer_recolte, name='supprimer_recolte'),

    # Sections
    path('sections/', liste_sections, name='sections'),
    path('sections/ajouter/', ajouter_section, name='ajouter_section'),
    path('sections/modifier/<int:pk>/', modifier_section, name='modifier_section'),
    path('sections/supprimer/<int:pk>/', supprimer_section, name='supprimer_section'),
    path('sections/details/<int:pk>/', details_section, name='details_section'),
]
