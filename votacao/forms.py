from django.forms import ModelForm
from .models import Chapa


class ChapaForm(ModelForm):
    class Meta:
        model = Chapa
        fields = 'nome_chapa', 'nome_candidato', 'nome_vice', 'numero', 'profile'
