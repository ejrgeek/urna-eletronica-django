from django.db import models
import uuid

# Create your models here.


def get_path_photo_profile(instance, filename):
    return f'chapas/{instance.nome_chapa}@{instance.numero}/foto_candidato/{filename}'


class Chapa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nome_chapa = models.CharField(max_length=50, null=False, blank=False)
    nome_candidato = models.CharField(max_length=50, null=False, blank=False)
    nome_vice = models.CharField(max_length=50, null=False, blank=False)
    numero = models.CharField(max_length=2, null=False, blank=False)
    profile = models.ImageField(upload_to=get_path_photo_profile, null=False, blank=False)
    numero_votos = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.nome_chapa}@{self.numero}"
