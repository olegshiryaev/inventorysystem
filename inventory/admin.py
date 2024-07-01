from django.contrib import admin
from .models import EquipmentType, EquipmentModel, Manufacturer, PersonInCharge, Warehouse, SystemUnit, Monitor

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
    list_display = ('id', 'manufacturer', 'model', 'type', 'nomenclature_number', 'created_at', 'updated_at')
    list_filter = ('type', 'manufacturer')
    search_fields = ('model', 'manufacturer__name', 'type__name', 'nomenclature_number')
    date_hierarchy = 'created_at'

@admin.register(PersonInCharge)
class PersonInChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name', 'location')

@admin.register(SystemUnit)
class SystemUnitAdmin(admin.ModelAdmin):
    list_display = ('model', 'code', 'serial_number', 'person_in_charge', 'status')
    list_filter = ('status', 'warehouse', 'person_in_charge')
    search_fields = ('model__model', 'serial_number', 'code')

@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('model', 'code', 'serial_number', 'person_in_charge', 'status')
    list_filter = ('status', 'warehouse', 'person_in_charge')
    search_fields = ('model__model', 'serial_number', 'code')