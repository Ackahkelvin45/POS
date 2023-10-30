from django import forms
from .models import Category, Subcategory, Unit, Product
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


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             "code",
#             "name",
#             "category",
#             "subcategory",
#             "unit",
#             "supplier",
#             "notes",
#             "cost_price",
#             "profit_margin",
#             "selling_price",
#             "min_stock_level",
#             "expire_date",
#             "image",
#         ]


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "name", str(obj))


class CustomModelChoiceField1(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "first_name", str(obj))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "w-full  pl-4 pr-3 py-2 rounded-l-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "subcategory": forms.Select(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-l-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "item_unit": forms.Select(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-l-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "supplier": forms.Select(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-l-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300",
                    "placeholder": "business name",
                }
            ),
            "cost_price": forms.TextInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "selling_price": forms.TextInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "profit_margin": forms.TextInput(
                attrs={
                    "class": "w-full pl-4 pr-3 py-2 rounded-lg border border-gray-300 outline-none focus:outline-none focus:ring-0 focus:border-gray-300"
                }
            ),
            "minimum_stock_level": forms.TextInput(
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
            "product_image": forms.FileInput(
                attrs={"id": "dropzone-file", "class": "hidden"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Customize choices for category, subcategory, item_unit, and supplier
        self.fields["category"] = CustomModelChoiceField(
            queryset=Category.objects.all()
        )
        self.fields["subcategory"] = CustomModelChoiceField(
            queryset=Subcategory.objects.all()
        )
        self.fields["item_unit"] = CustomModelChoiceField(queryset=Unit.objects.all())
        self.fields["supplier"] = CustomModelChoiceField1(
            queryset=Supplier.objects.all()
        )
