from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from production.models import Legumineuse, Recolte
from ventes.models import Vente
from depenses.models import Depense
from stock.models import Stock
from commandes.models import Commande
from django.contrib.auth.models import User
import json

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


@login_required
def commandes_livraisons(request):
    # Accessible seulement par le staff
    if not request.user.is_staff:
        return redirect('mon_compte')

    # Regroupement des commandes par client
    clients = User.objects.filter(commandes__isnull=False).distinct()
    data = []
    for u in clients:
        commandes = u.commandes.all().order_by('-date_commande')
        data.append({'client': u, 'commandes': commandes})

    return render(request, 'dashboard/commandes_livraisons.html', {'clients_commandes': data})


@login_required
def statistiques(request):
    legumineuses = Legumineuse.objects.all()
    stats_legumineuses = []
    
    labels = []
    production_data = []
    stock_data = []
    ventes_data = []

    for c in legumineuses:
        # Production totale
        total_recolte = sum([r.quantite for r in Recolte.objects.filter(legumineuse=c)])
        # Stock disponible
        stock = Stock.objects.filter(legumineuse=c).first()
        quantite_stock = stock.quantite_disponible if stock else 0
        # Ventes
        total_ventes = sum([v.quantite for v in Vente.objects.filter(legumineuse=c)])
        # Rendement non calculable (champ superficie absent sur Legumineuse)
        rendement = 0

        stats_legumineuses.append({
            'legumineuse': c.nom,
            'total_recolte': total_recolte,
            'stock': quantite_stock,
            'total_ventes': total_ventes,
            'rendement': rendement
        })
        
        # Données pour les graphiques
        labels.append(c.nom)
        production_data.append(total_recolte)
        stock_data.append(quantite_stock)
        ventes_data.append(total_ventes)

    # Revenu total
    revenu_total = sum([v.revenu() for v in Vente.objects.all()])
    # Dépenses totales
    depenses_total = sum([d.montant for d in Depense.objects.all()])
    # Bilan
    bilan = revenu_total - depenses_total

    context = {
        'stats_legumineuses': stats_legumineuses,
        'revenu_total': revenu_total,
        'depenses_total': depenses_total,
        'bilan': bilan,
        'labels': json.dumps(labels),
        'production_data': json.dumps(production_data),
        'stock_data': json.dumps(stock_data),
        'ventes_data': json.dumps(ventes_data)
    }

    return render(request, 'dashboard/statistiques.html', context)
