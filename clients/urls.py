from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription_client, name='inscription_client'),
    path('compte/', views.mon_compte, name='mon_compte'),
]
