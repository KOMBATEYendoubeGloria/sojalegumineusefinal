from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Depense

@login_required
def liste_depenses(request):
    depenses = Depense.objects.all()
    return render(request, 'depenses/liste_depenses.html', {'depenses': depenses})
