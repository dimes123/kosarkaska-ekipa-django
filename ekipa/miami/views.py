from django.shortcuts import render, get_object_or_404, redirect
from miami.models import *
from django.db.models import Avg, Max
from django import forms
from django.http import HttpResponseRedirect
from .forms import PovpForm

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
    print(seznam_igralcev)
    return render(request, 'ekipa.html', {
                    'podatki_o_ekipi': podatki,
                    'seznam_igralcev': seznam_igralcev,
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
    return render(request, 'povpigralec.html', {
                    'igralec': igralec,
                    'max': maximum,
                    'avg': average,
    })
