from django import forms
from .models import Sale,SaleProduct,Tax,PaymentDetails
from product.models import Package
from suppliers.models import Supplier
from settings.models import AppSettings
from django.urls import reverse_lazy





class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = '__all__'
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    "step":"0.01",
                }
            ),
            "name":forms.TextInput(
                attrs={
                    "class":"select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
        }

class CustomModelChoiceField2(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "company_name", str(obj))

class SaleForm(forms.ModelForm):
    
    date_created = forms.DateTimeField(
        input_formats=['%d/%m/%y %H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'class': "h-6 border-0 bg-[#f9f9ef] w-48 focus:ring-0",
                'type': "datetime-local",
                'id': "date_created"
            }
        )
    )
    class Meta:
        model = Sale
        fields = ("date_created",)
  
    def __init__(self, *args,allow_date_change_value=None, **kwargs,  ):
            super(SaleForm, self).__init__(*args, **kwargs)
            self.allow_date_change_value = allow_date_change_value
            if not  self.allow_date_change_value:
                self.fields['date_created'].widget.attrs['readonly'] = True
     


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{getattr(obj, "package_name", str(obj))} ({ getattr(obj, "number_of_products_item", str(obj))} units) '


class SaleProductForm(forms.ModelForm):
    class Meta:
        model =SaleProduct
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
                    "required": True,"id":"cost_price"
                
                    
                    
                }
            ),
            "package_type":forms.Select(
                attrs={
                 'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ",
                   'required': False ,"id":"package_type","data-cost-price-url": reverse_lazy('sales:get_package_cost_price'),


                }
            ),
        }
    def __init__(self, *args, **kwargs):
            super(SaleProductForm, self).__init__(*args, **kwargs)
            
            # Set the default value for cost_unit_price
            self.fields["package_type"].widget.attrs['required'] = False
            if 'product' in self.initial:
                product = self.initial['product']
                if product and 'instance' not in kwargs:
                    self.fields['cost_unit_price'].initial = product.selling_price
                self.fields["package_type"].queryset = Package.objects.filter(product_id=product.id)

            self.fields["package_type"] = CustomModelChoiceField(
                queryset=self.fields["package_type"].queryset,
                required=False,
                widget=forms.Select(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ", "id": "package_type",
                 "data-cost-price-url": reverse_lazy('sales:get_package_cost_price'), }),

            )


class PaymentDetailsForm(forms.ModelForm):
    class Meta:
        model = PaymentDetails
        fields = ("payment_type", "amount_paid", "change", "balance",)
        widgets = {
            "payment_type": forms.Select(
                attrs={
                    "class": " select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                     "required":False
                }
            ),
            "amount_paid": forms.NumberInput(
                attrs={
                    "class": " select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    "step": "0.01",
                    "min": "0",
                    "id": "amount_paid",
                    
                }
            ),
            "change": forms.NumberInput(
                    attrs={
                    "class": "select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                                        "step": "0.01",
                                        "min": "0",
                                        "id": "change_amount",
                                        "readonly":"readonly",
                }
                  
            ),
            "balance": forms.NumberInput(
                attrs={
                   "class": " select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    "step": "0.01",
                    "min": "0",
                    "id": "balance_amount",
                   "readonly":"readonly",
                    "required":False
                    
                
                }

            ),
        }
    def __init__(self, *args, **kwargs):
        super(PaymentDetailsForm, self).__init__(*args, **kwargs)
        if 'sale' in self.initial:
            sale = self.initial['sale']

        # Set the default value for the balance field
            self.fields['balance'].initial = sale.total_cost_price
            self.fields['balance'].required=False
        
        self.fields["payment_type"] = forms.ChoiceField(
                choices=(("cash","cash"),("Mobile Money","Mobile Money"),("Bank","Bank")),
                
                widget=forms.Select(
                      attrs={
                    "class": " select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    "required":False
                }
                ),

            )
        self.fields['payment_type'].initial = 'cash'
        self.fields['payment_type'].required=False