from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('my_equipment/', views.user_equipment_list, name='user_equipment_list'),
    path('mol_equipment/', views.mol_equipment_view, name='mol_equipment'),
]