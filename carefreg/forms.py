from django.forms import ModelForm
from .models import ProvidedServices

class ProvidedServiceForm(ModelForm):
    class Meta:
        model = ProvidedServices
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for bfield in self.base_fields:
            self[bfield].field.widget.attrs.update({'class': 'form-control'})
