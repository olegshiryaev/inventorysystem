from django import forms
from .models import Equipment, EquipmentModel

class EquipmentModelForm(forms.ModelForm):
    class Meta:
        model = EquipmentModel
        fields = ['manufacturer', 'model', 'type']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['serial_number', 'model', 'purchase_date', 'warranty_expiry_date']
