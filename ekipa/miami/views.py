from django.shortcuts import render, get_object_or_404, redirect
from miami.models import *
from django.db.models import Avg, Max
from django import forms
from django.http import HttpResponseRedirect
from .forms import PovpForm, DateForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def registracija(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registracija.html', {'form': form})

def index(request):
    return render(request, 'index.html', {
        'title': 'Miami Heat igralci',
    })

def igralci(request):
    vsi = Igralec.objects.all().order_by('stevilka')
    return render(request, 'igralci.html', {
        'igralci': vsi,
    })

def igralec(request, id):
    igralec = get_object_or_404(Igralec, pk=id)
    statistika = igralec.statistika_igralec.all()
    return render(request, 'igralec.html', {
        'igralec': igralec,
        'statistika': statistika,
    })

def ekipa(request):
    podatki = get_object_or_404(Ekipa, kratica='MIA')
    seznam_igralcev = Igralec.objects.all().order_by('stevilka')
    zacetek = request.GET.get('zacetniDan')
    konec = request.GET.get('koncniDan')
    print(zacetek,konec)
    print()
    if zacetek is None or konec is None:
        return render(request, 'ekipa.html', {
                        'podatki_o_ekipi': podatki,
                        'seznam_igralcev': seznam_igralcev,
                        'form': DateForm(),
        })
    else:
        return redirect('tekme', zacetek, konec)

def tekme(request, zacetek, konec):
    return render(request, 'tekme.html', {
        'zacetek': zacetek,
        'konec': konec,
        })

def povprecja(request):
    id_igralca = request.GET.get('igralec')
    if id_igralca is None:
        return render(request,'povprecja.html', {
            'form': PovpForm()
        })
    else:
        return redirect('povpigralec', id_igralca)

def povpigralec(request, id):
    igralec = get_object_or_404(Igralec, id=id)
    maximum = igralec.statistika_igralec.all().aggregate(Max('skoki'), Max('podaje'), Max('ukradene'), Max('tocke'))
    average = igralec.statistika_igralec.all().aggregate(Avg('skoki'),Avg('podaje'), Avg('ukradene'), Avg('tocke'))
    print(average)
    return render(request, 'povpigralec.html', {
                    'igralec': igralec,
                    'max': maximum,
                    'avg': average,
    })

