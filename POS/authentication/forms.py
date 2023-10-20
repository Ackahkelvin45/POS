from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone_number",)
        
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'w-full -ml-10 pl-10 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300', "placeholder": "John", "required": "True"}),
            "last_name": forms.TextInput(attrs={'class': "w-full -ml-10 pl-10 pr-3 py-2 rounded-lg border border-gray-300 outline-none    focus:outline-none focus:ring-0 focus:border-gray-300", "placeholder": "smith", "required": "True"}),
            "email": forms.TextInput(attrs={"class": "w-full -ml-10 pl-10 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300", "placeholder": "martinsmith@example.com", "required": "True"}),
            "phone_number" :forms.TextInput(attrs={"class":"w-full -ml-10 pl-10 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300","placeholder":"(+233)","required":"True"})
        }
