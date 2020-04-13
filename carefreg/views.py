from django.shortcuts import render
from django.views import generic
from .models import ProvidedServices

# Create your views here.
class IndexView(generic.ListView):
    #template_name = 'carefreg/index.html'
    #context_object_name = 'latest_question_list'
    
    def get_queryset(self):
	    return ProvidedServices.objects.order_by('-service_date')
