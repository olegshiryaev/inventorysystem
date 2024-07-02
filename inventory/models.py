from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название склада")
    location = models.CharField(max_length=100, verbose_name="Адрес склада")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class PersonInCharge(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="ФИО материально-ответственного лица"
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
    type = models.ForeignKey(
        EquipmentType, on_delete=models.CASCADE, verbose_name="Тип оборудования"
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=100, verbose_name="Модель оборудования")
    nomenclature_number = models.CharField(
        max_length=100, blank=True, verbose_name="Номенклатурный номер"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.type.name} {self.manufacturer.name} {self.model}"

    class Meta:
        verbose_name = "Модель оборудования"
        verbose_name_plural = "Модели оборудования"


class Workstation(models.Model):
    user = models.CharField(max_length=100, verbose_name="Имя пользователя")
    location = models.CharField(max_length=100, verbose_name="Местоположение")

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"


class Equipment(models.Model):
    STATUS_CHOICES = [
        ("working", "Рабочее"),
        ("needs_repair", "Требует ремонта"),
        ("in_repair", "Ремонт"),
        ("diagnostics", "На диагностику"),
        ("disposal", "На утилизацию"),
        ("disposed", "Утилизировано"),
    ]
    model = models.ForeignKey(
        EquipmentModel, on_delete=models.CASCADE, verbose_name="Модель оборудования"
    )
    code = models.CharField(max_length=100, verbose_name="Код")
    serial_number = models.CharField(
        max_length=100, unique=True, verbose_name="Серийный номер"
    )
    inventory_number = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Инвентарный номер"
    )
    person_in_charge = models.ForeignKey(
        PersonInCharge, on_delete=models.CASCADE, verbose_name="МОЛ"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Склад"
    )
    workstation = models.ForeignKey(
        Workstation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Рабочее место",
    )
    purchase_date = models.DateField(
        null=True, blank=True, verbose_name="Дата приобретения"
    )
    warranty_expiry_date = models.DateField(
        null=True, blank=True, verbose_name="Дата окончания гарантии"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="working",
        verbose_name="Состояние",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"


class EquipmentStatusHistory(models.Model):
    equipment = models.ForeignKey(
        "Equipment", on_delete=models.CASCADE, verbose_name="Оборудование"
    )
    status = models.CharField(
        max_length=20, choices=Equipment.STATUS_CHOICES, verbose_name="Состояние"
    )
    change_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    comments = models.TextField(blank=True, verbose_name="Комментарии")

    class Meta:
        verbose_name = "История состояния оборудования"
        verbose_name_plural = "История состояний оборудования"


class SystemUnit(Equipment):
    cpu = models.CharField(max_length=100, verbose_name="Процессор")
    ram = models.PositiveIntegerField(verbose_name="Оперативная память (ГБ)")
    storage = models.PositiveIntegerField(verbose_name="Накопитель (ГБ)")

    def __str__(self):
        return f"Системный блок: {self.model}"

    class Meta:
        verbose_name = "Системный блок"
        verbose_name_plural = "Системные блоки"


class Monitor(Equipment):
    resolution = models.CharField(max_length=100, verbose_name="Разрешение")
    size = models.PositiveIntegerField(verbose_name="Диагональ (дюймы)")

    def __str__(self):
        return f"Монитор: {self.model}"

    class Meta:
        verbose_name = "Монитор"
        verbose_name_plural = "Мониторы"


# Сигнал для отслеживания изменения статуса
@receiver(pre_save, sender=Equipment)
def create_status_history(sender, instance, **kwargs):
    if instance.pk:
        previous = Equipment.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            previous_status_display = previous.get_status_display()
            new_status_display = instance.get_status_display()
            EquipmentStatusHistory.objects.create(
                equipment=instance,
                status=instance.status,
                comments=f"Статус изменен с {previous_status_display} на {new_status_display}",
            )


# Подключение сигнала к моделям-наследникам
@receiver(pre_save, sender=SystemUnit)
@receiver(pre_save, sender=Monitor)
def create_status_history_submodels(sender, instance, **kwargs):
    create_status_history(sender, instance, **kwargs)
