from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_tenants.utils import get_tenant, schema_context
from django.contrib import messages
from django.http import HttpResponse
from .models import Unit, Subcategory, Category,Product_Item,Package
from .forms import SubcategoryForm, CategoryForm, UnitForm, ProductForm,PackageForm
import pandas as pd
from io import BytesIO
from django.http import FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pdfkit
from stock.models import StockEntry
from django.utils import timezone




# Create your views here.

@login_required(login_url='tenant:login')
def showAddCategory(request):
    context = {
        "categorys": Category.objects.all().order_by("-id"),
        "form": CategoryForm,
    }
    return render(request, "product/addcategory.html", context=context)

@login_required(login_url='tenant:login')
def showCategoryList(request):
    context = {
        "categorys": Category.objects.all().order_by("-id"),
    }

    return render(request, "product/categorylist.html", context=context)

@login_required(login_url='tenant:login')
def showAddSubCategory(request):
    context = {
        "subcategorys": Subcategory.objects.all().order_by("-id"),
        "form": SubcategoryForm,
    }
    return render(request, "product/subcategory.html", context=context)

@login_required(login_url='tenant:login')
def showSubCategoryList(request):
    context = {
        "subcategorys": Subcategory.objects.all().order_by("-id"),
    }
    return render(request, "product/subcategorylist.html", context=context)

@login_required(login_url='tenant:login')
def showAddProduct(request):

    # suppliers = Supplier.objects.all()
    context = {
   
        "form": ProductForm,
    }

    return render(request, "product/addproduct.html", context=context)

@login_required(login_url='tenant:login')
def addProductProcess(request):
    if request.method == "POST":
        productform = ProductForm(request.POST,request.FILES)
        if productform.is_valid():
            product = productform.save()
            messages.success(request, "Product Added Successfully")
            return redirect("product:productlist")
        messages.error(request, str(productform.errors))
        return redirect("product:productpage")

@login_required(login_url='tenant:login')
def showProducts(request):
    context = {
        'products':Product_Item.objects.all().order_by("-id")
    }

    return render(request, "product/productlist.html", context=context)

@login_required(login_url='tenant:login')
def editProduct(request, pk):
    product = Product_Item.objects.get(id=pk)
    # suppliers = Supplier.objects.all()
    context = {
        
        "form": ProductForm(instance=product),
        'edit': True,
        'product':product
    }

    return render(request, "product/addproduct.html", context=context)
@login_required(login_url='tenant:login')
def edit_product_process(request, pk):
     if request.method == "POST":
        product = Product_Item.objects.get(id=pk)
        productform = ProductForm(request.POST,request.FILES,instance=product)
        if productform.is_valid():
            product = productform.save()
            messages.success(request, "Product  Edited Successfully")
            return redirect("product:productlist")
        messages.error(request, str(productform.errors))
        return redirect("product:productpage")


@login_required(login_url='tenant:login')
def delete_product(request, pk):
    if Product_Item.objects.filter(id=pk).exists():
        product = Product_Item.objects.get(id=pk)
        product.delete()
        messages.success(request, "Product Deleted Successfully")
        return redirect("product:productlist")
    messages.error(request, "Error Try Agian")
    return redirect("product:productlist")

@login_required(login_url='tenant:login')   
def showAddUnit(request):
    context = {"form": UnitForm, "units": Unit.objects.all().order_by("-id")}
    return render(request, "product/unit.html", context=context)

@login_required(login_url='tenant:login')
def showUnitList(request):
    context = {"units": Unit.objects.all().order_by("-id")}
    return render(request, "product/unitlist.html", context=context)

@login_required(login_url='tenant:login')
def add_unit_process(request):
    if request.method == "POST":
        unitform = UnitForm(request.POST)
        if unitform.is_valid():
            unit = unitform.save()
            messages.success(request, "Unit added Successfully")
            return redirect("product:unitpage")
        messages.error(request, str(unitform.errors))
        return redirect("product:unitpage")

@login_required(login_url='tenant:login')
def edit_unit(request, pk):
    if Unit.objects.filter(id=pk).exists():
        unit = Unit.objects.get(id=pk)
        context = {
            "units": Unit.objects.all().order_by("-id"),
            "form": UnitForm(instance=unit),
            "edit": True,
            "unit_item": unit,
        }
        return render(request, "product/unit.html", context=context)

