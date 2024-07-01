from django.urls import path
from . import views


app_name = 'inventory'

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('create/', views.equipment_create, name='equipment_create'),
    path('<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
    path('scan/', views.scan_barcode, name='scan_barcode'),
    path('search/', views.search_equipment, name='search_equipment'),
    path('equipment_model/', views.equipment_model_list, name='equipment_model_list'),
    path('equipment_model/<int:pk>/', views.equipment_model_detail, name='equipment_model_detail'),
    path('equipment_model/new/', views.equipment_model_new, name='equipment_model_new'),
    path('equipment_model/<int:pk>/edit/', views.equipment_model_edit, name='equipment_model_edit'),
]