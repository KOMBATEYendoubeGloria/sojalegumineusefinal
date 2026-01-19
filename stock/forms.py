from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['legumineuse', 'quantite_disponible']
        widgets = {
            'legumineuse': forms.Select(attrs={'class': 'form-control'}),
            'quantite_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
        }
