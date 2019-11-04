from django.shortcuts import render, redirect
from .models import Chapa
import json
# Create your views here.


def secret(request):
    return render(request, 'secret.html')


def zerezima():

    with open('caminhoDoArquivo.json', 'r') as votos_ler:
        votos_dados = json.load(votos_ler)

    for v in votos_dados:
        votos_dados[v] = 0

        with open('caminhoDoArquivo.json', 'w') as votos_att:
            json.dump(votos_dados, votos_att)

    zerezima_txt = open('caminhoDoArquivo.txt', 'w')

    for v in votos_dados:
        zerezima_txt.write(f"{v}: {votos_dados[v]}")
        zerezima_txt.write("\n")


def boletim_urna():
    with open('caminhoDoArquivo.json', 'r') as votos:
        votos_dados = json.load(votos)

    zerezima = open('caminhoDoArquivo.txt', 'w')

    for v in votos_dados:
        zerezima.write(f"{v}: {votos_dados[v]}")
        zerezima.write("\n")


def secret_code(request):
    code = str(request.POST.get("secret-code"))
    if code == "55555":
        zerezima()
        return redirect('home')
    elif code == "00000":
        boletim_urna()
        return redirect('home')
    else:
        return redirect('home')


def voto_branco(request):
    with open('caminhoDoArquivo.json', 'r') as votos_ler:
        votos_dados = json.load(votos_ler)

    for v in votos_dados:

        if v == 'branco':
            votos_dados[v] += 1

            with open('caminhoDoArquivo.json', 'w') as votos_att:
                json.dump(votos_dados, votos_att)

    return render(request, 'fim.html')


def votar(request):

    numero = str(request.POST.get("primeiro_numero"))
    numero += str(request.POST.get("segundo_numero"))
    chapa = Chapa.objects.get(numero=numero)

    chapa_votar = chapa.nome_chapa

    with open('caminhoDoArquivo.json', 'r') as votos_ler:
        votos_dados = json.load(votos_ler)

    for v in votos_dados:

        if v == chapa_votar:
            votos_dados[v] += 1

            with open('caminhoDoArquivo.json', 'w') as votos_att:
                json.dump(votos_dados, votos_att)

    return render(request, 'fim.html')


def mostra_chapa(request):
    numero = str(request.POST.get("primeiro_numero"))
    numero += str(request.POST.get("segundo_numero"))

    if numero:
        try:
            chapa = Chapa.objects.get(numero=numero)
        except Exception as e:
            chapa = Chapa.objects.get(numero="00")
    else:
        chapa = ""

    return render(request, 'votar.html', {'chapa': chapa})


def home(request):
    return render(request, 'index.html')
