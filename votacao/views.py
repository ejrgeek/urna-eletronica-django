from django.shortcuts import render, redirect
from .models import Chapa
from datetime import datetime
import json
from os import system as cmd
# Create your views here.


def secret(request):
    return render(request, 'secret.html')


def zerezima():

    with open('/home/pi/Documents/urna-eletronica-django/votacao/votos/votos.json', 'r') as votos_ler:
        votos_dados = json.load(votos_ler)

    for v in votos_dados:
        votos_dados[v] = 0

        with open('/home/pi/Documents/urna-eletronica-django/votacao/votos/votos.json', 'w') as votos_att:
            json.dump(votos_dados, votos_att)

    zerezima_txt = open('/home/pi/Documents/urna-eletronica-django/votacao/votos/zerezima.txt', 'w')
    zerezima_txt.write(" ")
    zerezima_txt.write(" ")
    zerezima_txt.write(" ")
    zerezima_txt.write(" ")
    zerezima_txt.write("ELEIÇÕES DCE - FAFIC 2019\n\n")

    for v in votos_dados:
        zerezima_txt.write(f"{v}: {votos_dados[v]}")
        zerezima_txt.write("\n")
        
    data = datetime.now()
    data = str(data.day) + "/" + str(data.month) + "/" + str(data.year)
    hora = datetime.now()
    hora = str(hora.hour) + ":" + str(hora.minute) + ":" + str(hora.second)
    
    zerezima_txt.write("\nGERADO:")
    zerezima_txt.write("\n")
    zerezima_txt.write(data)
    zerezima_txt.write("\n")
    zerezima_txt.write(hora)
    zerezima_txt.close()
    cmd("lp -d Lotus-LT-668 /home/pi/Documents/urna-eletronica-django/votacao/votos/zerezima.txt")


def boletim_urna():
    with open('/home/pi/Documents/urna-eletronica-django/votacao/votos/votos.json', 'r') as votos:
        votos_dados = json.load(votos)

    zerezima = open('/home/pi/Documents/urna-eletronica-django/votacao/votos/zerezima.txt', 'w')
    zerezima.write("    ELEIÇÕES DCE - FAFIC 2019\n\n") #MAX 28 CHAR

    for v in votos_dados:
        zerezima.write(f"{v}: {votos_dados[v]}")
        zerezima.write("\n")
        
    data = datetime.now()
    data = str(data.day) + "/" + str(data.month) + "/" + str(data.year)
    hora = datetime.now()
    hora = str(hora.hour) + ":" + str(hora.minute) + ":" + str(hora.second)
    
    zerezima.write("\nGERADO:")
    zerezima.write("\n")
    zerezima.write(data)
    zerezima.write("\n")
    zerezima.write(hora)
    zerezima.close()
    cmd("lp -d Lotus-LT-668 /home/pi/Documents/urna-eletronica-django/votacao/votos/zerezima.txt")

def secret_code(request):
    code = str(request.POST.get("secret-code"))
    if code == "0000":
        zerezima()
        return redirect('home')
    elif code == "5555":
        boletim_urna()
        return redirect('home')
    else:
        return redirect('home')


def voto_branco(request):
    with open('/home/pi/Documents/urna-eletronica-django/votacao/votos/votos.json', 'r') as votos_ler:
        votos_dados = json.load(votos_ler)

    for v in votos_dados:

        if v == 'branco':
            votos_dados[v] += 1

            with open('/home/pi/Documents/urna-eletronica-django/votacao/votos/votos.json', 'w') as votos_att:
                json.dump(votos_dados, votos_att)

    return render(request, 'fim.html')


def votar(request):

    numero = str(request.POST.get("primeiro_numero"))
    numero += str(request.POST.get("segundo_numero"))
    if numero == "" or numero == " " or numero is None:
        numero = "00"
    print(numero)
    try:
        chapa = Chapa.objects.get(numero=numero)
    except Exception as e:
        chapa = Chapa.objects.get(numero="00")

    chapa_votar = chapa.nome_chapa

    with open('/home/pi/Documents/urna-eletronica-django/votacao/votos/votos.json', 'r') as votos_ler:
        votos_dados = json.load(votos_ler)

    for v in votos_dados:

        if v == chapa_votar:
            votos_dados[v] += 1

            with open('/home/pi/Documents/urna-eletronica-django/votacao/votos/votos.json', 'w') as votos_att:
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
