from django.forms import ModelForm
from .models import SimInput


# Create Sim Input form
class SimInputForm(ModelForm):
    class Meta:
        model = SimInput
        fields = '__all__'
