from django import forms
from payments.models import Payment


class PaymentForm(forms.ModelForm):
    """Form for processing payments"""
    class Meta:
        model = Payment
        fields = ['method', 'amount']
        widgets = {
            'method': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
        }


class MpesaPaymentForm(forms.Form):
    """Form for M-Pesa payments"""
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '254712345678',
            'pattern': '[0-9]{12}',
        }),
        help_text='Enter phone number in format: 254712345678'
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )