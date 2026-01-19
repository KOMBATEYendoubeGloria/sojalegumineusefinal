from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stock
from .forms import StockForm

@login_required
def liste_stock(request):
    stocks = Stock.objects.all()
    return render(request, 'stock/liste_stock.html', {'stocks': stocks})

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
                form.save()
                
            return redirect('stock')
    else:
        form = StockForm()
    return render(request, 'stock/ajouter_stock.html', {'form': form, 'title': 'Ajouter du Stock'})

@login_required
def modifier_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
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