@login_required(login_url='tenant:login')
def edit_unit_process(request, pk):
    if request.method == "POST":
        if Unit.objects.filter(id=pk).exists():
            unit = Unit.objects.get(id=pk)
            unitform = UnitForm(request.POST, instance=unit)
            if unitform.is_valid():
                unit = unitform.save()
                messages.success(request, "Unit Edited Successfully")
                return redirect("product:unitlist")
            messages.error(request, str(unitform.errors))
            return redirect("product:unitlist")

@login_required(login_url='tenant:login')
def delete_unit(request, pk):
    if Unit.objects.filter(id=pk).exists():
        unit = Unit.objects.get(id=pk)
        unit.delete()
        messages.success(request, "Unit Deleted Successfully")
        return redirect("product:unitlist")
    messages.error(request, "Error Try Agian")
    return redirect("product:unitlist")

@login_required(login_url='tenant:login')
def add_subcategory(request):
    if request.method == "POST":
        subcategoryform = SubcategoryForm(request.POST)
        if subcategoryform.is_valid():
            subcategory = subcategoryform.save()
            messages.success(request, "Subcategory Added Successfully")
            return redirect("product:subcategorypage")
        messages.error(request, str(subcategoryform.errors))
        return redirect("product:subcategorypage")

@login_required(login_url='tenant:login')
def delete_subcategory(request, pk):
    if Subcategory.objects.filter(id=pk).exists():
        subcategory = Subcategory.objects.get(id=pk)
        subcategory.delete()
        messages.success(request, "Subcategory Deleted Successfully")
        return redirect("product:subcategory_list")
    messages.error(request, "Error Try Agian")
    return redirect("product:subcategory_list")

@login_required(login_url='tenant:login')
def edit_subcategory(request, pk):
    if Subcategory.objects.filter(id=pk).exists():
        subcategory = Subcategory.objects.get(id=pk)
        context = {
            "subcategorys": Subcategory.objects.all().order_by("-id"),
            "form": SubcategoryForm(instance=subcategory),
            "edit": True,
            "subcategory_item": subcategory,
        }
        return render(request, "product/subcategory.html", context=context)


def edit_subcategory_process(request, pk):
    if request.method == "POST":
        if Subcategory.objects.filter(id=pk).exists():
            subcategory = Subcategory.objects.get(id=pk)
            subcategoryform = SubcategoryForm(request.POST, instance=subcategory)
            if subcategoryform.is_valid():
                subcategory = subcategoryform.save()
                messages.success(request, "Subcategory Edited Successfully")
                return redirect("product:subcategory_list")
            messages.error(request, str(subcategoryform.errors))
            return redirect("product:subcategory_list")

@login_required(login_url='tenant:login')
def add_category(request):
    if request.method == "POST":
        categoryform = CategoryForm(request.POST)
        if categoryform.is_valid():
            category = categoryform.save()
            messages.success(request, "Category Added Successfully")
            return redirect("product:categorypage")
        messages.error(request, str(categoryform.errors))
        return redirect("product:categorypage")

@login_required(login_url='tenant:login')
def delete_category(request, pk):
    if Category.objects.filter(id=pk).exists():
        category = Category.objects.get(id=pk)
        category.delete()
        messages.success(request, "Category Deleted Successfully")
        return redirect("product:categorylist")
    messages.error(request, "Error Try Agian")
    return redirect("product:categorylist")

@login_required(login_url='tenant:login')
def edit_category(request, pk):
    if Category.objects.filter(id=pk).exists():
        category = Category.objects.get(id=pk)
        context = {
            "categorys": Category.objects.all().order_by("-id"),
            "form": CategoryForm(instance=category),
            "edit": True,
            "category_item": category,
        }
        return render(request, "product/addcategory.html", context=context)

@login_required(login_url='tenant:login')
def edit_category_process(request, pk):
    if request.method == "POST":
        if Category.objects.filter(id=pk).exists():
            category = Category.objects.get(id=pk)
            categoryform = CategoryForm(request.POST, instance=category)
            if categoryform.is_valid():
                category = categoryform.save()
                messages.success(request, "Category Edited Successfully")
                return redirect("product:categorylist")
            messages.error(request, str(categoryform.errors))
            return redirect("product:categorylist")

