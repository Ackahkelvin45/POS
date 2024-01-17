from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.displayUsers, name='userslist'),
    path('add/', views.addUserpage, name='usersadd'),
     path('edit/<int:pk>/', views.edit_user_page, name='usersedit'),
      path('delte/<int:pk>/', views.deleteUser, name='usersdelete'),
    path('add_group/', views.createGroup, name='groupadd'), 
    path("add_user_process/", views.addUserProcess, name="add_user_process"),
     path("edit_user_process/<int:pk>/", views.editUserProcess, name="edit_user_process"),
     path("add_group_process/", views.addGroupProcess, name="add_group_process"),
    path("permissions/list/", views.showPermissions, name='permissions'),
    path("permissions/edit/<int:pk>/", views.editPermissions, name='editpermissions'),
    path("permissions_process/edit/<int:pk>/", views.editPermissionProcess, name='editpermissionsprocess'),
 path("profile/", views.profilepage, name='profilepage'),

    
]