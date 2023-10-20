from django import forms
from .models import Pharmacy

class PharmacyForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = ("name", "address", "contact")
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full -ml-10 pl-10 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300", "placeholder": 'business name', "required": 'True'}),
            "address": forms.TextInput(attrs={'class': "w-full -ml-10 pl-10 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300", "placeholder": "address", "required": 'True'}),
            'contact': forms.TextInput(attrs={"class": "w-full -ml-10 pl-10 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300", "placeholder": "+(233)", "required": "True"})
            
        }