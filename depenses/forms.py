from django import forms
from .models import Depense

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['type_depense', 'montant', 'date', 'legumineuse']
        widgets = {
            'type_depense': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'legumineuse': forms.Select(attrs={'class': 'form-control'}),
        }
