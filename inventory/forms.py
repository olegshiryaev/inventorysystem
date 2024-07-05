from django import forms
from .models import (
    MFP,
    ConsumableStock,
    ConsumableUsage,
    Equipment,
    EquipmentModel,
    Monitor,
    PersonInCharge,
    Printer,
    SystemUnit,
    Warehouse,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db import models


class EquipmentModelForm(forms.ModelForm):
    class Meta:
        model = EquipmentModel
        fields = ["manufacturer", "model", "type", "nomenclature_number"]


class DateInput(forms.DateInput):
    input_type = "date"


class SystemUnitForm(forms.ModelForm):
    class Meta:
        model = SystemUnit
        fields = "__all__"
        widgets = {
            "purchase_date": DateInput(format=('%Y-%m-%d'), attrs={"class": "datepicker"}),
            "warranty_expiry_date": DateInput(format=('%Y-%m-%d'), attrs={"class": "datepicker"}),
        }


class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = "__all__"
        widgets = {
            "purchase_date": DateInput(format=('%Y-%m-%d'), attrs={"class": "datepicker"}),
            "warranty_expiry_date": DateInput(format=('%Y-%m-%d'), attrs={"class": "datepicker"}),
        }


class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = "__all__"
        widgets = {
            "purchase_date": DateInput(format=('%Y-%m-%d'), attrs={"class": "datepicker"}),
            "warranty_expiry_date": DateInput(format=('%Y-%m-%d'), attrs={"class": "datepicker"}),
        }


class MFPForm(forms.ModelForm):
    class Meta:
        model = MFP
        fields = "__all__"
        widgets = {
            "purchase_date": DateInput(format=('%Y-%m-%d'), attrs={"class": "datepicker"}),
            "warranty_expiry_date": DateInput(format=('%Y-%m-%d'), attrs={"class": "datepicker"}),
        }

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


class ConsumableUsageForm(forms.ModelForm):
    class Meta:
        model = ConsumableUsage
        fields = [
            "consumable",
            "equipment",
            "warehouse",
            "installation_date",
            "installed_by",
        ]
        widgets = {
            "installation_date": DateInput(attrs={"class": "datepicker"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipment"].queryset = Equipment.objects.filter(
            models.Q(printer__isnull=False) | models.Q(mfp__isnull=False)
        )

    def clean(self):
        cleaned_data = super().clean()
        consumable = cleaned_data.get("consumable")
        warehouse = cleaned_data.get("warehouse")

        if consumable and warehouse:
            stock = ConsumableStock.objects.filter(
                consumable=consumable, warehouse=warehouse
            ).first()
            if not stock or stock.quantity < 1:
                raise forms.ValidationError(
                    "Нет достаточного количества расходных материалов на складе"
                )
        return cleaned_data
