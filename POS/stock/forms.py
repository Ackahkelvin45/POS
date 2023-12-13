from django import forms
from .models import StockEntry
from product.models import Product_Item
from django.urls import reverse_lazy



class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "name", str(obj))


class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ("product","quantity_received","previous_quantity","created_at","reason")
        
        widgets = {
            "product": forms.Select(
                attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block  w-full p-2.5 select outline-none focus:outline-none focus:ring-0",
                "data-available-quantity-url": reverse_lazy('inventory:get_available_quantity')
                }
            ),
            'quantity_received': forms.NumberInput(
                attrs={
                    "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full  p-2.5 outline-none focus:outline-none focus:ring-0"
                }
            ),
            'previous_quantity':
            forms.NumberInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 outline-none focus:outline-none focus:ring-0",
                    'disabled':True,'id':"id_previous_quantity"
                }
            ),
            "created_at":forms.TextInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 outline-none focus:outline-none focus:ring-0"
                  ,'required':True,"type":"datetime-local"
                }
              
            ),
            "reason":forms.Textarea(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 outline-none focus:outline-none focus:ring-0"
                  ,'required':True,'rows':2
                }
              
            ),

        }

        def __init__(self, *args, **kwargs):
            super(StockEntryForm, self).__init__(*args, **kwargs)

            # Customize choices for category, subcategory, item_unit, and supplier
            self.fields["product"] = CustomModelChoiceField(
                queryset=Product_Item.objects.all(),
                widget=forms.Select(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 select outline-none focus:outline-none focus:ring-0"}),
            )
