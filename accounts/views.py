from django.shortcuts import render, redirect


# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.contrib import messages

class ConnexionView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        # vérifie le type de compte si la redirection demandée est un flux client
        user = form.get_user()
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if user.is_staff and next_url and ('passer' in next_url or 'mes' in next_url or 'compte' in next_url):
            messages.warning(self.request, "Compte staff détecté — vous avez été redirigé vers le dashboard.")
            return redirect('dashboard')
        return super().form_valid(form)

    def get_success_url(self):
        # Preferer le paramètre 'next' s'il est présent
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        # Sinon, rediriger en fonction du rôle
        if self.request.user.is_staff:
            return reverse('dashboard')
        # Les clients sont redirigés vers leurs commandes
        return reverse('mes_commandes')


class DeconnexionView(LogoutView):
    def get_next_page(self):
        return reverse('accueil')

