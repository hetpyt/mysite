from django.forms import ModelForm
from .models import ProvidedServices

class ProvidedServiceForm(ModelForm):
    class Meta:
        model = ProvidedServices
        fields = '__all__'