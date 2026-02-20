from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Commande
from production.models import Legumineuse
from django.utils import timezone

@login_required
def liste_commandes(request):
    """Liste de toutes les commandes pour le staff avec filtrage des statuts"""
    if not request.user.is_staff:
        return redirect('mes_commandes')

    commandes = Commande.objects.all().select_related('client', 'legumineuse')
    statut_filter = request.GET.get('statut')
    if statut_filter:
        commandes = commandes.filter(statut=statut_filter)
    
    statuts_list = [
        {'code': code, 'label': label, 'selected': (code == statut_filter)} 
        for code, label in Commande.STATUT_CHOICES
    ]

    return render(request, 'commandes/liste_commande.html', {
        'commandes': commandes,
        'statuts_list': statuts_list,
        'current_statut': statut_filter
    })

@login_required
def mes_commandes(request):
    """Affiche les commandes du client connecté"""
    if request.user.is_staff:
        return redirect('dashboard')

    commandes = Commande.objects.filter(client=request.user).select_related('legumineuse')
    return render(request, 'commandes/mes_commandes.html', {'commandes': commandes})

@login_required
def passer_commande(request):
    """Permet à un client de passer une commande"""
    if request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        leg_id = request.POST.get('legumineuse')
        quantite = request.POST.get('quantite')
        # ignore prix_unitaire sent by client; use prix from Legumineuse
        nom = request.POST.get('nom')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')

        leg = Legumineuse.objects.get(pk=leg_id)
        prix_u = leg.prix_unitaire if leg.prix_unitaire is not None else 0
        commande = Commande.objects.create(
            client=request.user,
            legumineuse=leg,
            quantite=float(quantite),
            date_commande=timezone.now(),
            prix_unitaire=float(prix_u),
            client_nom=nom or request.user.get_full_name() or request.user.username,
            client_telephone=telephone,
            client_adresse=adresse,
        )

        # Mettre à jour le profil utilisateur si présent
        try:
            profil = request.user.profilclient
            if telephone:
                profil.telephone = telephone
            if adresse:
                profil.adresse = adresse
            profil.save()
        except Exception:
            pass

        # Mettre à jour le nom de l'utilisateur (séparation approximative)
        if nom:
            parts = nom.split()
            request.user.first_name = parts[0]
            request.user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
            request.user.save()

        return redirect('mes_commandes')

    # GET: préparer valeurs par défaut si le profil existe
    profil = None
    try:
        profil = request.user.profilclient
    except Exception:
        profil = None

    defaults = {
        'default_nom': request.user.get_full_name() or request.user.username,
        'default_telephone': profil.telephone if profil and profil.telephone else '',
        'default_adresse': profil.adresse if profil and profil.adresse else '',
    }

    legumineuses = Legumineuse.objects.all()
    context = {'legumineuses': legumineuses, **defaults}
    return render(request, 'commandes/passer_commande.html', context)

@login_required
def changer_statut_commande(request, commande_id):
    """Permet au staff de changer le statut d'une commande"""
    if not request.user.is_staff:
        return redirect('mes_commandes')
    
    commande = get_object_or_404(Commande, pk=commande_id)
    
    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        notes = request.POST.get('notes_staff')
        date_livraison = request.POST.get('date_livraison_prevue')
        
        if nouveau_statut in dict(Commande.STATUT_CHOICES):
            commande.statut = nouveau_statut
            if notes:
                commande.notes_staff = notes
            if date_livraison:
                commande.date_livraison_prevue = date_livraison
            if nouveau_statut == 'Livrée':
                commande.date_livraison_reelle = timezone.now().date()
                # Créer une vente associée si elle n'existe pas
                try:
                    from ventes.models import Vente
                    # éviter doublons
                    if not hasattr(commande, 'vente'):
                        prix_u = commande.prix_unitaire if commande.prix_unitaire is not None else 0
                        vente = Vente.objects.create(
                            legumineuse=commande.legumineuse,
                            quantite=commande.quantite,
                            prix_unitaire=prix_u,
                            client=commande.client_nom or commande.client.get_full_name() or commande.client.username,
                            date=commande.date_livraison_reelle,
                            commande=commande,
                            client_telephone=commande.client_telephone,
                            client_adresse=commande.client_adresse,
                        )
                except Exception:
                    # en cas d'erreur, on continue sans bloquer la sauvegarde
                    pass
            commande.save()
            return redirect('commandes')
    
    statuts_data = {
        'En attente': 'background: #fff3cd; color: #856404;',
        'Confirmée': 'background: #d1ecf1; color: #0c5460;',
        'En livraison': 'background: #e2e3e5; color: #383d41;',
        'Livrée': 'background: #d4edda; color: #155724;',
        'Annulée': 'background: #f8d7da; color: #721c24;',
    }

    statuts_list = [
        {
            'code': code, 
            'label': label, 
            'is_current': (code == commande.statut),
            'checked': 'checked' if code == commande.statut else '',
            'style': statuts_data.get(code, 'background: #eee; color: #333;')
        } 
        for code, label in Commande.STATUT_CHOICES
    ]
    
    client_display_name = commande.client_nom or commande.client.get_full_name() or commande.client.username

    return render(request, 'commandes/changer_statut.html', {
        'commande': commande,
        'statuts_list': statuts_list,
        'client_display_name': client_display_name
    })
