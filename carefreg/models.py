from django.db import models
from django.utils import timezone
# !!!есть картриджи, которые можно изпользовать на разных устройствах одного производителя

class AbstractDeviceModel(models.Model):
    vendor_name = models.CharField('Производитель', max_length = 50, blank = False, unique = False)
    model_name = models.CharField('Модель', max_length = 50, blank = False, unique = False)

    def __str__(self):
        return f"{self.vendor_name} {self.model_name}"

    class Meta:
        abstract = True

class AbstractRelationship(models.Model):
    rel_date = models.DateField('Дата', db_index = True, null = False, blank = False)
    comment = models.CharField('Комментарий', max_length = 150, blank = True)
    
    class Meta:
        abstract = True
        
class DeviceModel(AbstractDeviceModel):
    pass
    
class CartridgeModel(AbstractDeviceModel):
    pass
    
class Department(models.Model):
    department_name = models.CharField('Наименование отдела', max_length = 50, blank = False, unique = False)
    abbreviated_name = models.CharField('Аббревиатура', max_length = 3, blank = False, unique = True)

    def __str__(self):
        return f"{self.department_name} ({self.abbreviated_name})"
        
class Device(models.Model):
    device_model = models.ForeignKey(DeviceModel, on_delete = models.CASCADE, verbose_name = 'Модель устройства')
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
    #
    device_name = models.CharField('Описание устройства', max_length = 100, blank = True, unique = False)
    #
    production_date = models.DateField('Дата изготовления', null = True, blank = True)
    start_date = models.DateField('Дата начала эксплуатации', null = True, blank = True)

    def __str__(self):
        if self.device_name:
            return f"{self.device_model} ({self.device_name})"
        else:
            return f"{self.device_model}"

    def current_department_name(self):
        now = timezone.now()
        rel = RelDeviceDepartment.objects.filter(device = self.id, rel_date__lte = now).select_related('owner_dept').order_by('-rel_date')
        if rel.exists():
            return str(rel[0].owner_dept)
        else:
            return ''
            
    current_department_name.short_description = 'Текущий отдел'
    
class Cartridge(models.Model):
    cartridge_model = models.ForeignKey(CartridgeModel, on_delete = models.CASCADE, verbose_name = 'Модель картриджа')
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
    #
    start_date = models.DateField('Дата начала эксплуатации', null = True, blank = True)

    def __str__(self):
        return f"{self.cartridge_model} [{self.serial_number}]"

    def current_department_name(self):
        return ''
        
    def current_device_name(self):
        now = timezone.now()
        rel_dev_qs = RelCartridgeDevice.objects.filter(cartridge = self.id, rel_date__lte = now).select_related('owner_device').order_by('-rel_date')
        if rel_dev_qs.exists():
            
            def get_current_department_name():
                rel_dept_qs = RelDeviceDepartment.objects.filter(device = rel_dev_qs[0].owner_device.id, rel_date__lte = now).select_related('owner_dept').order_by('-rel_date')
                if rel_dept_qs.exists():
                    return str(rel_dept_qs[0].owner_dept)
                else:
                    return ''
            self.current_department_name = get_current_department_name
            
            return str(rel_dev_qs[0].owner_device)
        else:
            return ''
    
    current_department_name.short_description = 'Текущий отдел'
    current_device_name.short_description = 'Текущее устройство'


class Service(models.Model):
    service_name = models.CharField('Наименование услуги', max_length = 100, blank = False, unique = True)
    default_price = models.DecimalField('Цена по умолчанию', max_digits = 10, decimal_places = 2, null = False, blank = True)
    
    def __str__(self):
        return self.service_name

class RelCartridgeDevice(AbstractRelationship):
    """ Связи между картриджами и устройствами, в которых они используются, во времени """
    owner_device = models.ForeignKey(Device, on_delete = models.CASCADE, verbose_name = 'Устройство', null = False, blank = False)
    cartridge = models.ForeignKey(Cartridge, on_delete = models.CASCADE, verbose_name = 'Картридж', null = False, blank = False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['rel_date', 'cartridge'], name = 'rel_cartridge_device__unique_date_cartridge'),
            models.UniqueConstraint(fields = ['rel_date', 'cartridge', 'owner_device'], name = 'rel_cartridge_device__unique_date_cartridge_owner_device'),
        ]
        ordering = ('rel_date',)

class RelDeviceDepartment(AbstractRelationship):
    """ Связи между устройствами и отделами, в которых они используются, во времени """
    owner_dept = models.ForeignKey(Department, on_delete = models.CASCADE, verbose_name = 'Отдел', null = False, blank = False)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, verbose_name = 'Устройство', null = False, blank = False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['rel_date', 'device'], name = 'rel_device_department__unique_date_device'),
            models.UniqueConstraint(fields = ['rel_date', 'device', 'owner_dept'], name = 'rel_device_department__unique_date_device_owner_dept'),
        ]
        ordering = ('rel_date',)
        
class ProvidedServices(models.Model):
    service_date = models.DateField('Дата услуги', null = False, blank = False)
    cartridge = models.ForeignKey(Cartridge, on_delete = models.CASCADE, verbose_name = 'Картридж', null = False, blank = False)
    service = models.ForeignKey(Service, on_delete = models.CASCADE, verbose_name = 'Услуга', null = False, blank = False)
    service_price = models.DecimalField('Цена', max_digits = 10, decimal_places = 2, null = True, blank = True)
    invoice_num = models.CharField('Номер счета', max_length = 15, blank = True)
    invoice_date = models.DateField('Дата счета', null = True, blank = True)
    
    def __str__(self):
        return f"{self.service_date} {self.service} {self.cartridge}"
    
__all__ = ['DeviceModel', 'CartridgeModel', 'Department', 'Device', 'Cartridge', 'Service',
    'RelCartridgeDevice', 'RelDeviceDepartment', 'ProvidedServices']