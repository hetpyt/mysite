from django.db import models

# Create your models here.
class Device(models.Model):
    vendor_name = models.CharField('Производитель', max_length = 100, blank = False, unique = False)
    model_name = models.CharField('Модель', max_length = 100, blank = False, unique = False)
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
    #
    production_date = models.DateField('Дата изготовления')
    start_date = models.DateField('Дата начала эксплуатации')

class Cartridge(models.Model):
    device = models.CharField('Устройство', max_length = 50)
    serial_number = models.CharField('Серийный номер', max_length = 50, blank = False, unique = True)
