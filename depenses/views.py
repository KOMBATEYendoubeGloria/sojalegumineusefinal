from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Depense
from .forms import DepenseForm

@login_required
def liste_depenses(request):
    depenses = Depense.objects.all()
    return render(request, 'depenses/liste_depenses.html', {'depenses': depenses})

@login_required
def ajouter_depense(request):
    if request.method == 'POST':
        form = DepenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('depenses')
    else:
        form = DepenseForm()
    return render(request, 'depenses/ajouter_depense.html', {'form': form, 'title': 'Ajouter une Dépense'})

@login_required
def modifier_depense(request, pk):
    depense = get_object_or_404(Depense, pk=pk)
    if request.method == 'POST':
        form = DepenseForm(request.POST, instance=depense)
        if form.is_valid():
            form.save()
            return redirect('depenses')
    else:
        form = DepenseForm(instance=depense)
    return render(request, 'depenses/ajouter_depense.html', {'form': form, 'title': 'Modifier une Dépense'})

@login_required
def supprimer_depense(request, pk):
    depense = get_object_or_404(Depense, pk=pk)
    if request.method == 'POST':
        depense.delete()
        return redirect('depenses')
    return render(request, 'production/confirm_delete.html', {'objet': f"la dépense de {depense.montant}", 'cancel_url': 'depenses'})
