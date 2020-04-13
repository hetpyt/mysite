from django.db import models
# Create your models here.
# !!!есть картриджи, которые можно изпользовать на разных устройствах одного производителя

class DeviceModel(models.Model):
    vendor_name = models.CharField('Производитель', max_length = 50, blank = False, unique = False)
    model_name = models.CharField('Модель', max_length = 50, blank = False, unique = False)
    
    def __str__(self):
        return f"{self.vendor_name} {self.model_name}"
    
class CartridgeModel(models.Model):
    vendor_name = models.CharField('Производитель', max_length = 50, blank = False, unique = False)
    model_name = models.CharField('Модель', max_length = 50, blank = False, unique = False)
    
    def __str__(self):
        return f"{self.vendor_name} {self.model_name}"
        
class Device(models.Model):
    device_model = models.ForeignKey(DeviceModel, on_delete = models.CASCADE, verbose_name = 'Модель устройства')
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
    #
    device_name = models.CharField('Имя устройства', max_length = 100, blank = True, unique = False)
    #
    production_date = models.DateField('Дата изготовления', null = True, blank = True)
    start_date = models.DateField('Дата начала эксплуатации', null = True, blank = True)

    def __str__(self):
        if self.device_name:
            return f"{self.device_model} ({self.device_name})"
        else:
            return f"{self.device_model}"

class Cartridge(models.Model):
    cartridge_model = models.ForeignKey(CartridgeModel, on_delete = models.CASCADE, verbose_name = 'Модель картриджа')
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
    #
    start_date = models.DateField('Дата начала эксплуатации', null = True, blank = True)

    def __str__(self):
        return f"{self.cartridge_model} [{self.serial_number}]"

class Service(models.Model):
    service_name = models.CharField('Наименование услуги', max_length = 100, blank = False, unique = True)
    default_price = models.DecimalField('Цена по умолчанию', max_digits = 10, decimal_places = 2, null = False, blank = True)
    
    def __str__(self):
        return self.service_name
    
class ProvidedServices(models.Model):
    service_date = models.DateField('Дата услуги', null = False, blank = False)
    cartridge = models.ForeignKey(Cartridge, on_delete = models.CASCADE, verbose_name = 'Картридж', null = False, blank = False)
    servise = models.ForeignKey(Service, on_delete = models.CASCADE, verbose_name = 'Услуга', null = False, blank = False)
    service_price = models.DecimalField('Цена', max_digits = 10, decimal_places = 2, null = False, blank = True)
    invoice_num = models.CharField('Номер счета', max_length = 15, blank = True)
    invoice_date = models.DateField('Дата счета', null = True, blank = True)
    
    def __str__(self):
        return f"{self.service_date} {self.service} {self.cartridge}"
    