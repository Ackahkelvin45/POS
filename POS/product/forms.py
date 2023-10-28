from django import forms
from .models import Category, Subcategory, Unit


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ["name", "code"]
        
        widgets = {
            "name": forms.TextInput(attrs={'class': "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300", "required": "True"}),
            "code":forms.TextInput(attrs={"class":"w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300", "required": "True"})
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "code"]
        
        widgets = {
            "name": forms.TextInput(attrs={'class': "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300", "required": "True"}),
            "code":forms.TextInput(attrs={"class":"w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300", "required": "True"})
        }




class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "shorthand"]
        
        widgets = {
            "name": forms.TextInput(attrs={'class': "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300", "required": "True"}),
            "shorthand":forms.TextInput(attrs={"class":"w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300", "required": "True"})
        }



