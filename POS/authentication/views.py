from django.shortcuts import render, redirect
from main.models import Domain, Pharmacy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import UserForm
from main.forms import PharmacyForm
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django_tenants.utils import tenant_context, schema_context
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
import threading
from .utils import send_verification_email,create_admin_group



# Create your views here.


def showSignuppage(request):
    context = {
        "userform": UserForm,
        "pharmacyform": PharmacyForm,
    }
    return render(request, "auth/signup.html", context=context)


def show(request):
    return render(
        request,
        "auth/email_message.html",
    )




def signupprocess(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        pharmacyform = PharmacyForm(request.POST)
        password1 = request.POST["password"]
        password2 = request.POST["confirmpassword"]

        if password1 == password2:
            if userform.is_valid() :
                if  pharmacyform.is_valid():
                    pharmacy = pharmacyform.save(commit=False)
                    user = userform.save()
                    pharmacy.is_mainbranch = True
                    name = pharmacy.name.replace("-", "")
                    name = name.replace(" ", "")
                    pharmacy.schema_name = name
                    pharmacy.save()
                    user.set_password(password1)
                    user.save()
                    
                    user.is_admin = True
                            
                                
                    user.is_staff=True
                    user.is_superuser = True
                    user.is_staff = True

                    user.save()


                    pharmacy.owner = user
                    pharmacy.workers.add(user)
                    pharmacy.save()
                    user.pharmacys.add(pharmacy)
                    group = create_admin_group(pharmacy)
                    user.groups.add(group)
                    user.save()
                    domain = Domain(
                        domain=name + ".localhost", tenant=pharmacy, is_primary=True
                    )
                    domain.save()



          

                    email_thread = threading.Thread(target=send_verification_email, args=(user,))
                    email_thread.start()

                    messages.success(
                        request,
                        "Please allow up to 24 hours for our team to verify your account.",
                    )
                    return redirect("auth:signup")
                
                messages.error(request,  str(pharmacyform.errors))
                return redirect("auth:signup")
            messages.error(request, str(userform.errors))
            return redirect("auth:signup")
        messages.error(request, "Passwords must match")
        return redirect("auth:signup")
    messages.error(request, "An error occured try again ")
    return redirect("auth:signup")


def view_profile(request):
    if request.user.is_authenticated:
        return render(request, "auth/userprofile.html")
    return redirect("auth:login")


def preview_template(request):
     return render(request, "auth/signup_redirect.html")
