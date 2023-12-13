from django.shortcuts import render,redirect
from .forms import EmailbackendForm,AppsettingsForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import AppSettings
from django.http import HttpResponseRedirect
# Create your views here.

def showEmailSettings(request):
    context = {
        "emailbackendform":EmailbackendForm()
    }
    return render(request,"settings/email_settings.html",context=context)


def showSalesSettings(request):
    setting=AppSettings.objects.first()
    context = {
        "appsettingsform": AppsettingsForm(instance=setting),
        "app_settings":AppSettings.objects.first()
    }
    
    return render(request, "settings/sales_settings.html",context=context)
    


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
        
