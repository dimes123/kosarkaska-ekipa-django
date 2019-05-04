from django.shortcuts import render, get_object_or_404
from miami.models import *
from django.db.models import Avg, Max

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
    igralci = Igralec.objects.all()
    print(igralci)
    return render(request,'povprecja.html', {
                    'vsi_igralci': igralci
    })

def povpigralec(request, id):
    igralec = get_object_or_404(Igralec, pk=id)
    maximum = igralec.statistika_igralec.all().aggregate(Max('skoki'), Max('podaje'), Max('ukradene'), Max('tocke'))
    average = igralec.statistika_igralec.all().aggregate(Avg('skoki'),Avg('podaje'), Avg('ukradene'), Avg('tocke'))
    print(average)
    return render(request, 'povpigralec.html', {
                    'igralec': igralec,
                    'max': maximum,
                    'avg': average,
    })