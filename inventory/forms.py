from django import forms
from .models import Equipment, EquipmentModel

class EquipmentModelForm(forms.ModelForm):
    class Meta:
        model = EquipmentModel
        fields = ['manufacturer', 'model', 'type', 'nomenclature_number']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['model', 'code', 'serial_number', 'inventory_number', 'person_in_charge', 'warehouse', 'purchase_date', 'warranty_expiry_date', 'status']