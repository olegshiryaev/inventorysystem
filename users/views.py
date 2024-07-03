from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from inventory.models import Equipment, Workstation
from django.contrib.auth.forms import AuthenticationForm


def custom_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('users:user_equipment_list')  # или другая страница после успешного входа
    else:
        form = EmailAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Переход на главную страницу после успешной регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_equipment_list(request):
    user = request.user  # Получаем текущего пользователя

    if user.is_authenticated and hasattr(user, 'workstation'):
        workstation = user.workstation
        equipment_list = Equipment.objects.filter(workstation=workstation)
    else:
        workstation = None
        equipment_list = []

    context = {
        'user': user,
        'workstation': workstation,
        'equipment_list': equipment_list,
    }

    return render(request, 'users/user_equipment_list.html', context)

@login_required
def mol_equipment_view(request):
    # Получаем текущего пользователя (МОЛ)
    mol = request.user
    
    # Получаем оборудование, на котором числится текущий МОЛ
    equipment_list = Equipment.objects.filter(person_in_charge=mol)
    
    context = {
        'mol': mol,
        'equipment_list': equipment_list,
    }
    
    return render(request, 'users/mol_equipment.html', context)