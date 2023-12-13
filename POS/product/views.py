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




# Create your views here.


def showAddCategory(request):
    context = {
        "categorys": Category.objects.all().order_by("-id"),
        "form": CategoryForm,
    }
    return render(request, "product/addcategory.html", context=context)


def showCategoryList(request):
    context = {
        "categorys": Category.objects.all().order_by("-id"),
    }

    return render(request, "product/categorylist.html", context=context)


def showAddSubCategory(request):
    context = {
        "subcategorys": Subcategory.objects.all().order_by("-id"),
        "form": SubcategoryForm,
    }
    return render(request, "product/subcategory.html", context=context)


def showSubCategoryList(request):
    context = {
        "subcategorys": Subcategory.objects.all().order_by("-id"),
    }
    return render(request, "product/subcategorylist.html", context=context)


def showAddProduct(request):

    # suppliers = Supplier.objects.all()
    context = {
   
        "form": ProductForm,
    }

    return render(request, "product/addproduct.html", context=context)


def addProductProcess(request):
    if request.method == "POST":
        productform = ProductForm(request.POST,request.FILES)
        if productform.is_valid():
            product = productform.save()
            messages.success(request, "Product Added Successfully")
            return redirect("product:productlist")
        messages.error(request, str(productform.errors))
        return redirect("product:productpage")


def showProducts(request):
    context = {
        'products':Product_Item.objects.all().order_by("-id")
    }

    return render(request, "product/productlist.html", context=context)


def editProduct(request, pk):
    product = Product_Item.objects.get(id=pk)
    # suppliers = Supplier.objects.all()
    context = {
        
        "form": ProductForm(instance=product),
        'edit': True,
        'product':product
    }

    return render(request, "product/addproduct.html", context=context)

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



def delete_product(request, pk):
    if Product_Item.objects.filter(id=pk).exists():
        product = Product_Item.objects.get(id=pk)
        product.delete()
        messages.success(request, "Product Deleted Successfully")
        return redirect("product:productlist")
    messages.error(request, "Error Try Agian")
    return redirect("product:productlist")
    
def showAddUnit(request):
    context = {"form": UnitForm, "units": Unit.objects.all().order_by("-id")}
    return render(request, "product/unit.html", context=context)


def showUnitList(request):
    context = {"units": Unit.objects.all().order_by("-id")}
    return render(request, "product/unitlist.html", context=context)


def add_unit_process(request):
    if request.method == "POST":
        unitform = UnitForm(request.POST)
        if unitform.is_valid():
            unit = unitform.save()
            messages.success(request, "Unit added Successfully")
            return redirect("product:unitpage")
        messages.error(request, str(unitform.errors))
        return redirect("product:unitpage")


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


def delete_unit(request, pk):
    if Unit.objects.filter(id=pk).exists():
        unit = Unit.objects.get(id=pk)
        unit.delete()
        messages.success(request, "Unit Deleted Successfully")
        return redirect("product:unitlist")
    messages.error(request, "Error Try Agian")
    return redirect("product:unitlist")


def add_subcategory(request):
    if request.method == "POST":
        subcategoryform = SubcategoryForm(request.POST)
        if subcategoryform.is_valid():
            subcategory = subcategoryform.save()
            messages.success(request, "Subcategory Added Successfully")
            return redirect("product:subcategorypage")
        messages.error(request, str(subcategoryform.errors))
        return redirect("product:subcategorypage")


def delete_subcategory(request, pk):
    if Subcategory.objects.filter(id=pk).exists():
        subcategory = Subcategory.objects.get(id=pk)
        subcategory.delete()
        messages.success(request, "Subcategory Deleted Successfully")
        return redirect("product:subcategory_list")
    messages.error(request, "Error Try Agian")
    return redirect("product:subcategory_list")


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


def add_category(request):
    if request.method == "POST":
        categoryform = CategoryForm(request.POST)
        if categoryform.is_valid():
            category = categoryform.save()
            messages.success(request, "Category Added Successfully")
            return redirect("product:categorypage")
        messages.error(request, str(categoryform.errors))
        return redirect("product:categorypage")


