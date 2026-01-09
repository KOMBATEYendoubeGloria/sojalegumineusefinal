from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Vente

@login_required
def liste_ventes(request):
    ventes = Vente.objects.all()
    return render(request, 'ventes/liste_ventes.html', {'ventes': ventes})
