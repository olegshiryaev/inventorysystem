from django.urls import path
from . import views


app_name = 'inventory'

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/new/', views.equipment_new, name='equipment_new'),
    path('equipment/<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment_model/', views.equipment_model_list, name='equipment_model_list'),
    path('equipment_model/<int:pk>/', views.equipment_model_detail, name='equipment_model_detail'),
    path('equipment_model/new/', views.equipment_model_new, name='equipment_model_new'),
    path('equipment_model/<int:pk>/edit/', views.equipment_model_edit, name='equipment_model_edit'),
]