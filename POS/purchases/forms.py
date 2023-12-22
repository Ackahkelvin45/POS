from django import forms
from .models import PurchaseOrder, OrderedProduct
from product.models import Package
from suppliers.models import Supplier





class CustomModelChoiceField2(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "company_name", str(obj))

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ("supplier","discount","invoice_number")
        
        widgets = {
            "supplier":forms.Select(
                attrs={
                    "class": " w-[40%] max-sm:w-[50%]   h-10  pl-4 pr-3  rounded-md  border border-gray-400 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    'required':False
                }
            ),
            'discount': forms.NumberInput(
                attrs={
                 "class": "w-[40%]   max-sm:w-[50%]  h-10  pl-4 pr-3  rounded-md  border border-gray-400 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                 'required':False
                 
                }
            ),
              'invoice_number': forms.NumberInput(
                attrs={
                    "class": "w-[40%]   max-sm:w-[50%]  h-10  pl-4 pr-3  rounded-md  border border-gray-400 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    'required':False
                 
                }
            ),
        }
    def __init__(self, *args, **kwargs):
            super(PurchaseOrderForm, self).__init__(*args, **kwargs)

            self.fields["supplier"].widget.attrs['required'] = False
            self.fields["discount"].widget.attrs['required'] = False
            self.fields["supplier"] = CustomModelChoiceField2(
                queryset=Supplier.objects.all(),
                widget=forms.Select(attrs={"class": " max-sm:w-[50%]  w-[40%]  h-10  pl-4 pr-3  rounded-md  border border-gray-400 outline-none focus:outline-none focus:ring-0 focus:border-gray-300 ","required":False}),
            )


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
                return f'{getattr(obj, "package_name", str(obj))} ({ getattr(obj, "number_of_products_item", str(obj))} units) '


class OrderedProductForm(forms.ModelForm):
    class Meta:
        model = OrderedProduct
        fields = ("quantity",'cost_unit_price','product',"package_type")
        
        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ",
                    
                    "required": True,
                    
                    
                }
            ),
            "cost_unit_price": forms.NumberInput(
                attrs={
                    'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ",
                    "step": "0.01",
                    "required": True,
                    "id":'item_cost_price'
                    
                    
                }
            ),
            "package_type":forms.Select(
                attrs={
                 'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ",
                   'required': False 


                }
            ),
        }
    def __init__(self, *args, **kwargs):
            super(OrderedProductForm, self).__init__(*args, **kwargs)
            
            # Set the default value for cost_unit_price
            self.fields["package_type"].widget.attrs['required'] = False
            if 'product' in self.initial:
                product = self.initial['product']
                if product and 'instance' not in kwargs:
                    self.fields['cost_unit_price'].initial = product.cost_price
                if hasattr(product, 'id'):
                    self.fields["package_type"].queryset = Package.objects.filter(product_id=product.id)

            self.fields["package_type"] = CustomModelChoiceField(
                queryset=self.fields["package_type"].queryset,
                required=False,
                widget=forms.Select(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ","id":"package_select" }),

            )


      
   