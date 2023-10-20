
from django_tenants.middleware.main import TenantMainMiddleware 
from django.http import HttpResponseForbidden
from main.models import  Domain
from django.shortcuts import render
from django_tenants.utils import get_tenant


#middle to check if tenent has been verified 
class VerifyTenantMiddleware(TenantMainMiddleware):
    def process_request(self, request):
        tenant = get_tenant(request)       
        try:
            if not tenant.is_verified and tenant.name != "public" :
                return HttpResponseForbidden("This pharmacy is not verified. Access denied.")
        except tenant.DoesNotExist:
            return HttpResponseForbidden("No tenant found for this domain. Access denied.")
            
        

