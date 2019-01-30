from django import forms
from .models import ShippingModel


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(initial='1')


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingModel
        exclude = ('paid',)
        widgets = {
            'address': forms.Textarea(attrs={'row': 5, 'col': 8}),
        }