from django.contrib import admin
from .models import *
# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_model', 'device_name', 'serial_number', 'production_date', 'start_date', 'current_department_name')

class CartridgeAdmin(admin.ModelAdmin):
    list_display = ('cartridge_model', 'serial_number', 'start_date', 'current_device', 'current_department', )
    
class ProvidedServicesAdmin(admin.ModelAdmin):
    list_display = ('service_date', 'cartridge', 'service', 'service_price', 'invoice_num', 'invoice_date')
    list_filter = ['service_date']
    search_fields = ['service']

class RelCartridgeDeviceAdmin(admin.ModelAdmin):
    list_display = ('rel_date', 'cartridge', 'owner_device', 'comment')

class RelDeviceDepartmentAdmin(admin.ModelAdmin):
    list_display = ('rel_date', 'device', 'owner_dept', 'comment')
    
admin.site.register(DeviceModel)
admin.site.register(CartridgeModel)
admin.site.register(Department)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Cartridge, CartridgeAdmin)
admin.site.register(Service)
admin.site.register(RelCartridgeDevice, RelCartridgeDeviceAdmin)
admin.site.register(RelDeviceDepartment, RelDeviceDepartmentAdmin)
admin.site.register(ProvidedServices, ProvidedServicesAdmin)
