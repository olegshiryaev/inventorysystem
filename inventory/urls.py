from django.urls import path
from . import views


app_name = "inventory"

urlpatterns = [
    path("", views.equipment_list, name="equipment_list"),
    path("<int:pk>/", views.equipment_detail, name="equipment_detail"),
    path("equipment/add/", views.choose_equipment_type, name="choose_equipment_type"),
    path(
        "equipment/add/<str:type>/",
        views.EquipmentCreateView.as_view(),
        name="equipment_add",
    ),
    path(
        "equipment/edit/<int:pk>/",
        views.EquipmentUpdateView.as_view(),
        name="equipment_edit",
    ),
    path(
        "equipment/delete/<int:pk>/",
        views.EquipmentDeleteView.as_view(),
        name="equipment_delete",
    ),
    # path("create/", views.equipment_create, name="equipment_create"),
    # path("create/systemunit", views.systemunit_create, name="systemunit_create"),
    # path("create/monitor", views.monitor_create, name="monitor_create"),
    # path(
    #     "equipment/create_generic/",
    #     views.equipment_create_generic,
    #     name="equipment_create_generic",
    # ),
    # path("<int:pk>/edit/", views.equipment_edit, name="equipment_edit"),
    # path("<int:pk>/delete/", views.equipment_delete, name="equipment_delete"),
    path("scan/", views.scan_barcode, name="scan_barcode"),
    path("search/", views.search_equipment, name="search_equipment"),
    path("equipment_model/", views.equipment_model_list, name="equipment_model_list"),
    path(
        "equipment_model/<int:pk>/",
        views.equipment_model_detail,
        name="equipment_model_detail",
    ),
    path("equipment_model/new/", views.equipment_model_new, name="equipment_model_new"),
    path(
        "equipment_model/<int:pk>/edit/",
        views.equipment_model_edit,
        name="equipment_model_edit",
    ),
    path(
        "add_person_in_charge/", views.add_person_in_charge, name="add_person_in_charge"
    ),
    path("add_warehouse/", views.add_warehouse, name="add_warehouse"),
    path(
        "consumable_usage/", views.consumable_usage_list, name="consumable_usage_list"
    ),
    path(
        "consumable_usage/add/",
        views.consumable_usage_create,
        name="consumable_usage_create",
    ),
]
