from django.db import models

class EquipmentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class EquipmentModel(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    category = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category.name} {self.manufacturer.name} {self.model}'

class Equipment(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    model = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    warranty_expiry_date = models.DateField()

    def __str__(self):
        return f'{self.model} ({self.serial_number})'
