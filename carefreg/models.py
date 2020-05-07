from django.db import models
from django.utils import timezone
# !!!есть картриджи, которые можно изпользовать на разных устройствах одного производителя

class AbstractDeviceModel(models.Model):
    """ Абстрактная модель устройства. Содержит общие для всех устройств атрибуты (наименование производителя,
    наименование модели, etc)"""
    vendor_name = models.CharField('Производитель', max_length = 50, blank = False, unique = False)
    model_name = models.CharField('Модель', max_length = 50, blank = False, unique = False)

    def __str__(self):
        return f"{self.vendor_name} {self.model_name}"

    class Meta:
        abstract = True

class AbstractRelationship(models.Model):
    """ абстрактная модель связывающей таблицы """
    rel_date = models.DateField('Дата', db_index = True, null = False, blank = False)
    comment = models.CharField('Комментарий', max_length = 150, blank = True)
    
    class Meta:
        abstract = True
        
class DeviceModel(AbstractDeviceModel):
    """ Модели устройств """
    class Meta:
        verbose_name = 'Модель устройства'
        verbose_name_plural = 'Модели устройств'
    
class CartridgeModel(AbstractDeviceModel):
    """ Модели картриджей """
    class Meta:
        verbose_name = 'Модель картриджа'
        verbose_name_plural = 'Модели картриджей'
    
class Department(models.Model):
    """ Отделы """
    department_name = models.CharField('Наименование отдела', max_length = 50, blank = False, unique = False)
    abbreviated_name = models.CharField('Аббревиатура', max_length = 3, blank = False, unique = True)

    def __str__(self):
        return f"{self.department_name} ({self.abbreviated_name})"
        
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        
class Device(models.Model):
    """ Устройства (принтеры, МФУ, etc) """
    device_model = models.ForeignKey(DeviceModel, on_delete = models.CASCADE, verbose_name = 'Модель устройства')
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
    #
    device_name = models.CharField('Описание устройства', max_length = 100, blank = True, unique = False)
    #
    production_date = models.DateField('Дата изготовления', null = True, blank = True)
    start_date = models.DateField('Дата начала эксплуатации', null = True, blank = True)

    department = models.ManyToManyField(Department, related_name='devices', through='RelDeviceDepartment', through_fields=('device', 'owner_dept'))

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
    
    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'
    
    
class Cartridge(models.Model):
    """ Картриджи """
    cartridge_model = models.ForeignKey(CartridgeModel, on_delete = models.CASCADE, verbose_name = 'Модель картриджа')
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
    #
    start_date = models.DateField('Дата начала эксплуатации', null = True, blank = True)
    device = models.ManyToManyField(Device, related_name='cartridges', through='RelCartridgeDevice', through_fields=('cartridge', 'owner_device'))

    def __str__(self):
        return f"{self.cartridge_model} [{self.serial_number}]"

    def current_department(self):
        if not hasattr(self, '_current_device'):
            self._current_device = self.current_device()
        if not self._current_device:
            return None
        return Department.objects.filter(reldevicedepartment__device = self._current_device, reldevicedepartment__rel_date__lte = timezone.now()).order_by('-reldevicedepartment__rel_date').first()
        
    def current_device(self):
        self._current_device = self.device.filter(relcartridgedevice__rel_date__lte = timezone.now()).order_by('-relcartridgedevice__rel_date').first()
        return self._current_device
    
    current_department.short_description = 'Текущий отдел'
    current_device.short_description = 'Текущее устройство'
    
    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджи'

class Service(models.Model):
    """ Услуги """
    service_name = models.CharField('Наименование услуги', max_length = 100, blank = False, unique = True)
    default_price = models.DecimalField('Цена по умолчанию', max_digits = 10, decimal_places = 2, null = False, blank = True)
    
    def __str__(self):
        return self.service_name
        
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        
class RelCartridgeDevice(AbstractRelationship):
    """ Связи между картриджами и устройствами, в которых они используются, во времени """
    owner_device = models.ForeignKey(Device, on_delete = models.CASCADE, verbose_name = 'Устройство', null = False, blank = False)
    cartridge = models.ForeignKey(Cartridge, on_delete = models.CASCADE, verbose_name = 'Картридж', null = False, blank = False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['rel_date', 'cartridge'], name = 'rel_cartridge_device__unique_date_cartridge'),
            models.UniqueConstraint(fields = ['rel_date', 'cartridge', 'owner_device'], name = 'rel_cartridge_device__unique_date_cartridge_owner_device'),
        ]
        ordering = ('-rel_date',)
        verbose_name = 'Принадлежность картриджа устройству'
        verbose_name_plural = 'Принадлежности картриджей устройствам'

class RelDeviceDepartment(AbstractRelationship):
    """ Связи между устройствами и отделами, в которых они используются, во времени """
    owner_dept = models.ForeignKey(Department, on_delete = models.CASCADE, verbose_name = 'Отдел', null = False, blank = False)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, verbose_name = 'Устройство', null = False, blank = False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['rel_date', 'device'], name = 'rel_device_department__unique_date_device'),
            models.UniqueConstraint(fields = ['rel_date', 'device', 'owner_dept'], name = 'rel_device_department__unique_date_device_owner_dept'),
        ]
        ordering = ('-rel_date',)
        verbose_name = 'Принадлежность устройства отделу'
        verbose_name_plural = 'Принадлежности устройств отделам'
        
class ProvidedServices(models.Model):
    """ Оказанные услуги """
    service_date = models.DateField('Дата услуги', null = False, blank = False)
    cartridge = models.ForeignKey(Cartridge, on_delete = models.CASCADE, verbose_name = 'Картридж', null = False, blank = False)
    service = models.ForeignKey(Service, on_delete = models.CASCADE, verbose_name = 'Услуга', null = False, blank = False)
    service_price = models.DecimalField('Цена', max_digits = 10, decimal_places = 2, null = True, blank = True)
    invoice_num = models.CharField('Номер счета', max_length = 15, blank = True)
    invoice_date = models.DateField('Дата счета', null = True, blank = True)
    
    def __str__(self):
        return f"{self.service_date} {self.service} {self.cartridge}"
        
    class Meta:
        ordering = ('-service_date',)
        verbose_name = 'Предоставленные услуги'
        verbose_name_plural = 'Предоставленная услуга'
        
__all__ = ['DeviceModel', 'CartridgeModel', 'Department', 'Device', 'Cartridge', 'Service',
    'RelCartridgeDevice', 'RelDeviceDepartment', 'ProvidedServices']