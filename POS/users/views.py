from django.shortcuts import render,redirect
from .forms import UserForm,GroupForm
from django.contrib.auth.models import Group,Permission
from django_tenants.utils import tenant_context,schema_context
from django_tenants.utils import get_tenant
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from authentication.models import User


# Create your views here.


def displayUsers(request):
    tenant = get_tenant(request)

    context = {
                "users": tenant.workers.all(),
                
            }
    return render(request, 'users/userslist.html',context=context)



def addUserpage(request):
    tenant = get_tenant(request)
    with schema_context(tenant.schema_name):
        context = {
            "userform": UserForm,
            'groups':Group.objects.all(),
        }
        return render(request, 'users/adduser.html', context=context)
    


def addUserProcess(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        permission = request.POST.get('permission')
        tenant=get_tenant(request)
        
        userform = UserForm(request.POST)
        if password1==password2:
            if userform.is_valid():
                with schema_context(tenant.schema_name):
                    user = userform.save()
                    user.set_password(password1)
                    if permission != "":
                        group = Group.objects.get(pk=permission)
                        if group.name == "Administrator":
                            user.is_admin = True
                            user.is_staff=True
                        user.groups.add(group)
                        user.save()
                        tenant.workers.add(user)
                        tenant.save_with_default_behavior()
                        messages.success(request, "User has been Created successfully")
                        return redirect("users:userslist")
            messages.error(request, str(userform.errors))
            return redirect("users:usersadd")
        messages.error(request, "passwords must match")
        return redirect("users:usersadd")



def edit_user_page(request, pk):
    context = {
        "userform": UserForm(instance=(User.objects.get(id=pk))),
        'groups': Group.objects.all(),
        'edit':True,
        'user':User.objects.get(id=pk)
    }
    return render(request, 'users/adduser.html', context=context)
            

def editUserProcess(request,pk):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        permission = request.POST.get('permission')
        tenant=get_tenant(request)
        user = User.objects.get(id=pk)
        
        userform = UserForm(request.POST,instance=user)
        if password1==password2:
            if userform.is_valid():
                with schema_context(tenant.schema_name):
                    user = userform.save()
                    user.set_password(password1)
                    if permission != "":
                        group = Group.objects.get(pk=permission)
                        if group.name == "Administrator":
                            user.is_admin = True
                            user.is_staff=True
                        user.groups.add(group)
                        user.save()
                        messages.success(request, "User has been Edited successfully")
                        return redirect("users:userslist")
            messages.error(request, str(userform.errors))
            return redirect("users:usersadd")
        messages.error(request, "passwords must match")
        return redirect("users:usersadd")

def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    tenant = get_tenant(request)
    if not user.is_admin:
        messages.error(request, "You don't have permission to delete a user")
        return redirect("users:userslist")
    if user == tenant.owner:
        messages.error(request, "Cannot delete Pharmacy Owner")
        return redirect("users:userslist")
    user.delete()
    messages.success(request, "User has been Deleted successfully")
    return redirect("users:userslist")

def showPermissions(request):
    tenant=get_tenant(request)
    with schema_context(tenant.schema_name):
        context = {
            "groups":Group.objects.all()
        }

        return render(request,'users/permissions.html',context=context)

def editPermissions(request, pk):
  
    group = Group.objects.get(id=pk)
    permissions = group.permissions.all()
    group_permissions = set(permission.content_type.app_label for permission in permissions)
    
    exclude_apps = ['admin', 'auth', 'sessions', 'contenttypes', 'main']

    # Get content types associated with excluded app labels
    excluded_content_types = ContentType.objects.filter(app_label__in=exclude_apps)

    # Get unique app labels from content types
    excluded_app_labels = set(excluded_content_types.values_list('app_label', flat=True))

    # Get permissions excluding those associated with excluded app labels
    all_permissions = Permission.objects.exclude(content_type__in=excluded_content_types)

    # Get unique app labels from permissions
    all_permissions = set(all_permissions.values_list('content_type__app_label', flat=True))
    
    context={
        'allpermissions': all_permissions,
        'group': Group.objects.get(id=pk),
        'group_permissions': group_permissions,
        'groupform':GroupForm(instance=group)
    }

    return render(request,'users/editpermissions.html',context=context)


def editPermissionProcess(request, pk):
    if request.method == 'POST':
        group=Group.objects.get(id=pk)
        groupform = GroupForm(request.POST,instance=group)
        if groupform.is_valid():
                tenant=get_tenant(request)
                with schema_context(tenant.schema_name):
                    group=groupform.save()
                    permissions = request.POST.getlist('permissions[]')
                    for permission in permissions:
                        if permission !="":
                            permissions_to_add = Permission.objects.filter(content_type__app_label=permission)
                            for p in permissions_to_add:
                                group.permissions.add(p)
                    group.save()
        messages.success(request, "Permissions Edited Succesfully")
        return redirect("users:permissions")
    


def createGroup(request):
    # List of app labels to exclude
    exclude_apps = ['admin', 'auth', 'sessions', 'contenttypes', 'main']

    # Get content types associated with excluded app labels
    excluded_content_types = ContentType.objects.filter(app_label__in=exclude_apps)

    # Get unique app labels from content types
    excluded_app_labels = set(excluded_content_types.values_list('app_label', flat=True))

    # Get permissions excluding those associated with excluded app labels
    all_permissions = Permission.objects.exclude(content_type__in=excluded_content_types)

    # Get unique app labels from permissions
    all_permissions = set(all_permissions.values_list('content_type__app_label', flat=True))
    
    context={
        'allpermissions': all_permissions,
        'groupform':GroupForm
    }

    return render(request, 'users/addgroup.html', context=context)
    


def addGroupProcess(request):
    if request.method=='POST':
        groupform = GroupForm(request.POST)
        if groupform.is_valid():
            tenant=get_tenant(request)
            with schema_context(tenant.schema_name):
                group=groupform.save()
                permissions = request.POST.getlist('permissions[]')
                for permission in permissions:
                    if permission !="":
                        permissions_to_add = Permission.objects.filter(content_type__app_label=permission)
                        for p in permissions_to_add:
                            group.permissions.add(p)

                group.save()
                messages.success(request, "Group Added Succesfully")
                return redirect("users:permissions")
        messages.success(request, f"{str(groupform.errors)}")
        return redirect("users:groupadd")
