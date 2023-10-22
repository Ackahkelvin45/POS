from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django_tenants.utils import get_tenant, schema_context
from django.contrib import messages
from .models import Unit, Subcategory,Category
from .forms import SubcategoryForm,CategoryForm,UnitForm




# Create your views here.

def showAddCategory(request):
    context = {
        "categorys": Category.objects.all().order_by('-id'),
         'form':CategoryForm,
    }
    return render(request, 'product/addcategory.html',context=context)


def showAddSubCategory(request):
    context = {
        "subcategorys": Subcategory.objects.all().order_by('-id'),
        'form':SubcategoryForm,
    }
    return render(request, 'product/subcategory.html',context=context)


def showAddProduct(request):
    return render(request, 'product/addproduct.html')



def showAddUnit(request):
    context = {
        "form": UnitForm,
        'units':Unit.objects.all().order_by('-id')
    }
    return render(request, 'product/unit.html',context=context)



        
def add_unit_process(request):
   
        if request.method == 'POST':
            unitform = UnitForm(request.POST)
            if unitform.is_valid():

                unit=unitform.save()
                messages.success(request, 'Unit added Successfully')
                return redirect("product:unitpage")
            messages.error(request,str(unitform.errors))
            return redirect("product:unitpage")




def edit_unit(request, pk):
    if Unit.objects.filter(id=pk).exists():
        unit = Unit.objects.get(id=pk)
        context = {
              "units": Unit.objects.all().order_by('-id'),
                'form': UnitForm(instance=unit),
                "edit": True,
                'unit_item':unit
        }
        return render(request, 'product/unit.html', context=context)  
    
def edit_unit_process(request, pk):
    if request.method == "POST":
        if Unit.objects.filter(id=pk).exists():
            unit= Unit.objects.get(id=pk)
            unitform = UnitForm(request.POST,instance=unit)
            if unitform.is_valid():
                unit = unitform.save()
                messages.success(request, 'Unit Edited Successfully')
                return redirect("product:unitpage")
            messages.error(request, str(unitform.errors))
            return redirect("product:unitpage")


def delete_unit(request, pk):
    if Unit.objects.filter(id=pk).exists():
        unit =Unit.objects.get(id=pk)
        unit.delete()
        messages.success(request, 'Unit Deleted Successfully')
        return redirect("product:unitpage")
    messages.error(request, 'Error Try Agian')
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




def delete_subcategory(request, pk):
    if Subcategory.objects.filter(id=pk).exists():
        subcategory = Subcategory.objects.get(id=pk)
        subcategory.delete()
        messages.success(request, 'Subcategory Deleted Successfully')
        return redirect("product:subcategorypage")
    messages.error(request, 'Error Try Agian')
    return redirect("product:subcategorypage")




def edit_subcategory(request, pk):
    if Subcategory.objects.filter(id=pk).exists():
        subcategory = Subcategory.objects.get(id=pk)
        context = {
              "subcategorys": Subcategory.objects.all().order_by('-id'),
                'form': SubcategoryForm(instance=subcategory),
                "edit": True,
                'subcategory_item':subcategory
        }
        return render(request, 'product/subcategory.html', context=context)  

def edit_subcategory_process(request, pk):
    if request.method == "POST":
        if Subcategory.objects.filter(id=pk).exists():
            subcategory = Subcategory.objects.get(id=pk)
            subcategoryform = SubcategoryForm(request.POST,instance=subcategory)
            if subcategoryform.is_valid():
                subcategory = subcategoryform.save()
                messages.success(request, 'Subcategory Edited Successfully')
                return redirect("product:subcategorypage")
            messages.error(request, str(subcategoryform.errors))
            return redirect("product:subcategorypage")
   

def add_category(request):
        if request.method == "POST":
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category = categoryform.save()
                messages.success(request, 'Category Added Successfully')
                return redirect("product:categorypage")
            messages.error(request, str(categoryform.errors))
            return redirect("product:categorypage")
        


       
            
            

def delete_category(request, pk):
    if Category.objects.filter(id=pk).exists():
        category = Category.objects.get(id=pk)
        category.delete()
        messages.success(request, 'Category Deleted Successfully')
        return redirect("product:categorypage")
    messages.error(request, 'Error Try Agian')
    return redirect("product:categorypage")

        
def edit_category(request, pk):
    if Category.objects.filter(id=pk).exists():
        category = Category.objects.get(id=pk)
        context = {
              "categorys": Category.objects.all().order_by('-id'),
                'form': CategoryForm(instance=category),
                "edit": True,
                'category_item':category
        }
        return render(request, 'product/addcategory.html', context=context)
        




        
def edit_category_process(request, pk):
    if request.method == "POST":
        if Category.objects.filter(id=pk).exists():
            category = Category.objects.get(id=pk)
            categoryform = CategoryForm(request.POST,instance=category)
            if categoryform.is_valid():
                category = categoryform.save()
                messages.success(request, 'Category Edited Successfully')
                return redirect("product:categorypage")
            messages.error(request, str(categoryform.errors))
            return redirect("product:categorypage")
   
        
        




def add_unit(request): 
        if request.method == "POST":
            unitform = UnitForm(request.POST)
            if unitform.is_valid():
                unit = unitform.save()
                messages.success(request, 'Unit Added Successfully')
                return redirect("product:unitpage")
            messages.error(request, str(unitform.errors))
            return redirect("product:unitpage")


        
    