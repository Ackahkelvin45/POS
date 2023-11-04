from django.shortcuts import render,redirect
from django_tenants.utils import get_tenant
from main.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

      
@login_required(login_url='tenant:login')
def viewDashboard(request):  
        tenant = get_tenant(request)       
        user = request.user
        pharmacy_name = tenant.name 
        context = {
                    "pharmacy_name": pharmacy_name,
                   
                   
                }

        return render(request, 'tenant/dashboard.html', context=context)


def showLoginpage(request):
    return render(request, 'tenant/login.html')



def login_process(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        user=authenticate(email=email, password=password)
        print(user)     
        if user is not None:            
                login(request,user)                             
                return redirect("tenant:dashboard")
        else:
            messages.error(request,'Incorrect username or password. Please try again.')
            return redirect("tenant:login")
                


def logout_user(request):
    logout(request)
    return redirect("tenant:login")

    