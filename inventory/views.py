from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipment, EquipmentModel
from .forms import EquipmentForm, EquipmentModelForm

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'inventory/equipment_list.html', {'equipments': equipments})

def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'inventory/equipment_detail.html', {'equipment': equipment})

def equipment_new(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm()
    return render(request, 'inventory/equipment_edit.html', {'form': form})

def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            equipment = form.save()
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'inventory/equipment_edit.html', {'form': form})

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
