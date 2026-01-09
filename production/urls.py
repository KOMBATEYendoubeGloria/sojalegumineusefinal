from django.urls import path
from .views import liste_employes, liste_legumineuses, liste_recoltes
    
urlpatterns = [
    path('employes/', liste_employes, name='employes'),
    path('legumineuses/', liste_legumineuses, name='legumineuses'),
    path('recoltes/', liste_recoltes, name='recoltes'),
]