@login_required(login_url='tenant:login')
def add_unit(request):
    if request.method == "POST":
        unitform = UnitForm(request.POST)
        if unitform.is_valid():
            unit = unitform.save()
            messages.success(request, "Unit Added Successfully")
            return redirect("product:unitpage")
        messages.error(request, str(unitform.errors))
        return redirect("product:unitpage")
@login_required(login_url='tenant:login')
def create_categories_from_excel(request):
    try:
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            if excel_file.name.lower().endswith((".xls", ".xlsx")):
                df = pd.read_excel(excel_file)
                
                # Use a case-insensitive check for the "Name" column
                name_column = next((col for col in df.columns if col.lower() == "name"), None)
                
                # Use a case-insensitive check for the "Code" column
                code_column = next((col for col in df.columns if col.lower() == "code"), None)
                
                if name_column is not None and code_column is not None:
                    for index, row in df.iterrows():
                        name = row[name_column].lower() if pd.notna(row[name_column]) else ""
                        code = row[code_column] if pd.notna(row[code_column]) else ""
                        Category.objects.create(name=name, code=code)
                    
                    messages.success(request, "Category Added Successfully")
                    return redirect("product:categorylist")
                messages.error(request, "Please make sure you have the right rows and colums")
                return redirect("product:categorypage")
            messages.error(request, "Try again with the correct file")
            return redirect("product:categorypage")
    except Exception as e:
        messages.error(request, f"{str(e)}")
        return redirect("product:categorypage")


@login_required(login_url='tenant:login')
def create_subcategories_from_excel(request):
    try:
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            if excel_file.name.lower().endswith((".xls", ".xlsx")):
                df = pd.read_excel(excel_file)
                
                # Use a case-insensitive check for the "Name" column
                name_column = next((col for col in df.columns if col.lower() == "name"), None)
                
                # Use a case-insensitive check for the "Code" column
                code_column = next((col for col in df.columns if col.lower() == "code"), None)
                
                if name_column is not None and code_column is not None:
                    for index, row in df.iterrows():
                        name = row[name_column].lower() if pd.notna(row[name_column]) else ""
                        code = row[code_column] if pd.notna(row[code_column]) else ""
                        Subcategory.objects.create(name=name, code=code)
                    
                    messages.success(request, "Subcategory Added Successfully")
                    return redirect("product:subcategory_list")
                messages.error(request, "Please make sure you have the right rows and colums")
                return redirect("product:subcategorypage") 
            messages.error(request, "Try again with the correct file")
            return redirect("product:subcategorypage")
    except Exception as e:
        messages.error(request, f"{str(e)}")
        return redirect("product:subcategorypage")

@login_required(login_url='tenant:login')
def create_units_from_excel(request):
    try:
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            if excel_file.name.lower().endswith((".xls", ".xlsx")):
                df = pd.read_excel(excel_file)

                # Use a case-insensitive check for the "Name" column
                name_column = next((col for col in df.columns if col.lower() == "name"), None)

                # Use a case-insensitive check for the "Shorthand" column
                shorthand_column = next((col for col in df.columns if col.lower() == "shorthand"), None)

                if name_column is not None and shorthand_column is not None:
                    for index, row in df.iterrows():
                        name = row[name_column].lower() if pd.notna(row[name_column]) else ""
                        shorthand = row[shorthand_column].lower() if pd.notna(row[shorthand_column]) else ""
                        Unit.objects.create(name=name, shorthand=shorthand)

                    messages.success(request, "Units Added Successfully")
                    return redirect("product:unitlist")
                messages.error(request, "Please make sure you have the right rows and colums")
                return redirect("product:unitpage") 
            messages.error(request, "Try again with the correct file")
            return redirect("product:unitpage")

    except Exception as e:
        messages.error(request, f"{str(e)}")

    return redirect("product:unitpage")





@login_required(login_url='tenant:login')
def showAddPackage(request):
    context = {
        "packageform": PackageForm,
        'packages':Package.objects.all(),
    }
    return render(request, 'product/addpackage.html', context=context)




    
