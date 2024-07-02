from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipment, EquipmentModel, SystemUnit, Monitor
from .forms import (
    EquipmentForm,
    EquipmentModelForm,
    MonitorForm,
    PersonInChargeForm,
    SystemUnitForm,
    WarehouseForm,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect


def scan_barcode(request):
    return render(request, "inventory/barcode_scanner.html")


def search_equipment(request):
    serial_number = request.GET.get("serial_number")
    if serial_number:
        try:
            equipment = Equipment.objects.get(serial_number=serial_number)
            return redirect("inventory:equipment_detail", pk=equipment.pk)
        except Equipment.DoesNotExist:
            return render(
                request,
                "inventory/equipment_not_found.html",
                {"serial_number": serial_number},
            )
    return redirect("inventory:scan_barcode")


@login_required
def equipment_list(request):
    # Получаем параметр type из запроса GET
    type_param = request.GET.get(
        "type", "all"
    )  # По умолчанию отображаем все оборудование

    if type_param == "system_units":
        equipments = SystemUnit.objects.all()
    elif type_param == "monitors":
        equipments = Monitor.objects.all()
    else:
        # Отобразим все оборудование
        system_units = SystemUnit.objects.all()
        monitors = Monitor.objects.all()
        equipments = list(system_units) + list(monitors)

    context = {
        "equipments": equipments,
        "selected_type": type_param,
    }
    return render(request, "inventory/equipment_list.html", context)


@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)

    if isinstance(equipment, SystemUnit):
        template_name = "inventory/systemunit_detail.html"
    elif isinstance(equipment, Monitor):
        template_name = "inventory/monitor_detail.html"
    else:
        template_name = "inventory/equipment_detail.html"

    return render(request, template_name, {"equipment": equipment})


@login_required
def systemunit_detail(request, pk):
    systemunit = get_object_or_404(SystemUnit, pk=pk)
    return render(
        request, "inventory/systemunit_detail.html", {"equipment": systemunit}
    )


@login_required
def monitor_detail(request, pk):
    monitor = get_object_or_404(Monitor, pk=pk)
    return render(request, "inventory/monitor_detail.html", {"equipment": monitor})


@login_required
def equipment_create(request):
    if request.method == "GET" and "equipment_type" in request.GET:
        equipment_type = request.GET["equipment_type"]
        if equipment_type == "system_unit":
            return redirect("inventory:systemunit_create")
        elif equipment_type == "monitor":
            return redirect("inventory:monitor_create")
        else:
            return redirect("inventory:equipment_create_generic")

    return render(request, "inventory/equipment_create.html")


@login_required
def systemunit_create(request):
    if request.method == "POST":
        form = SystemUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:equipment_list")
    else:
        form = SystemUnitForm()
    return render(request, "inventory/systemunit_form.html", {"form": form})


@login_required
def monitor_create(request):
    if request.method == "POST":
        form = MonitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:equipment_list")
    else:
        form = MonitorForm()
    return render(request, "inventory/monitor_form.html", {"form": form})


@login_required
def equipment_create_generic(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:equipment_list")
    else:
        form = EquipmentForm()
    return render(request, "inventory/equipment_form.html", {"form": form})


@login_required
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            equipment = form.save()
            return redirect("inventory:equipment_detail", pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)
    return render(
        request,
        "inventory/equipment_form.html",
        {"form": form, "title": "Редактировать оборудование"},
    )


@login_required
@require_POST
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    return redirect("inventory:equipment_list")


def equipment_model_list(request):
    models = EquipmentModel.objects.all()
    return render(request, "inventory/equipment_model_list.html", {"models": models})


def equipment_model_detail(request, pk):
    model = get_object_or_404(EquipmentModel, pk=pk)
    return render(request, "inventory/equipment_model_detail.html", {"model": model})


def equipment_model_new(request):
    if request.method == "POST":
        form = EquipmentModelForm(request.POST)
        if form.is_valid():
            equipment_model = form.save(commit=False)
            equipment_model.created_by = request.user
            equipment_model.updated_by = request.user
            equipment_model.save()
            return redirect("equipment_model_detail", pk=equipment_model.pk)
    else:
        form = EquipmentModelForm()
    return render(request, "inventory/equipment_model_edit.html", {"form": form})


def equipment_model_edit(request, pk):
    model = get_object_or_404(EquipmentModel, pk=pk)
    if request.method == "POST":
        form = EquipmentModelForm(request.POST, instance=model)
        if form.is_valid():
            equipment_model = form.save(commit=False)
            equipment_model.updated_by = request.user
            equipment_model.save()
            return redirect("equipment_model_detail", pk=equipment_model.pk)
    else:
        form = EquipmentModelForm(instance=model)
    return render(request, "inventory/equipment_model_edit.html", {"form": form})


@csrf_protect
def add_person_in_charge(request):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        form = PersonInChargeForm(request.POST)
        if form.is_valid():
            person = form.save()
            data = {"id": person.id, "name": str(person)}
            return JsonResponse(data)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=403)


@csrf_protect
def add_warehouse(request):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save()
            data = {
                "id": warehouse.id,
                "name": warehouse.name,
                "location": warehouse.location,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=403)
