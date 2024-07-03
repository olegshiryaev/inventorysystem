from datetime import timezone
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

from django.conf import settings


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
        return f"{self.manufacturer.name} {self.model}"

    class Meta:
        verbose_name = "Модель оборудования"
        verbose_name_plural = "Модели оборудования"


class Workstation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    location = models.CharField(max_length=100, verbose_name="Рабочее место")

    def __str__(self):
        return f"{self.user}"
    
    def get_user_full_name(self):
        return f"{self.user.last_name} {self.user.first_name} {self.user.middle_name or ''}".strip()

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
    person_in_charge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_mol': True}, related_name="assigned_equipment", verbose_name="МОЛ")
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Склад"
    )
    workstation = models.ForeignKey(
        Workstation,
        on_delete=models.CASCADE,
        related_name='equipment',
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

    def __str__(self):
        return f"{self.model} ({self.serial_number})"


class Component(models.Model):
    COMPONENT_TYPE_CHOICES = [
        ('cpu', 'Процессор'),
        ('ram', 'Оперативная память'),
        ('storage', 'Накопитель'),
        ('gpu', 'Видеокарта'),
        ('motherboard', 'Материнская плата'),
        ('psu', 'Блок питания'),
        ('cooling', 'Cooling System'),
    ]

    type = models.CharField(
        max_length=50, choices=COMPONENT_TYPE_CHOICES, verbose_name="Тип компонента"
    )
    manufacturer = models.CharField(max_length=100, verbose_name="Производитель")
    model_name = models.CharField(max_length=100, verbose_name="Модель")
    purchase_date = models.DateField(null=True, blank=True, verbose_name="Дата приобретения")
    warranty_expiry_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания гарантии")
    status = models.CharField(max_length=20, choices=Equipment.STATUS_CHOICES, default="working", verbose_name="Состояние")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Компонент"
        verbose_name_plural = "Компоненты"

    def __str__(self):
        return f"{self.get_type_display()}: {self.manufacturer} {self.model_name}"

    def is_under_warranty(self):
        if self.warranty_expiry_date:
            return self.warranty_expiry_date >= timezone.now().date()
        return False
    

class CPU(Component):
    frequency = models.FloatField(verbose_name="Частота (ГГц)")
    cores = models.PositiveIntegerField(verbose_name="Количество ядер")
    threads = models.PositiveIntegerField(verbose_name="Количество потоков")

    class Meta:
        verbose_name = "Процессор"
        verbose_name_plural = "Процессоры"

    def __str__(self):
        return f"{self.manufacturer} {self.model_name} ({self.frequency} ГГц, {self.cores} ядер, {self.threads} потоков)"
    

class RAM(Component):
    size = models.PositiveIntegerField(verbose_name="Объем (ГБ)")
    speed = models.PositiveIntegerField(verbose_name="Скорость (МГц)")

    class Meta:
        verbose_name = "Оперативная память"
        verbose_name_plural = "Оперативная память"

    def __str__(self):
        return f"Оперативная память: {self.manufacturer} {self.model_name} ({self.size} ГБ, {self.speed} МГц)"


class Storage(Component):
    size = models.PositiveIntegerField(verbose_name="Объем (ГБ)")
    storage_type = models.CharField(max_length=50, choices=[('hdd', 'HDD'), ('ssd', 'SSD')], verbose_name="Тип накопителя")

    class Meta:
        verbose_name = "Накопитель"
        verbose_name_plural = "Накопители"

    def __str__(self):
        return f"Накопитель: {self.manufacturer} {self.model_name} ({self.size} ГБ, {self.storage_type})"


class SystemUnit(Equipment):
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Процессор")
    ram = models.ManyToManyField('RAM', blank=True, verbose_name="Оперативная память")
    storage = models.ManyToManyField('Storage', blank=True, verbose_name="Накопитель")
    os = models.CharField(max_length=100, null=True, blank=True, verbose_name="Операционная система")

    class Meta:
        verbose_name = "Системный блок"
        verbose_name_plural = "Системные блоки"

    def __str__(self):
        return f"Системный блок: {self.model} (CPU: {self.cpu}, RAM: {self.get_ram_total()}GB, Storage: {self.get_storage_total()}GB)"

    def get_ram_total(self):
        return sum(ram.size for ram in self.ram.all())

    def get_storage_total(self):
        return sum(storage.size for storage in self.storage.all())

    def is_under_warranty(self):
        if self.warranty_expiry_date:
            return self.warranty_expiry_date >= timezone.now().date()
        return False


class Monitor(Equipment):
    resolution = models.CharField(max_length=100, null=True, blank=True, verbose_name="Разрешение")
    size = models.PositiveIntegerField(null=True, blank=True, verbose_name="Диагональ (дюймы)")

    def __str__(self):
        return f"{self.model}"

    class Meta:
        verbose_name = "Монитор"
        verbose_name_plural = "Мониторы"


class Printer(Equipment):
    type_choices = [
        ('laser', 'Лазерный'),
        ('inkjet', 'Струйный'),
        ('dot_matrix', 'Матричный'),
    ]
    
    printer_type = models.CharField(
        max_length=20,
        choices=type_choices,
        default='laser',
        verbose_name="Тип принтера"
    )
    color = models.BooleanField(default=False, verbose_name="Цветная печать")
    duplex = models.BooleanField(default=False, verbose_name="Двусторонняя печать")
    network = models.BooleanField(default=False, verbose_name="Сетевой принтер")

    def __str__(self):
        return f"{self.model}"

    class Meta:
        verbose_name = "Принтер"
        verbose_name_plural = "Принтеры"


class MFP(Equipment):
    type_choices = [
        ('laser', 'Лазерный'),
        ('inkjet', 'Струйный'),
    ]
    
    mfp_type = models.CharField(
        max_length=20,
        choices=type_choices,
        default='laser',
        verbose_name="Тип МФУ"
    )
    color = models.BooleanField(default=False, verbose_name="Цветная печать")
    duplex = models.BooleanField(default=False, verbose_name="Двусторонняя печать")
    network = models.BooleanField(default=False, verbose_name="Сетевой принтер")
    scanner = models.BooleanField(default=True, verbose_name="Сканер")
    copier = models.BooleanField(default=True, verbose_name="Копир")
    fax = models.BooleanField(default=False, verbose_name="Факс")

    def __str__(self):
        return f"{self.model}"

    class Meta:
        verbose_name = "МФУ"
        verbose_name_plural = "МФУ"


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


class Consumable(models.Model):
    CONSUMABLE_TYPE_CHOICES = [
        ('toner', 'Картридж'),
        ('ink', 'Чернила'),
        ('drum', 'Фотобарабан'),
        ('other', 'Другое'),
    ]

    COLOR_CHOICES = [
        ('black', 'Черный'),
        ('cyan', 'Голубой'),
        ('magenta', 'Пурпурный'),
        ('yellow', 'Желтый'),
        ('other', 'Другой'),
    ]

    consumable_type = models.CharField(
        max_length=20,
        choices=CONSUMABLE_TYPE_CHOICES,
        verbose_name="Тип расходного материала"
    )
    model = models.CharField(max_length=100, verbose_name="Модель")
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    nomenclature_number = models.CharField(
        max_length=100, blank=True, verbose_name="Номенклатурный номер"
    )
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        blank=True,
        null=True,
        verbose_name="Цвет"
    )

    def __str__(self):
        return f"{self.get_consumable_type_display()} {self.model} {self.get_color_display()}"

    class Meta:
        verbose_name = "Расходный материал"
        verbose_name_plural = "Расходные материалы"


class ConsumableStock(models.Model):
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE, verbose_name="Расходный материал")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")

    def __str__(self):
        return f"{self.consumable.name} на складе {self.warehouse.name}"

    class Meta:
        verbose_name = "Запас расходного материала"
        verbose_name_plural = "Запасы расходных материалов"


class ConsumableUsage(models.Model):
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE, verbose_name="Расходный материал")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Оборудование")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад")
    installation_date = models.DateField(verbose_name="Дата установки")
    installed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Установил")

    def __str__(self):
        return f"{self.consumable} для {self.equipment.model} со склада {self.warehouse.name}"

    def save(self, *args, **kwargs):
        # Вычитаем один из склада
        stock, created = ConsumableStock.objects.get_or_create(consumable=self.consumable, warehouse=self.warehouse)
        if stock.quantity > 0:
            stock.quantity -= 1
            stock.save()
        else:
            raise ValueError("Нет достаточного количества расходных материалов на складе")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Использование расходного материала"
        verbose_name_plural = "Использование расходных материалов"