@login_required(login_url='tenant:login')
def addPackage(request):
    if request.method == 'POST':
        packageform = PackageForm(request.POST)
        if packageform.is_valid():
            package = packageform.save()
            package.unit = package.product.item_unit
            package.save()
            messages.success(request, "Package Added Successfully")
            return redirect("product:add_package")
        messages.error(request, str(packageform.errors))
        return redirect("product:unitpage")
        


@login_required(login_url='tenant:login')
def export_products_as_pdf(request):
    template = get_template('product/pdf.html')  
    html_content = template.render({
        'products': Product_Item.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    })  

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="products.pdf"'
    return response

@login_required(login_url='tenant:login')
def export_packages_as_pdf(request):
    template = get_template('product/packagespdf.html')  
    html_content = template.render({
        'products': Package.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    })  

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="packages.pdf"'
    return response

@login_required(login_url='tenant:login')
def export_categories_as_pdf(request):
    template = get_template('product/categorypdf.html')  
    html_content = template.render({
        'categorys': Category.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    }) 

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="categories.pdf"'
    return response
@login_required(login_url='tenant:login')
def export_subcategories_as_pdf(request):
    template = get_template('product/subcategorypdf.html')  
    html_content = template.render({
        'subcategorys': Subcategory.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    })

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="subcategories.pdf"'
    return response

@login_required(login_url='tenant:login')
def export_units_as_pdf(request):
    template = get_template('product/unitpdf.html')  
    html_content = template.render({
        'units': Unit.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    })  

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="units.pdf"'
    return response


@login_required(login_url='tenant:login')
def export_products_to_excel(request):
    
    products = Product_Item.objects.all()

   
    data = {
        'Product Name': [product.name for product in products],
        'Code': [product.code for product in products],
        'Category': [product.category for product in products],
        'Sub Category':[product.subcategory for product in products],
        'Cost Price': [product.cost_price for product in products],
        'Selling Price': [product.selling_price for product in products],
        'Unit': [product.item_unit for product in products],
        'profit margin': [product.profit_margin for product in products],
        'mark up': [product.markup for product in products],
        'Available Quantity': [product.available_quantity for product in products],
        'Location': [product.location for product in products],
        'Suplier':[product.supplier.company_name for product in products]
        
    
       
    }

    df = pd.DataFrame(data)

    output = BytesIO()

 
    df.to_excel(output, engine='openpyxl', index=False, sheet_name='Products')

 
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'

    return response



@login_required(login_url='tenant:login')
def export_package_to_excel(request):
    
    products = Package.objects.all()

   
    data = {
        'Package Name': [product.package_name for product in products],
        'Product': [product.product.name for product in products],
        'number of products item': [product.number_of_products_item for product in products],
        'unit':[product.unit for product in products],
        'Cost Price': [product.cost_price for product in products],
        'Selling Price': [product.selling_price for product in products],
        'Available Quantity': [product.available_quantity for product in products],
     
        
    
       
    }

    df = pd.DataFrame(data)

    output = BytesIO()

 
    df.to_excel(output, engine='openpyxl', index=False, sheet_name='Packages')

 
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=packages.xlsx'

    return response



@login_required(login_url='tenant:login')
def export_categories_to_excel(request):
    
    categories=Category.objects.all()

   
    data = {
        'Name': [category.name for category in categories],
        'Code': [category.code for category in categories],
     
      
        
    
       
    }

    df = pd.DataFrame(data)

    output = BytesIO()

 
    df.to_excel(output, engine='openpyxl', index=False, sheet_name='Categories')

 
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=categories.xlsx'

    return response




@login_required(login_url='tenant:login')
def export_subcategories_to_excel(request):
    
    subcategories=Subcategory.objects.all()

   
    data = {
        'Name': [subcategory.name for subcategory in subcategories],
        'Code': [subcategory.code for subcategory in subcategories],
     
      
        
    
       
    }

    df = pd.DataFrame(data)

    output = BytesIO()

 
    df.to_excel(output, engine='openpyxl', index=False, sheet_name='Subcategories')

 
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=subcategories.xlsx'

    return response

@login_required(login_url='tenant:login')
def export_units_to_excel(request):
    
    units=Unit.objects.all()

   
    data = {
        'Name': [unit.name for unit in units],
        'Shorthand': [unit.shorthand for unit in units],
     
      
        
    
       
    }

    df = pd.DataFrame(data)

    output = BytesIO()

 
    df.to_excel(output, engine='openpyxl', index=False, sheet_name='Units')

 
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=units.xlsx'

    return response
