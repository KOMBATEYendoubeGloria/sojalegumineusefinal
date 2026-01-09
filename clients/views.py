from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth.decorators import login_required


def inscription_client(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return redirect('inscription_client')

        user = User.objects.create_user(
            username=username,
            password=password
        )
        # S'assurer que ce compte est un compte client (pas staff / admin)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        login(request, user)
        if next_url:
            return redirect(next_url)
        return redirect('mes_commandes')

    return render(request, 'clients/inscription.html', {'next': next_url})


@login_required
def mon_compte(request):
    # Page client montrant ses informations et commandes
    if request.user.is_staff:
        return redirect('dashboard')

    commandes = request.user.commandes.all()
    return render(request, 'clients/compte.html', {'commandes': commandes})
