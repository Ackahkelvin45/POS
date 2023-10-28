from django import forms
from authentication.models import User
from django.contrib.auth.models import Group





class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone_number",'username',)
        
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300',"required": "True"}),
            "last_name": forms.TextInput(attrs={'class': "w-full max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300",  "required": "True"}),
            "email": forms.TextInput(attrs={"class": "w-full max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300", "required": "True"}),
            "phone_number" :forms.TextInput(attrs={"class":"w-full max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300","required":"True"}),
            'username':forms.TextInput(attrs={"class":"w-full max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300","required":"True"})
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={'class': 'w-[50%] pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300',"required": "True"}),

        }
