from django import forms
from .models import ReceivedStock


class RecievestockForm(forms.ModelForm):
    class Meta:
        model = ReceivedStock
        fields = ("received_quantity",)
        
        widgets = {
            "received_quantity": forms.NumberInput(attrs={"class":"w-[20px] h-8  pl-4 pr-3  rounded-lg  border border-gray-400 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"})
            
        }
