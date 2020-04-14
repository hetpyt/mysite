from django.contrib import admin
from .models import DeviceModel, CartridgeModel, Device, Cartridge, Service, ProvidedServices
# Register your models here.

class ProvidedServicesAdmin(admin.ModelAdmin):
    list_display = ('service_date', 'cartridge', 'service', 'service_price', 'invoice_num', 'invoice_date')
    list_filter = ['service_date']
    search_fields = ['servise']


admin.site.register(DeviceModel)
admin.site.register(CartridgeModel)
admin.site.register(Device)
admin.site.register(Cartridge)
admin.site.register(Service)
admin.site.register(ProvidedServices, ProvidedServicesAdmin)
