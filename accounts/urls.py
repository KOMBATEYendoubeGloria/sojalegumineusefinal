from django.urls import path
from .views import ConnexionView, DeconnexionView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', ConnexionView.as_view(), name='login'),
    path('logout/', DeconnexionView.as_view(), name='logout'),
]
