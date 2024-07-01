from django.contrib import admin
from .models import EquipmentType, EquipmentModel, Equipment, Manufacturer, PersonInCharge, Warehouse

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'manufacturer', 'model', 'type', 'created_at', 'updated_at')
    list_filter = ('type', 'manufacturer')
    search_fields = ('model', 'manufacturer__name', 'type__name')
    date_hierarchy = 'created_at'

@admin.register(PersonInCharge)
class PersonInChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name', 'location')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'serial_number', 'inventory_number', 'nomenclature_number', 'code', 'status', 'person_in_charge', 'warehouse', 'purchase_date', 'warranty_expiry_date')
    list_filter = ('model', 'person_in_charge', 'warehouse', 'status', 'purchase_date', 'warranty_expiry_date')
    search_fields = ('serial_number', 'inventory_number', 'nomenclature_number', 'code', 'model')