@login_required(login_url='tenant:login')
def reset_product_to_zero(request):
    products = Product_Item.objects.all()
    for product in products:
        product.available_quantity = 0
        product.save()
    messages.success(request, "Quantity has been reset ")
    return redirect("product:productlist")
@login_required(login_url='tenant:login')
def reset_package_to_zero(request):
    products = Package.objects.all()
    for product in products:
        product.available_quantity = 0
        product.save()
    messages.success(request, "Quantity has been reset ")
    return redirect("product:add_package")


@login_required(login_url='tenant:login')
def delete_all_categories(request):
    categories = Category.objects.all()
    for category in categories:
        category.delete()
    messages.success(request, "All catgories Deleted Successfully")
    return redirect("product:categorylist")
@login_required(login_url='tenant:login')
def delete_all_subcategories(request):
    subcategories = Subcategory.objects.all()
    for subcategory in subcategories:
        subcategory.delete()
    messages.success(request, "All subcatgories Deleted Successfully")
    return redirect("product:subcategory_list")

@login_required(login_url='tenant:login')
def delete_all_units(request):
    units = Unit.objects.all()
    for unit in units:
        unit.delete()
    messages.success(request, "All Units Deleted Successfully")
    return redirect("product:unitlist")


@login_required(login_url='tenant:login')
def update_quantity_in_bulk(request):
    if request.method == 'POST':
        percentage = request.POST['percentage']
        amount = request.POST['amount']
        products=Product_Item.objects.all()
        if amount != "":
            amount = int(amount)
            for product in products:

                stock = StockEntry.objects.create(product=product,
                quantity_received=amount,
                previous_quantity=product.available_quantity,
                info=f'{product.name} updated by {amount},bulk process',
                user=request.user,
                created_at=timezone.now(),

                
                )
                stock.add_to_stock()
                stock.available_quantity = product.available_quantity
                stock.save()
            messages.success(request, "All Product Quantity Updated successfully")
            return redirect("product:productlist")
        if percentage != "":

            percentage = int(percentage)
            percentage_decimal = percentage / 100.0

            for product in products:
                new_quantity = product.available_quantity * (1 + percentage_decimal)

                stock = StockEntry.objects.create(product=product,
                quantity_received=new_quantity ,
                previous_quantity=product.available_quantity,
                info=f'{product.name} updated by {amount},bulk process',
                user=request.user,
                created_at=timezone.now(),

                
                )
                stock.add_to_stock()
                stock.available_quantity = product.available_quantity
                stock.save()
            messages.success(request, "All Product Quantity Updated successfully")
            return redirect("product:productlist")
            
        
        messages.success(request, "All Product Quantity Updated successfully")
        return redirect("product:productlist")        


@login_required(login_url='tenant:login')
def update_packages_quantity_in_bulk(request):
    if request.method == 'POST':
        percentage = request.POST['percentage']
        amount = request.POST['amount']
        products=Package.objects.all()
        if amount != "":
            amount = int(amount)
            for product in products:

                stock = StockEntry.objects.create(product=product.product,
                package_type=product,
                quantity_received=amount,
                previous_quantity=product.available_quantity,
                info=f'{product.package_name} updated by {amount},bulk process',
                user=request.user,
                created_at=timezone.now(),

                
                )
                stock.add_to_stock()
                stock.available_quantity = product.available_quantity
                stock.save()
            messages.success(request, "All  Package  Quantity Updated successfully")
            return redirect("product:add_package")
        if percentage != "":

            percentage = int(percentage)
            percentage_decimal = percentage / 100.0

            for product in products:
                new_quantity = product.available_quantity * (1 + percentage_decimal)

                stock = StockEntry.objects.create(product=product.product,
                quantity_received=new_quantity,
                package_type=product,
                previous_quantity=product.available_quantity,
                info=f'{product.package_name} updated by {amount},bulk process',
                user=request.user,
                created_at=timezone.now(),

                
                )
                stock.add_to_stock()
                stock.available_quantity = product.available_quantity
                stock.save()
            messages.success(request, "All Package   Quantity Updated successfully")
            return redirect("product:add_package")
   
