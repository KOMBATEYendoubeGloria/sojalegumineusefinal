from django import forms
from .models import Employe, Legumineuse, Recolte, Section

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nom', 'telephone', 'section']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }

class LegumineuseForm(forms.ModelForm):
    class Meta:
        model = Legumineuse
        fields = ['nom', 'prix_unitaire', 'section']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }

class RecolteForm(forms.ModelForm):
    class Meta:
        model = Recolte
        fields = ['legumineuse', 'section', 'quantite', 'date', 'qualite']
        widgets = {
            'legumineuse': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'qualite': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['nom', 'superficie', 'employe']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'superficie': forms.NumberInput(attrs={'class': 'form-control'}),
            'employe': forms.Select(attrs={'class': 'form-control'}),
        }
