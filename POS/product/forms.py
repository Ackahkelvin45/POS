from django import forms
from .models import Category, Subcategory, Unit, Product_Item,Package
from suppliers.models import Supplier


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ["name", "code"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300",
                    "required": "True",
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300",
                    "required": "True",
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "code"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300",
                    "required": "True",
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300",
                    "required": "True",
                }
            ),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "shorthand"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300",
                    "required": "True",
                }
            ),
            "shorthand": forms.TextInput(
                attrs={
                    "class": "w-[60%] max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300",
                    "required": "True",
                }
            ),
        }



class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "name", str(obj))


class CustomModelChoiceField1(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "first_name", str(obj))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product_Item
        fields = ("code","name",'category',"subcategory","item_unit","supplier","notes","cost_price","markup","selling_price","profit_margin","minimum_stock_level","expiry_date","product_image")

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": " w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": " w-full  pl-4 pr-3 py-2 rounded-l-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "subcategory": forms.Select(
                attrs={
                    "class": " w-full pl-4 pr-3 py-2 rounded-l-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "item_unit": forms.Select(
                attrs={
                    "class": " w-full pl-4 pr-3 py-2 rounded-l-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "supplier": forms.Select(
                attrs={
                    "class": " w-full pl-4 pr-3 py-2 rounded-l-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",'required':False
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    
                }
            ),
            "cost_price": forms.NumberInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    'step': 0.1,'id':'unit_cost_price'
                }
            ),
             "markup": forms.NumberInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    'step': 0.1,'id':'markup','disabled':True
                }
            ),

           
            "selling_price": forms.NumberInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                    ,'step': 0.1,'id':"unit_selling_price",'disabled':True
                }
            ),
            "profit_margin": forms.NumberInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                    ,'step': 0.1,'id':"profit_forecast"   ,'disabled':True             }
            ),
            "minimum_stock_level": forms.NumberInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "expiry_date": forms.DateInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    "type": "date",
                }
            ),
            "product_image": forms.ClearableFileInput(
                attrs={"id": "dropzone-file", "class": "hidden",'required':False}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Customize choices for category, subcategory, item_unit, and supplier
        self.fields["supplier"].widget.attrs['required'] = False
        self.fields["category"] = CustomModelChoiceField(
            queryset=Category.objects.all(),
            widget=forms.Select(attrs={"class": " select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"}),

        )
        self.fields["subcategory"] = CustomModelChoiceField(
            queryset=Subcategory.objects.all(),
             widget=forms.Select(attrs={"class": " select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"}),
        )
        self.fields["item_unit"] = CustomModelChoiceField(queryset=Unit.objects.all(),
         widget=forms.Select(attrs={"class": " select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"}),)
        self.fields["supplier"] = CustomModelChoiceField1(
            queryset=Supplier.objects.all(),
             widget=forms.Select(attrs={"class": " select w-full pl-4 pr-3 py-2 rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",'required':False}),
             required=False,
        )





class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ("package_name","number_of_products_item","cost_price",  "selling_price","product","available_quantity",)
        
        widgets = {
            
      
            "package_name": forms.TextInput(
                attrs={
                    "class": " w-[40%] max-sm:w-[80%] pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
                "available_quantity": forms.TextInput(
                attrs={
                    "class": " w-[40%] max-sm:w-[80%] pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
              "number_of_products_item": forms.NumberInput(
                attrs={
                    "class": "w-[40%]   max-sm:w-[80%]  pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            
              "cost_price": forms.NumberInput(
                attrs={
                    "class": "w-[40%] max-sm:w-[80%]  pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                    ,'step': 0.1,         }
            ),
            "selling_price": forms.NumberInput(
                attrs={
                    "class": "w-[40%] max-sm:w-[80%]  pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300" ,'step': 0.1,         }
            
                
            ),
             "product": forms.Select(
                attrs={
                    "class": " select w-[40%] pl-4 pr-3  max-sm:w-[80%]  rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300" ,'step': 0.1,         }
            
                
            ),
           

        }

        def __init__(self, *args, **kwargs):
            super(PackageForm, self).__init__(*args, **kwargs)


            self.fields["product"] = CustomModelChoiceField(
                queryset=Unit.objects.all(),
                widget=forms.Select(attrs={"class": " select w-[40%] pl-4 pr-3  rounded-lg  border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"}),

            )