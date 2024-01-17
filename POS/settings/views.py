from django.shortcuts import render,redirect
from .forms import EmailbackendForm,AppsettingsForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import AppSettings,EmailBackend
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='tenant:login')
def showEmailSettings(request):
    context = {
        "emailbackendform": EmailbackendForm(),
        'emailbackend':EmailBackend.objects.first()
    }
    return render(request,"settings/email_settings.html",context=context)



@login_required(login_url='tenant:login')
def editEmailSettings(request, pk):
    
    email=EmailBackend.objects.get(id=pk)

    context = {
        "emailbackendform": EmailbackendForm(instance=email),
        "edit":True 
       
    }
    return render(request, "settings/email_settings.html", context=context)


@login_required(login_url='tenant:login')    
def showGeneralSettings(request):
    setting=AppSettings.objects.first()
    context = {
        "appsettingsform": AppsettingsForm(instance=setting),
        "app_settings":AppSettings.objects.first()
    }
    
    return render(request, "settings/generalsettings.html",context=context)
    


@login_required(login_url='tenant:login')   
def showSalesSettings(request):
    setting=AppSettings.objects.first()
    context = {
        "appsettingsform": AppsettingsForm(instance=setting),
        "app_settings":AppSettings.objects.first()
    }
    
    return render(request, "settings/sales_settings.html",context=context)
    


@login_required(login_url='tenant:login')
def edit_email_process(request,pk):
    if request.method == "POST":
        email=EmailBackend.objects.get(id=pk)
        emailbackendform = EmailbackendForm(request.POST,instance=email)
        if emailbackendform.is_valid():
            try :
                emailbackend = emailbackendform.save()
                messages.success(request,'Eamil editted successfully')
                return redirect('settings:emailsettings')
            except ValidationError as e:
                messages.error(request,str(e))
                return redirect('settings:emailsettings')
        messages.error(request,emailbackendform.errors)
        return redirect('settings:emailsettings')
            
@login_required(login_url='tenant:login')
def add_email_process(request):
    if request.method == "POST":
        emailbackendform = EmailbackendForm(request.POST)
        if emailbackendform.is_valid():
            try :
                emailbackend = emailbackendform.save()
                messages.success(request,'Eamil setup successfully')
                return redirect('settings:emailsettings')
            except ValidationError as e:
                messages.error(request,str(e))
                return redirect('settings:emailsettings')
        messages.error(request,emailbackendform.errors)
        return redirect('settings:emailsettings')

@login_required(login_url='tenant:login')           
def change_settings(request):
    if request.method == 'POST':
        setting=AppSettings.objects.first()
        settings = AppsettingsForm(request.POST, instance=setting)
        if settings.is_valid():
            settings.save()
            messages.success(request,"Settings changed successfully")
            return redirect('settings:salessettings')
        messages.error(request,"try again")
        return redirect('settings:salessettings')
        
@login_required(login_url='tenant:login')
def change_general_settings(request):
    if request.method == 'POST':
        setting=AppSettings.objects.first()
        settings = AppsettingsForm(request.POST, instance=setting)
        if settings.is_valid():
            settings.save()
            messages.success(request,"Settings changed successfully")
            return redirect('settings:generalsettings')
        messages.error(request,"try again")
        return redirect('settings:generalsettings')
        
