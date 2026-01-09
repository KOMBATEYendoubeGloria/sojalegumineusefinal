from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Employe , Legumineuse, Recolte

@login_required
def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'production/liste_employes.html', {
        'employes': employes
    })

@login_required
def liste_legumineuses(request):
    legumineuses = Legumineuse.objects.all()
    return render(request, 'production/liste_legumineuses.html', {
        'legumineuses': legumineuses
    })

@login_required
def liste_recoltes(request):
    recoltes = Recolte.objects.all()
    return render(request, 'production/liste_recoltes.html', {
        'recoltes': recoltes
    })
