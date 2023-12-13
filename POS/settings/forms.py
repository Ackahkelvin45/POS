from django import forms
from .models import EmailBackend,AppSettings


class EmailbackendForm(forms.ModelForm):
    class Meta:
        model = EmailBackend
        fields = ("email","email_host_password",)
        
        widgets = {
            "email": forms.EmailInput(
                attrs={"class":"w-full max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300"}
            ),
            "email_host_password": forms.PasswordInput(
                attrs={
                    "class": "w-full max-md:w-full pl-5 pr-3 py-2 rounded-lg border border-gray-300 outline-none   focus:outline-none focus:ring-0 focus:border-gray-300",
                    'id':"password"
                }
            )
        }



class AppsettingsForm(forms.ModelForm):
    class Meta:
        model = AppSettings
        fields = ("automatic_print_receipt", "allow_date_change", "allow_typeahead")
        
        widgets = {
            "automatic_print_receipt": forms.CheckboxInput(
                attrs={
                    "class":"w-4 h-4 my-2 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600  focus:ring-2"
                }
            ),
                        "allow_date_change": forms.CheckboxInput(
                attrs={
                    "class":"w-4 h-4 my-2 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600  focus:ring-2"
                }
            ),
                        "allow_typeahead": forms.CheckboxInput(
                attrs={
                    "class":"w-4 h-4 my-2 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600  focus:ring-2"
                }
            )
        }
