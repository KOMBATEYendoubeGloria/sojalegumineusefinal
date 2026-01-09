from django.urls import path
from .views import liste_stock

urlpatterns = [
    path('stock/', liste_stock, name='stock'),
]
