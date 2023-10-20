from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django_tenants.utils import get_tenant, schema_context
from django.contrib import messages
from .models import Unit, Subcategory
from .forms import SubcategoryForm




# Create your views here.

def showAddCategory(request):
    return render(request, 'product/addcategory.html')


def showAddSubCategory(request):
    context = {
        "subcategorys": Subcategory.objects.all().order_by('-id'),
        'form':SubcategoryForm,
    }
    return render(request, 'product/subcategory.html',context=context)


def showAddProduct(request):
    return render(request, 'product/addproduct.html')



def showAddUnit(request):
    return render(request, 'product/unit.html')



        
def add_unit_process(request):
    try:
   
        if request.method == 'POST':
            name = request.POST['name']
            shorthand = request.POST['shorthand']
            unit = Unit(name=name, shorthand=shorthand)
            unit.save()
            messages.success(request, 'Unit added Successfully')
            return redirect("product:unitpage")
        messages.error(request, 'Error Adding Unit,Try Again')
        return redirect("product:unitpage")
    except:
        messages.error(request, 'Unit Already Exists')
        return redirect("product:unitpage")

def add_subcategory(request):
   
        if request.method == "POST":
            subcategoryform = SubcategoryForm(request.POST)
            if subcategoryform.is_valid():
                subcategory = subcategoryform.save()
                messages.success(request, 'Subcategory Added Successfully')
                return redirect("product:subcategorypage")
            messages.error(request, str(subcategoryform.errors))
            return redirect("product:subcategorypage")
   
        


       
            
            


        
        