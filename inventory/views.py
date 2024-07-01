from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipment, EquipmentModel, SystemUnit, Monitor
from .forms import EquipmentForm, EquipmentModelForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def scan_barcode(request):
    return render(request, 'inventory/barcode_scanner.html')

def search_equipment(request):
    serial_number = request.GET.get('serial_number')
    if serial_number:
        try:
            equipment = Equipment.objects.get(serial_number=serial_number)
            return redirect('inventory:equipment_detail', pk=equipment.pk)
        except Equipment.DoesNotExist:
            return render(request, 'inventory/equipment_not_found.html', {'serial_number': serial_number})
    return redirect('inventory:scan_barcode')


@login_required
def equipment_list(request):
    system_units = SystemUnit.objects.all()
    monitors = Monitor.objects.all()
    return render(request, 'inventory/equipment_list.html', {'system_units': system_units, 'monitors': monitors})

@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'inventory/equipment_detail.html', {'equipment': equipment})

@login_required
def equipment_create(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            return redirect('inventory:equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm()
    return render(request, 'inventory/equipment_form.html', {'form': form, 'title': 'Создать оборудование'})

@login_required
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            equipment = form.save()
            return redirect('inventory:equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'inventory/equipment_form.html', {'form': form, 'title': 'Редактировать оборудование'})

@login_required
@require_POST
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    return redirect('inventory:equipment_list')

def equipment_model_list(request):
    models = EquipmentModel.objects.all()
    return render(request, 'inventory/equipment_model_list.html', {'models': models})

def equipment_model_detail(request, pk):
    model = get_object_or_404(EquipmentModel, pk=pk)
    return render(request, 'inventory/equipment_model_detail.html', {'model': model})

def equipment_model_new(request):
    if request.method == "POST":
        form = EquipmentModelForm(request.POST)
        if form.is_valid():
            equipment_model = form.save(commit=False)
            equipment_model.created_by = request.user
            equipment_model.updated_by = request.user
            equipment_model.save()
            return redirect('equipment_model_detail', pk=equipment_model.pk)
    else:
        form = EquipmentModelForm()
    return render(request, 'inventory/equipment_model_edit.html', {'form': form})

def equipment_model_edit(request, pk):
    model = get_object_or_404(EquipmentModel, pk=pk)
    if request.method == "POST":
        form = EquipmentModelForm(request.POST, instance=model)
        if form.is_valid():
            equipment_model = form.save(commit=False)
            equipment_model.updated_by = request.user
            equipment_model.save()
            return redirect('equipment_model_detail', pk=equipment_model.pk)
    else:
        form = EquipmentModelForm(instance=model)
    return render(request, 'inventory/equipment_model_edit.html', {'form': form})
