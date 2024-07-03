from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import (
    MFP,
    ConsumableUsage,
    Equipment,
    EquipmentModel,
    Printer,
    SystemUnit,
    Monitor,
)
from .forms import (
    ConsumableUsageForm,
    EquipmentForm,
    EquipmentModelForm,
    MFPForm,
    MonitorForm,
    PersonInChargeForm,
    PrinterForm,
    SystemUnitForm,
    WarehouseForm,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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
    elif type_param == "printers":
        equipments = Printer.objects.all()
    elif type_param == "mfps":
        equipments = MFP.objects.all()
    else:
        # Отобразим все оборудование
        system_units = SystemUnit.objects.all()
        monitors = Monitor.objects.all()
        printers = Printer.objects.all()
        mfps = MFP.objects.all()
        equipments = list(system_units) + list(monitors) + list(printers) + list(mfps)

    context = {
        "equipments": equipments,
        "selected_type": type_param,
    }
    return render(request, "inventory/equipment_list.html", context)


@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment_type = equipment.get_equipment_type()
    if equipment_type == "systemunit":
        template = "inventory/systemunit_detail.html"
    elif equipment_type == "monitor":
        template = "inventory/monitor_detail.html"
    elif equipment_type == "printer":
        template = "inventory/printer_detail.html"
    elif equipment_type == "mfp":
        template = "inventory/mfp_detail.html"
    else:
        template = "inventory/equipment_detail.html"

    return render(request, template, {"equipment": equipment})


# @login_required
# def equipment_create(request):
#     if request.method == "GET" and "equipment_type" in request.GET:
#         equipment_type = request.GET["equipment_type"]
#         if equipment_type == "system_unit":
#             return redirect("inventory:systemunit_create")
#         elif equipment_type == "monitor":
#             return redirect("inventory:monitor_create")
#         else:
#             return redirect("inventory:equipment_create_generic")

#     return render(request, "inventory/equipment_create.html")


# @login_required
# def systemunit_create(request):
#     if request.method == "POST":
#         form = SystemUnitForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("inventory:equipment_list")
#     else:
#         form = SystemUnitForm()
#     return render(request, "inventory/systemunit_form.html", {"form": form})


# @login_required
# def monitor_create(request):
#     if request.method == "POST":
#         form = MonitorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("inventory:equipment_list")
#     else:
#         form = MonitorForm()
#     return render(request, "inventory/monitor_form.html", {"form": form})


# @login_required
# def equipment_create_generic(request):
#     if request.method == "POST":
#         form = EquipmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("inventory:equipment_list")
#     else:
#         form = EquipmentForm()
#     return render(request, "inventory/equipment_form.html", {"form": form})


# @login_required
# def equipment_edit(request, pk):
#     equipment = get_object_or_404(Equipment, pk=pk)
#     if request.method == "POST":
#         form = EquipmentForm(request.POST, instance=equipment)
#         if form.is_valid():
#             equipment = form.save()
#             return redirect("inventory:equipment_detail", pk=equipment.pk)
#     else:
#         form = EquipmentForm(instance=equipment)
#     return render(
#         request,
#         "inventory/equipment_form.html",
#         {"form": form, "title": "Редактировать оборудование"},
#     )


# @login_required
# @require_POST
# def equipment_delete(request, pk):
#     equipment = get_object_or_404(Equipment, pk=pk)
#     equipment.delete()
#     return redirect("inventory:equipment_list")


def choose_equipment_type(request):
    if request.method == "POST":
        selected_type = request.POST.get("type")
        return redirect(
            reverse("inventory:equipment_add", kwargs={"type": selected_type})
        )

    return render(request, "inventory/choose_equipment_type.html")


class EquipmentCreateView(CreateView):
    template_name = "inventory/equipment_form.html"
    success_url = reverse_lazy("inventory:equipment_list")

    def get_form_class(self):
        equipment_type = self.kwargs.get("type")
        if equipment_type == "systemunit":
            return SystemUnitForm
        elif equipment_type == "monitor":
            return MonitorForm
        elif equipment_type == "printer":
            return PrinterForm
        elif equipment_type == "mfp":
            return MFPForm
        else:
            return EquipmentForm


class EquipmentUpdateView(UpdateView):
    model = Equipment
    template_name = "inventory/equipment_form.html"
    success_url = reverse_lazy("inventory:equipment_list")

    def get_form_class(self):
        if hasattr(self.object, "systemunit"):
            return SystemUnitForm
        elif hasattr(self.object, "monitor"):
            return MonitorForm
        elif hasattr(self.object, "printer"):
            return PrinterForm
        elif hasattr(self.object, "mfp"):
            return MFPForm


class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = "inventory/equipment_confirm_delete.html"
    success_url = reverse_lazy("inventory:equipment_list")

    def get_object(self, queryset=None):
        equipment = super().get_object(queryset)
        if hasattr(equipment, "systemunit"):
            return equipment.systemunit
        elif hasattr(equipment, "monitor"):
            return equipment.monitor
        elif hasattr(equipment, "printer"):
            return equipment.printer
        elif hasattr(equipment, "mfp"):
            return equipment.mfp
        return equipment


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


def consumable_usage_list(request):
    usage_list = ConsumableUsage.objects.all().order_by("-installation_date")
    return render(
        request, "inventory/consumable_usage_list.html", {"usage_list": usage_list}
    )


def consumable_usage_create(request):
    if request.method == "POST":
        form = ConsumableUsageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:consumable_usage_list")
    else:
        form = ConsumableUsageForm()
    return render(request, "inventory/consumable_usage_form.html", {"form": form})
