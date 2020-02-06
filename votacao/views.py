from django.shortcuts import render, redirect
from .models import Chapa
from datetime import datetime
from .forms import ChapaForm
import json
from os import system as cmd
# Create your views here.


def secret(request):
    return render(request, 'secret.html')


def zerezima():
    zerezima = open('/home/pi/Documents/urna-eletronica-django/votacao/votos/zerezima.txt', 'w')

    zerezima.write("ELEIÇÕES\n\n")  # MAX 28 CHAR

    todas_chapas = Chapa.objects.all()
    for index in todas_chapas:
        index.numero_votos = 0
        index.save()
        zerezima.write(f"{index.nome_chapa}:\t\t{index.numero_votos}")
        zerezima.write("\n")
        
    data = datetime.now()
    data = str(data.day) + "/" + str(data.month) + "/" + str(data.year)
    hora = datetime.now()
    hora = str(hora.hour) + ":" + str(hora.minute) + ":" + str(hora.second)

    zerezima.write("\n---------------")
    zerezima.write("\nGERADO EM:")
    zerezima.write("\n")
    zerezima.write(f'Data:\t{data}')
    zerezima.write("\n")
    zerezima.write(f'Hora:\t{hora}')
    zerezima.close()
    #cmd("lp -d Lotus-LT-668 /home/pi/Documents/urna-eletronica-django/votacao/votos/zerezima.txt")


def boletim_urna():
    zerezima = open('/home/pi/Documents/urna-eletronica-django/votacao/votos/zerezima.txt', 'w')

    boletim.write("ELEIÇÕES\n\n")  # MAX 28 CHAR

    todas_chapas = Chapa.objects.all()
    for index in todas_chapas:
        boletim.write(f"{index.nome_chapa}:\t\t{index.numero_votos}")
        boletim.write("\n")
        
    data = datetime.now()
    data = str(data.day) + "/" + str(data.month) + "/" + str(data.year)
    hora = datetime.now()
    hora = str(hora.hour) + ":" + str(hora.minute) + ":" + str(hora.second)
    
    boletim.write("\n---------------")
    boletim.write("\nGERADO EM:")
    boletim.write("\n")
    boletim.write(f'Data:\t{data}')
    boletim.write("\n")
    boletim.write(f'Hora:\t{hora}')
    boletim.close()

    #cmd("lp -d Lotus-LT-668 /home/pi/Documents/urna-eletronica-django/votacao/votos/zerezima.txt")

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
    try:
        chapa = Chapa.objects.get(numero="BR")
    except Exception as e:
        chapa = Chapa.objects.get(numero="BR")

    chapa.numero_votos += 1
    chapa.save()

    return render(request, 'fim.html')


def votar(request):

    #numero = str(request.POST.get("primeiro_numero"))
    n1 = str(request.POST.get("primeiro_numero"))
    #numero += str(request.POST.get("segundo_numero"))
    n2 = str(request.POST.get("segundo_numero"))

    if n1 == "" or n1 == '' or n1 == " " or n1 is None:
        n1 = "0"

    if n2 == "" or n2 == '' or n2 == " " or n2 is None:
        n2 = "0"

    numero = n1+n2

    if numero == "" or numero == " " or numero is None:
        numero = "00"
    try:
        chapa = Chapa.objects.get(numero=numero)
    except Exception as e:
        chapa = Chapa.objects.get(numero="00")

    chapa.numero_votos += 1
    chapa.save()

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


def cadastrar_chapa(request):
    form = ChapaForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return render(request, 'index.html')
    else:
        print(form)
    return render(request, 'cadastrar_chapa.html', {'form': form})


def home(request):
    return render(request, 'index.html')
