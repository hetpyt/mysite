from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from .models import ProvidedServices, Service, Device, Cartridge
from .forms import ProvidedServiceForm

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'carefreg/index.html'
    context_object_name = 'object_list'
    extra_context = {'page_title' : "Перечень оказанных услуг",}
    # fields = {} 
    # for field in ProvidedServices._meta.local_fields if not field.name == 'id':
        # fields[field.name] = field.verbose_name
    extra_context['model_fields'] = {field.name : field.verbose_name for field in ProvidedServices._meta.local_fields if not field.name == 'id'}   
    
    def get_queryset(self):
	    return ProvidedServices.objects.order_by('-service_date')

class ServicesListView(generic.ListView):
    template_name = 'carefreg/index.html'
    context_object_name = 'object_list'
    extra_context = {'page_title' : "Перечень услуг",}
    extra_context['model_fields'] = {field.name : field.verbose_name for field in Service._meta.local_fields if not field.name == 'id'}   
    
    def get_queryset(self):
	    return Service.objects.all()

class DevicesListView(generic.ListView):
    template_name = 'carefreg/index.html'
    context_object_name = 'object_list'
    extra_context = {'page_title' : "Перечень устройств",}
    extra_context['model_fields'] = {field.name : field.verbose_name for field in Device._meta.local_fields if not field.name == 'id'}   
    
    def get_queryset(self):
	    return Device.objects.all()

class CartridgesListView(generic.ListView):
    template_name = 'carefreg/index.html'
    context_object_name = 'object_list'
    extra_context = {'page_title' : "Перечень картриджей",}
    extra_context['model_fields'] = {field.name : field.verbose_name for field in Cartridge._meta.local_fields if not field.name == 'id'}   
    
    def get_queryset(self):
	    return Cartridge.objects.all()

def provided_services_detail(request):
    if request.method == "POST":
        form = ProvidedServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('carefreg/')
        else:
            context = {'form' : form}
            context['page_title'] = 'Оказанная услуга'
            return render(request, 'carefreg/form.html', context)
    else:
        form = ProvidedServiceForm()
        context = {'form' : form}
        context['page_title'] = 'Оказанная услуга'
        return render(request, 'carefreg/form.html', context)