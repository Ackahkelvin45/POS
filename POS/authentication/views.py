from django.shortcuts import render,redirect
from main.models import Domain,Pharmacy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import UserForm
from main.forms import PharmacyForm
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django_tenants.utils import tenant_context


# Create your views here.






def showSignuppage(request):
    context = {
        "userform": UserForm,
        "pharmacyform":PharmacyForm,
    }
    return render(request,'auth/signup.html',context=context)


def show(request):
   

    return render(request,'auth/email_message.html',)

def signupprocess(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        pharmacyform=PharmacyForm(request.POST)
        password1 = request.POST['password']
        password2 = request.POST['confirmpassword']

        if password1 == password2:
            if userform.is_valid() and pharmacyform.is_valid():
                pharmacy = pharmacyform.save(commit=False)
                user = userform.save()
                pharmacy.is_mainbranch = True       
                name = pharmacy.name.replace("-", "")
                name = name.replace(" ", "")
                pharmacy.schema_name=name
                pharmacy.save()
                user.set_password(password1)
                user.save()
                with tenant_context(pharmacy):
                    user.is_admin = True
                    user.is_superuser = True
                    user.is_staff=True
                    user.save()
                with schema_context('public'):
                    user.is_superuser = False
                    user.save()
                pharmacy.owner = user
                pharmacy.workers.add(user)
                pharmacy.save()    
                domain = Domain(domain=name + ".localhost", tenant=pharmacy, is_primary=True)
                domain.save()

                template = render_to_string("auth/email_message.html", {"name":user.first_name})
                email = EmailMessage(
                        "Thank you for choosing samsof pharmacies!",
                        template,
                        settings.EMAIL_HOST_USER,
                        [user.email,]

                    )
                email.fail_silently = False
                email.send()
            
           
            

                messages.success(request, "Please allow up to 24 hours for our team to verify your account.")
                return redirect( 'auth:signup')
            messages.error(request, str(userform.errors) + str(pharmacyform.errors))
            return redirect('auth:signup')
        messages.error(request, 'Passwords must match')
        return render('auth:signup')
    messages.error(request, 'An error occured try again ')
    return redirect('auth:signup')




