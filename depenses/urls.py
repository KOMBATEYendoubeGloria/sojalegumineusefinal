from django.urls import path
from .views import liste_depenses

urlpatterns = [
    path('depenses/', liste_depenses, name='depenses'),
]
