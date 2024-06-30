from django.contrib import admin
from .models import EquipmentType, EquipmentModel, Equipment, Manufacturer

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'manufacturer')
    search_fields = ('manufacturer', 'model')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'purchase_date', 'warranty_expiry_date')
    list_filter = ('model', 'purchase_date', 'warranty_expiry_date')
    search_fields = ('serial_number', 'model')