from django import forms
from .models import (
    Equipment,
    EquipmentModel,
    Monitor,
    PersonInCharge,
    SystemUnit,
    Warehouse,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class EquipmentModelForm(forms.ModelForm):
    class Meta:
        model = EquipmentModel
        fields = ["manufacturer", "model", "type", "nomenclature_number"]


class DateInput(forms.DateInput):
    input_type = "text"


class SystemUnitForm(forms.ModelForm):
    class Meta:
        model = SystemUnit
        fields = [
            "model",
            "serial_number",
            "inventory_number",
            "person_in_charge",
            "warehouse",
            "purchase_date",
            "warranty_expiry_date",
            "status",
            "cpu",
            "ram",
            "storage",
        ]
        widgets = {
            "purchase_date": DateInput(attrs={"class": "datepicker"}),
            "warranty_expiry_date": DateInput(attrs={"class": "datepicker"}),
        }

    def __init__(self, *args, **kwargs):
        super(SystemUnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Сохранить"))


class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = [
            "model",
            "serial_number",
            "inventory_number",
            "person_in_charge",
            "warehouse",
            "purchase_date",
            "warranty_expiry_date",
            "status",
            "resolution",
            "size",
        ]
        widgets = {
            "purchase_date": DateInput(attrs={"class": "datepicker"}),
            "warranty_expiry_date": DateInput(attrs={"class": "datepicker"}),
        }

    def __init__(self, *args, **kwargs):
        super(MonitorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Сохранить"))


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            "model",
            "serial_number",
            "inventory_number",
            "person_in_charge",
            "warehouse",
            "purchase_date",
            "warranty_expiry_date",
            "status",
        ]
        widgets = {
            "purchase_date": DateInput(attrs={"class": "datepicker"}),
            "warranty_expiry_date": DateInput(attrs={"class": "datepicker"}),
        }

    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Сохранить"))


class PersonInChargeForm(forms.ModelForm):
    class Meta:
        model = PersonInCharge
        fields = ["name"]


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "location"]
