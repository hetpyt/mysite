from django.shortcuts import render
from django.views import generic
from .models import ProvidedServices, Service

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'carefreg/index.html'
    context_object_name = 'provided_service_list'
    extra_context = {'page_title' : "Перечень оказанных услуг",}
    fields = {}
    for field in ProvidedServices._meta.local_fields:
        fields[field.name] = field.verbose_name
    extra_context['model_fields'] = fields   
    
    def get_queryset(self):
	    return ProvidedServices.objects.order_by('-service_date')

        

class ServicesListView(generic.ListView):
    template_name = 'carefreg/service_list.html'
    context_object_name = 'service_list'
    extra_context = {'page_title' : "Перечень услуг",}
    
    def get_queryset(self):
	    return Service.objects.all()
