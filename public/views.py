from django.shortcuts import render

# Create your views here.


def accueil(request):
    return render(request, 'public/accueil.html')

def apropos(request):
    return render(request, 'public/apropos.html')

def produits(request):
    return render(request, 'public/produits.html')

from django.shortcuts import render, redirect
from django.urls import reverse


def commande(request):
    # Si l'utilisateur est connecté et non staff, on le redirige vers le formulaire de commande
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        return redirect('passer_commande')

    # Utilisateur non authentifié : afficher l'incitation à se connecter / inscrire
    next_url = reverse('passer_commande')
    return render(request, 'public/commande_prompt.html', {'next': next_url})

def contact(request):
    return render(request, 'public/contact.html')
