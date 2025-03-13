from django import forms
from .models import NFCTag

class BalanceForm(forms.ModelForm):
    class Meta:
        model = NFCTag
        fields = ['balance']
        widgets = {
            'balance': forms.NumberInput(attrs={'min': '0', 'step': '0.01'})
        }
