from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stock, MouvementStock
from .forms import StockForm

@login_required
def liste_stock(request):
    stocks = Stock.objects.all()
    return render(request, 'stock/liste_stock.html', {'stocks': stocks})

@login_required
def liste_mouvements(request):
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    mouvements = MouvementStock.objects.all().order_by('-date')
    
    if date_debut:
        mouvements = mouvements.filter(date__gte=date_debut)
    if date_fin:
        mouvements = mouvements.filter(date__lte=date_fin)
        
    return render(request, 'stock/liste_mouvements.html', {
        'mouvements': mouvements,
        'date_debut': date_debut,
        'date_fin': date_fin
    })

@login_required
def ajouter_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            # Check if stock exists for this legumineuse
            legumineuse = form.cleaned_data['legumineuse']
            quantite = form.cleaned_data['quantite_disponible']
            
            existing_stock = Stock.objects.filter(legumineuse=legumineuse).first()
            if existing_stock:
                existing_stock.quantite_disponible += quantite
                existing_stock.save()
            else:
                existing_stock = form.save()
            
            # Record movement
            MouvementStock.objects.create(
                legumineuse=legumineuse,
                type_mouvement='ENTREE',
                quantite=quantite,
                motif="Ajustement manuel (Ajout)"
            )
                
            return redirect('stock')
    else:
        form = StockForm()
    return render(request, 'stock/ajouter_stock.html', {'form': form, 'title': 'Ajouter du Stock'})

@login_required
def modifier_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    old_quantite = stock.quantite_disponible
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            new_stock = form.save()
            diff = new_stock.quantite_disponible - old_quantite
            
            if diff != 0:
                MouvementStock.objects.create(
                    legumineuse=new_stock.legumineuse,
                    type_mouvement='ENTREE' if diff > 0 else 'SORTIE',
                    quantite=abs(diff),
                    motif="Ajustement manuel (Modification)"
                )
            
            return redirect('stock')
    else:
        form = StockForm(instance=stock)
    return render(request, 'stock/ajouter_stock.html', {'form': form, 'title': 'Modifier le Stock'})

@login_required
def supprimer_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        stock.delete()
        return redirect('stock')
    return render(request, 'production/confirm_delete.html', {'objet': f"le stock de {stock.legumineuse.nom}", 'cancel_url': 'stock'})
