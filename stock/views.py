from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Stock

@login_required
def liste_stock(request):
    stocks = Stock.objects.all()
    return render(request, 'stock/liste_stock.html', {'stocks': stocks})
