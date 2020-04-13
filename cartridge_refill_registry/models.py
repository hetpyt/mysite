from django.db import models

# Create your models here.
# !!!есть картриджи, которые можно изпользовать на разных устройствах одного производителя

class DeviceModel(models.Model):
    vendor_name = models.CharField('Производитель', max_length = 100, blank = False, unique = False)
    model_name = models.CharField('Модель', max_length = 100, blank = False, unique = False)

class Device(models.Model):
    device_model = models.ForeignKey(DeviceModel, on_delete = models.SET_NULL, verbose_name = 'Модель устройства')
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
    #
    production_date = models.DateField('Дата изготовления')
    start_date = models.DateField('Дата начала эксплуатации')

class Cartridge(models.Model):
    device_model = models.ForeignKey(DeviceModel, on_delete = models.SET_NULL, verbose_name = 'Модель устройства')
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
