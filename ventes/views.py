from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Vente

@login_required
def liste_ventes(request):
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    ventes = Vente.objects.all().order_by('-date')
    
    if date_debut:
        ventes = ventes.filter(date__gte=date_debut)
    if date_fin:
        ventes = ventes.filter(date__lte=date_fin)
        
    return render(request, 'ventes/liste_ventes.html', {
        'ventes': ventes,
        'date_debut': date_debut,
        'date_fin': date_fin
    })

@login_required
def supprimer_vente(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    if request.method == 'POST':
        vente.delete()
        return redirect('ventes')
    return render(request, 'ventes/confirm_delete_vente.html', {'vente': vente})
