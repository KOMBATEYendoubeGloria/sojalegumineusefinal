from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employe, Legumineuse, Recolte, Section
from .forms import EmployeForm, LegumineuseForm, RecolteForm, SectionForm

@login_required
def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'production/liste_employes.html', {
        'employes': employes
    })

@login_required
def liste_legumineuses(request):
    legumineuses = Legumineuse.objects.all()
    return render(request, 'production/liste_legumineuses.html', {
        'legumineuses': legumineuses
    })

@login_required
def liste_recoltes(request):
    recoltes = Recolte.objects.all()
    return render(request, 'production/liste_recoltes.html', {
        'recoltes': recoltes
    })

@login_required
def liste_sections(request):
    sections = Section.objects.all()
    return render(request, 'production/liste_sections.html', {
        'sections': sections
    })

# --- EMPLOYES ---
@login_required
def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employes')
    else:
        form = EmployeForm()
    return render(request, 'production/ajouter_employe.html', {'form': form, 'title': 'Ajouter un Employé'})

@login_required
def modifier_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('employes')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'production/ajouter_employe.html', {'form': form, 'title': 'Modifier un Employé'})

@login_required
def supprimer_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.delete()
        return redirect('employes')
    return render(request, 'production/confirm_delete.html', {'objet': f"l'employé {employe.nom}", 'cancel_url': 'employes'})

# --- LEGUMINEUSES ---
@login_required
def ajouter_legumineuse(request):
    if request.method == 'POST':
        form = LegumineuseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('legumineuses')
    else:
        form = LegumineuseForm()
    return render(request, 'production/ajouter_legumineuse.html', {'form': form, 'title': 'Ajouter une Légumineuse'})

@login_required
def modifier_legumineuse(request, pk):
    legumineuse = get_object_or_404(Legumineuse, pk=pk)
    if request.method == 'POST':
        form = LegumineuseForm(request.POST, instance=legumineuse)
        if form.is_valid():
            form.save()
            return redirect('legumineuses')
    else:
        form = LegumineuseForm(instance=legumineuse)
    return render(request, 'production/ajouter_legumineuse.html', {'form': form, 'title': 'Modifier une Légumineuse'})

@login_required
def supprimer_legumineuse(request, pk):
    legumineuse = get_object_or_404(Legumineuse, pk=pk)
    if request.method == 'POST':
        legumineuse.delete()
        return redirect('legumineuses')
    return render(request, 'production/confirm_delete.html', {'objet': f"la légumineuse {legumineuse.nom}", 'cancel_url': 'legumineuses'})

# --- RECOLTES ---
@login_required
def ajouter_recolte(request):
    if request.method == 'POST':
        form = RecolteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recoltes')
    else:
        form = RecolteForm()
    return render(request, 'production/ajouter_recolte.html', {'form': form, 'title': 'Ajouter une Récolte'})

@login_required
def modifier_recolte(request, pk):
    recolte = get_object_or_404(Recolte, pk=pk)
    if request.method == 'POST':
        form = RecolteForm(request.POST, instance=recolte)
        if form.is_valid():
            form.save()
            return redirect('recoltes')
    else:
        form = RecolteForm(instance=recolte)
    return render(request, 'production/ajouter_recolte.html', {'form': form, 'title': 'Modifier une Récolte'})

@login_required
def supprimer_recolte(request, pk):
    recolte = get_object_or_404(Recolte, pk=pk)
    if request.method == 'POST':
        recolte.delete()
        return redirect('recoltes')
    return render(request, 'production/confirm_delete.html', {'objet': f"cette récolte de {recolte.legumineuse.nom}", 'cancel_url': 'recoltes'})

# --- SECTIONS ---
@login_required
def ajouter_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sections')
    else:
        form = SectionForm()
    return render(request, 'production/ajouter_section.html', {'form': form, 'title': 'Ajouter une Section'})

@login_required
def modifier_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('sections')
    else:
        form = SectionForm(instance=section)
    return render(request, 'production/ajouter_section.html', {'form': form, 'title': 'Modifier une Section'})

@login_required
def supprimer_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section.delete()
        return redirect('sections')
    return render(request, 'production/confirm_delete.html', {'objet': f"la section {section.nom}", 'cancel_url': 'sections'})

@login_required
def details_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    # Les employés dont c'est la section de travail
    employes = section.employes.all()
    # Les légumineuses cultivées dans cette section
    legumineuses = section.legumineuses_cultures.all()
    # Les dernières récoltes de cette section
    recoltes = section.recoltes.all().order_by('-date')
    
    return render(request, 'production/details_section.html', {
        'section': section,
        'employes': employes,
        'legumineuses': legumineuses,
        'recoltes': recoltes
    })
