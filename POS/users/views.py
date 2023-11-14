from django.shortcuts import render,redirect
from .forms import UserForm,GroupForm
from django.contrib.auth.models import Group,Permission
from django_tenants.utils import tenant_context,schema_context
from django_tenants.utils import get_tenant
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from authentication.models import User
<<<<<<< HEAD

=======
>>>>>>> 4c06f3e6412e08eb08a5f31a74fb0b63f4e12c52


# Create your views here.


def displayUsers(request):
    tenant = get_tenant(request)
<<<<<<< HEAD

    context = {
                "users": tenant.workers.all(),
                
            }
=======
    with tenant_context(tenant):
        context = {
            'users':User.objects.all()
        }

>>>>>>> 4c06f3e6412e08eb08a5f31a74fb0b63f4e12c52
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
    tenant=get_tenant(request)
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
       # Get the content types to exclude
    exclude_apps = ['admin', 'auth', 'sessions', 'contenttypes','main']
    excluded_content_types = ContentType.objects.filter(app_label__in=exclude_apps)

    # Retrieve all permissions excluding those from the excluded content types
    all_permissions = Permission.objects.exclude(content_type__in=excluded_content_types)
    
    user_group_permissions = Group.objects.get(id=pk).permissions.all() if request.user.groups.exists() else set()
   
    apps_permissions = {}
    for permission in all_permissions:
        app_name = permission.content_type.app_label
        if app_name not in apps_permissions:
            apps_permissions[app_name] = {'permissions': []}
        apps_permissions[app_name]['permissions'].append({
            'name': permission.name,
            'codename': permission.codename,
            'in_user_group': permission in user_group_permissions,
            "id":permission.id
        })
    
    context={
        'apps_permissions': apps_permissions,
        'group':Group.objects.get(id=pk)
    }

    return render(request,'users/editpermissions.html',context=context)


def editPermissionProcess(request, pk):
    if request.method=='POST':
        group = Group.objects.get(id=pk)
        permissions = request.POST.getlist('permissions[]')
        group.permissions.clear()
        for permission in permissions:
            if permission !="":
                permissionitem = Permission.objects.get(pk=permission)
                group.permissions.add(permissionitem)
        group.save()
        messages.success(request, "Permissions Edited Succesfully")
        return redirect("users:permissions")
    


def createGroup(request):
          # Get the content types to exclude
    exclude_apps = ['admin', 'auth', 'sessions', 'contenttypes','main']
    excluded_content_types = ContentType.objects.filter(app_label__in=exclude_apps)

    # Retrieve all permissions excluding those from the excluded content types
    all_permissions = Permission.objects.exclude(content_type__in=excluded_content_types)
    
   
    apps_permissions = {}
    for permission in all_permissions:
        app_name = permission.content_type.app_label
        if app_name not in apps_permissions:
            apps_permissions[app_name] = {'permissions': []}
        apps_permissions[app_name]['permissions'].append({
            'name': permission.name,
            'codename': permission.codename,
            "id":permission.id
        })
    
    context={
        'apps_permissions': apps_permissions,
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
                        permissionitem = Permission.objects.get(pk=permission)
                        group.permissions.add(permissionitem)
                group.save()
                messages.success(request, "Group Added Succesfully")
                return redirect("users:permissions")
        messages.success(request, f"{str(groupform.errors)}")
        return redirect("users:groupadd")