def delete_category(request, pk):
    if Category.objects.filter(id=pk).exists():
        category = Category.objects.get(id=pk)
        category.delete()
        messages.success(request, "Category Deleted Successfully")
        return redirect("product:categorylist")
    messages.error(request, "Error Try Agian")
    return redirect("product:categorylist")


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


def add_unit(request):
    if request.method == "POST":
        unitform = UnitForm(request.POST)
        if unitform.is_valid():
            unit = unitform.save()
            messages.success(request, "Unit Added Successfully")
            return redirect("product:unitpage")
        messages.error(request, str(unitform.errors))
        return redirect("product:unitpage")


def create_categories_from_excel(request):
    try:
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            if excel_file.name.endswith(".xls") or excel_file.name.endswith(".xlsx"):
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    name = row["name"]
                    code = row["code"]
                    Category.objects.create(name=name, code=code)
                messages.success(request, "Category Added Successfully")
                return redirect("product:categorylist")
    except Exception as e:
        messages.error(request, f"{str(e)}")
        return redirect("product:categorypage")


def create_subcategories_from_excel(request):
    try:
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            if excel_file.name.endswith(".xls") or excel_file.name.endswith(".xlsx"):
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    name = row["name"]
                    code = row["code"]
                    Subcategory.objects.create(name=name, code=code)
                messages.success(request, "Subcategory Added Successfully")
                return redirect("product:subcategory_list")
    except Exception as e:
        messages.error(request, f"{str(e)}")
        return redirect("product:subcategorypage")


def create_units_from_excel(request):
    try:
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            if excel_file.name.endswith(".xls") or excel_file.name.endswith(".xlsx"):
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    name = row["name"]
                    shorthand = row["shorthand"]
                    Unit.objects.create(name=name, shorthand=shorthand)
                messages.success(request, "Unit Added Successfully")
                return redirect("product:unitlist")
    except Exception as e:
        messages.error(request, f"{str(e)}")
        return redirect("product:unitpage")





def showAddPackage(request):
    context = {
        "packageform": PackageForm,
        'packages':Package.objects.all(),
    }
    return render(request, 'product/addpackage.html', context=context)




    

def addPackage(request):
    if request.method == 'POST':
        packageform = PackageForm(request.POST)
        if packageform.is_valid():
            package = packageform.save()
            messages.success(request, "Package Added Successfully")
            return redirect("product:add_package")
        messages.error(request, str(packageform.errors))
        return redirect("product:unitpage")
        



def export_products_as_pdf(request):
    template = get_template('product/pdf.html')  # Replace with your actual template name
    html_content = template.render({
        'products': Product_Item.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    })  # Replace with your actual data

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="preview.pdf"'
    return response



def export_categories_as_pdf(request):
    template = get_template('product/categorypdf.html')  # Replace with your actual template name
    html_content = template.render({
        'categorys': Category.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    })  # Replace with your actual data

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="preview.pdf"'
    return response

def export_subcategories_as_pdf(request):
    template = get_template('product/subcategorypdf.html')  # Replace with your actual template name
    html_content = template.render({
        'subcategorys': Subcategory.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    })  # Replace with your actual data

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="preview.pdf"'
    return response



def export_products_to_excel(request):
    # Query the data you want to export
    products = Product_Item.objects.all()

    # Create a DataFrame from the queryset
    data = {
        'Product Name': [product.name for product in products],
        'Category': [product.category for product in products],
        'Cost Price': [product.cost_price for product in products],
        'Selling Price': [product.selling_price for product in products],
        # Add more fields as needed
    }

    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    output = BytesIO()

    # Use pandas to write the Excel file to the BytesIO object using openpyxl engine
    df.to_excel(output, engine='openpyxl', index=False, sheet_name='Products')

    # Set up the response
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'

    return response

    # Query the data you want to export
    products = Product_Item.objects.all()

    # Create a DataFrame from the queryset
    data = {
        'Product Name': [product.name for product in products],
        'Category': [product.category for product in products],
        'Cost Price': [product.cost_price for product in products],
        'Selling Price': [product.selling_price for product in products],
        # Add more fields as needed
    }

    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    output = BytesIO()

    # Use pandas to write the Excel file to the BytesIO object
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Products', index=False)
    writer.save()
    writer.close()

    # Set up the response
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'

    return response