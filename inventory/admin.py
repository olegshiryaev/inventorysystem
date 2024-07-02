from django.contrib import admin
from .models import (
    Equipment,
    EquipmentStatusHistory,
    EquipmentType,
    EquipmentModel,
    Manufacturer,
    PersonInCharge,
    Warehouse,
    SystemUnit,
    Monitor,
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


@admin.register(SystemUnit)
class SystemUnitAdmin(admin.ModelAdmin):
    list_display = EquipmentAdmin.list_display + ["cpu", "ram", "storage"]
    list_filter = ("status", "warehouse", "person_in_charge")
    search_fields = EquipmentAdmin.search_fields + ["cpu", "ram", "storage"]


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = EquipmentAdmin.list_display + ["resolution", "size"]
    list_filter = ("status", "warehouse", "person_in_charge")
    search_fields = EquipmentAdmin.search_fields + ["resolution", "size"]
