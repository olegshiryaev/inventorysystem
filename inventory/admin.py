from django.contrib import admin
from .models import (
    CPU,
    MFP,
    RAM,
    Component,
    Consumable,
    ConsumableStock,
    ConsumableUsage,
    Equipment,
    EquipmentStatusHistory,
    EquipmentType,
    EquipmentModel,
    Manufacturer,
    PersonInCharge,
    Printer,
    Storage,
    Warehouse,
    SystemUnit,
    Monitor,
    Workstation,
)


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "manufacturer",
        "model",
        "type",
        "nomenclature_number",
        "created_at",
        "updated_at",
    )
    list_filter = ("type", "manufacturer")
    search_fields = ("model", "manufacturer__name", "type__name", "nomenclature_number")
    date_hierarchy = "created_at"


@admin.register(PersonInCharge)
class PersonInChargeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location")
    search_fields = ("name", "location")


@admin.register(Workstation)
class WorkstationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location")
    search_fields = ("user__email", "location")


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    search_fields = ["serial_number", "inventory_number", "model__model"]
    list_filter = [
        "status",
        "warehouse",
        "person_in_charge",
        "workstation",
        "purchase_date",
    ]
    list_display = [
        "model",
        "serial_number",
        "status",
        "person_in_charge",
        "warehouse",
        "workstation",
        "purchase_date",
    ]
    readonly_fields = ["created_at", "updated_at"]
    list_select_related = ["model", "person_in_charge", "warehouse", "workstation"]
    actions = ["mark_as_needs_repair", "mark_as_working"]

    def mark_as_needs_repair(self, request, queryset):
        queryset.update(status="needs_repair")

    mark_as_needs_repair.short_description = "Отметить как требующее ремонта"

    def mark_as_working(self, request, queryset):
        queryset.update(status="working")

    mark_as_working.short_description = "Отметить как рабочее"


@admin.register(EquipmentStatusHistory)
class EquipmentStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ["equipment", "status", "change_date", "comments"]
    search_fields = ["equipment__serial_number", "equipment__model__model"]
    list_filter = ["status", "change_date"]


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('type', 'manufacturer', 'model_name', 'status')
    list_filter = ('type', 'status', 'manufacturer')
    search_fields = ('manufacturer', 'model_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model_name', 'frequency', 'cores', 'threads', 'status')
    list_filter = ('manufacturer', 'status')
    search_fields = ('manufacturer', 'model_name', 'serial_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model_name', 'size', 'speed', 'status')
    list_filter = ('size', 'speed', 'status', 'manufacturer')
    search_fields = ('manufacturer', 'model_name', 'serial_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model_name', 'size', 'storage_type', 'status')
    list_filter = ('size', 'storage_type', 'status', 'manufacturer')
    search_fields = ('manufacturer', 'model_name', 'serial_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SystemUnit)
class SystemUnitAdmin(admin.ModelAdmin):
    list_display = EquipmentAdmin.list_display + ["cpu", 'get_ram_total', 'get_storage_total']
    list_filter = ("status", "warehouse", "person_in_charge")
    search_fields = EquipmentAdmin.search_fields + ["cpu"]
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('ram', 'storage')

    def get_cpu_display(self, obj):
        return obj.cpu if obj.cpu else 'Не указано'
    get_cpu_display.short_description = 'Процессор'

    def get_ram_total(self, obj):
        return obj.get_ram_total() if obj.ram.exists() else 'Не указано'
    get_ram_total.short_description = 'Оперативная память (ГБ)'

    def get_storage_total(self, obj):
        return obj.get_storage_total() if obj.storage.exists() else 'Не указано'
    get_storage_total.short_description = 'Накопитель (ГБ)' 


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = EquipmentAdmin.list_display + ["resolution", "size"]
    list_filter = ("status", "warehouse", "person_in_charge")
    search_fields = EquipmentAdmin.search_fields + ["resolution", "size"]


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('model', 'serial_number', 'printer_type', 'color', 'duplex', 'network', 'status')
    list_filter = ('printer_type', 'color', 'duplex', 'network', 'status')
    search_fields = ('model__name', 'serial_number', 'inventory_number', 'code')


@admin.register(MFP)
class MFPAdmin(admin.ModelAdmin):
    list_display = ('model', 'serial_number', 'mfp_type', 'color', 'duplex', 'network', 'scanner', 'copier', 'fax', 'status')
    list_filter = ('mfp_type', 'color', 'duplex', 'network', 'scanner', 'copier', 'fax', 'status')
    search_fields = ('model__name', 'serial_number', 'inventory_number', 'code')


@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ('model', 'manufacturer', 'consumable_type')
    list_filter = ('consumable_type', 'manufacturer')
    search_fields = ('model', 'manufacturer')

@admin.register(ConsumableStock)
class ConsumableStockAdmin(admin.ModelAdmin):
    list_display = ('consumable', 'warehouse', 'quantity')
    list_filter = ('warehouse',)
    search_fields = ('warehouse__name',)

@admin.register(ConsumableUsage)
class ConsumableUsageAdmin(admin.ModelAdmin):
    list_display = ('consumable', 'equipment', 'warehouse', 'installation_date', 'installed_by')
    list_filter = ('installation_date', 'installed_by', 'warehouse')
    search_fields = ('equipment__model', 'warehouse__name',)