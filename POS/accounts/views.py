from django.shortcuts import render

# Create your views here.


from django.urls import reverse
from django.http import HttpResponseRedirect

# For example, if you want to access the 'password_reset' URL
password_reset_url = reverse('password_reset')

# If you're inside a view function, you can use it like this:
def my_view(request):
    password_reset_url = reverse('password_reset')
    # Now you can use the generated URL as needed
    return HttpResponseRedirect(password_reset_url)