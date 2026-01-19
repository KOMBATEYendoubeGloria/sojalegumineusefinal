from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from production.models import Legumineuse, Recolte
from ventes.models import Vente
from depenses.models import Depense
from stock.models import Stock
from commandes.models import Commande
from django.contrib.auth.models import User
import json

def get_legume_colors(labels):
    """Génère une palette de couleurs cohérente pour une liste de labels."""
    palette = [
        '#e74c3c', # Rouge
        '#3498db', # Bleu
        '#2ecc71', # Vert
        '#f39c12', # Orange
        '#9b59b6', # Violet
        '#1abc9c', # Turquoise
        '#34495e', # Gris foncé
        '#d35400', # Orange foncé
        '#8e44ad', # Pourpre
        '#2c3e50', # Bleu nuit
    ]
    # Si on a plus de labels que de couleurs, on boucle
    return [palette[i % len(palette)] for i in range(len(labels))]

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('mon_compte') 

    # KPIs Globaux
    revenu_total = sum([v.revenu() for v in Vente.objects.all()]) or 0
    depenses_total = sum([d.montant for d in Depense.objects.all()]) or 0
    bilan = revenu_total - depenses_total
    
    # Commandes en attente
    commandes_attente = Commande.objects.filter(statut='En attente').count()

    # Données pour les graphiques (Par nom de légumineuse)
    legumineuses = Legumineuse.objects.all()
    data_map = {}

    for leg in legumineuses:
        name = leg.nom.strip()
        if name not in data_map:
            data_map[name] = {'production': 0, 'ventes': 0, 'stock': 0}
        
        # Production
        total_prod = sum([r.quantite for r in Recolte.objects.filter(legumineuse=leg)])
        data_map[name]['production'] += total_prod
        
        # Ventes
        total_vente = sum([v.quantite for v in Vente.objects.filter(legumineuse=leg)])
        data_map[name]['ventes'] += total_vente
        
        # Stock
        total_stock = sum([s.quantite_disponible for s in Stock.objects.filter(legumineuse=leg)])
        data_map[name]['stock'] += total_stock

    labels = list(data_map.keys())
    production_data = [data_map[k]['production'] for k in labels]
    ventes_data = [data_map[k]['ventes'] for k in labels]
    stock_data = [data_map[k]['stock'] for k in labels]
    
    # Couleurs cohérentes
    background_colors = get_legume_colors(labels)

    # Dernières Commandes
    dernieres_commandes = Commande.objects.filter(statut='En attente').order_by('-date_commande')[:5]

    context = {
        'revenu_total': revenu_total,
        'depenses_total': depenses_total,
        'bilan': bilan,
        'commandes_attente': commandes_attente,
        'labels': json.dumps(labels),
        'production_data': json.dumps(production_data),
        'ventes_data': json.dumps(ventes_data),
        'stock_data': json.dumps(stock_data),
        'background_colors': json.dumps(background_colors),
        'dernieres_commandes': dernieres_commandes,
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def statistiques(request):
    legumineuses = Legumineuse.objects.all()
    stats_legumineuses = []
    
    # Aggregation par nom
    data_map = {}
    for c in legumineuses:
        name = c.nom.strip()
        if name not in data_map:
            data_map[name] = {
                'total_recolte': 0, 'stock': 0, 'total_ventes': 0, 'rendement': 0
            }
            
        # Production totale
        data_map[name]['total_recolte'] += sum([r.quantite for r in Recolte.objects.filter(legumineuse=c)])
        
        # Stock disponible
        total_stock = sum([s.quantite_disponible for s in Stock.objects.filter(legumineuse=c)])
        data_map[name]['stock'] += total_stock
        
        # Ventes
        data_map[name]['total_ventes'] += sum([v.quantite for v in Vente.objects.filter(legumineuse=c)])

    labels = []
    production_data = []
    stock_data = []
    ventes_data = []

    # Reformat for template
    for name, data in data_map.items():
        stats_legumineuses.append({
            'legumineuse': name,
            'total_recolte': data['total_recolte'],
            'stock': data['stock'],
            'total_ventes': data['total_ventes'],
            'rendement': data['rendement']
        })
        
        # Données pour les graphiques
        labels.append(name)
        production_data.append(data['total_recolte'])
        stock_data.append(data['stock'])
        ventes_data.append(data['total_ventes'])

    # Couleurs cohérentes
    background_colors = get_legume_colors(labels)

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
        'ventes_data': json.dumps(ventes_data),
        'background_colors': json.dumps(background_colors),
    }

    return render(request, 'dashboard/statistiques.html', context)

@login_required
def commandes_livraisons(request):
    if not request.user.is_staff:
        return redirect('mon_compte')

    clients = User.objects.filter(commandes__isnull=False).distinct()
    data = []
    for u in clients:
        commandes = u.commandes.all().order_by('-date_commande')
        data.append({'client': u, 'commandes': commandes})

    return render(request, 'dashboard/commandes_livraisons.html', {'clients_commandes': data})
