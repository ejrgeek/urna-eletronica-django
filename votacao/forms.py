from django.forms import ModelForm
from .models import Chapa


class ChapaForm(ModelForm):
    class Meta:
        model = Chapa
        fields = '__all__'
