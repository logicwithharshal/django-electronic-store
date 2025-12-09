from django import forms
from .models import DeliveryDetail

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = DeliveryDetail
        fields = ['name', 'address', 'phone']
