from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ("company_name", 'first_name',
         'other_names', 'email', 'phone_number_1',
         'phone_number_2', 'code', 'website', 'city', 'address', 'opening_balance')
         
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300', "required": "True"}),
            'first_name': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300' }),
            'other_names': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300'}),
            'email': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300'}),
            'phone_number_1': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300', "required": "True"}),
            'phone_number_2': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300'}),
            'code': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300'}),
            'website': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300'}),
            'city': forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300', "required": "True"}),
            "address": forms.Textarea(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300', "required": "True", 'rows': 5}),
            'opening_balance':forms.NumberInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300','step': 0.1}),
            
            


         }
