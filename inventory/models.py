from django.db import models


class Warehouse(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="Название склада"
    )
    location = models.CharField(
        max_length=100, 
        verbose_name="Адрес склада"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class PersonInCharge(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="ФИО ответственного лица"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Материально-ответственное лицо"
        verbose_name_plural = "Материально-ответственные лица"


class EquipmentType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название типа оборудования")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип оборудования"
        verbose_name_plural = "Типы оборудования"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название производителя")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
    

class EquipmentModel(models.Model):
    type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, verbose_name="Тип оборудования")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    model = models.CharField(max_length=100, verbose_name="Модель оборудования")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f'{self.type.name} {self.manufacturer.name} {self.model}'
    
    class Meta:
        verbose_name = "Модель оборудования"
        verbose_name_plural = "Модели оборудования"


class Equipment(models.Model):
    STATUS_CHOICES = [
        ('working', 'Рабочее'),
        ('needs_repair', 'Требует ремонта'),
        ('in_repair', 'Ремонт'),
        ('diagnostics', 'На диагностику'),
        ('disposal', 'На утилизацию'),
        ('disposed', 'Утилизировано'),
    ]
    model = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE, verbose_name="Модель оборудования")
    code = models.CharField(max_length=100, verbose_name="Код")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Серийный номер")
    inventory_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Инвентарный номер")
    nomenclature_number = models.CharField(max_length=100, verbose_name="Номенклатурный номер")
    person_in_charge = models.ForeignKey(PersonInCharge, on_delete=models.CASCADE, verbose_name="МОЛ")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад")
    purchase_date = models.DateField(verbose_name="Дата приобретения")
    warranty_expiry_date = models.DateField(verbose_name="Дата окончания гарантии")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='working', verbose_name="Состояние")

    def __str__(self):
        return f'{self.model} ({self.serial_number})'
    
    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
