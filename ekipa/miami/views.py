from django.shortcuts import render, get_object_or_404, redirect
from miami.models import *
from django.db.models import Avg, Max
from django import forms
from django.http import HttpResponseRedirect
from .forms import PovpForm, DateForm, najboljsiIgralecForm, IgralecForm
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

def brisanje(request, id):
    igralec = get_object_or_404(Igralec, id=id)
    igralec.delete()
    return HttpResponseRedirect('/igralci/')

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

def tekme(request):
    return render(request, 'tekme.html', {
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

def najboljsi(request):
    ekipa = request.GET.get('ekipa')
    prikazi = 1
    if ekipa is None:
        return render(request,'najboljsi.html',{
            'form': najboljsiIgralecForm(),
            'prikazi': prikazi,
        })
    else:
        prikazi = 2
        nasprotnik = list(Ekipa.objects.filter(id = ekipa))
        datumi = Tekma.objects.filter(nasprotnik = ekipa)
        print(type(datumi))
        return render(request, 'najboljsi.html',{
            'prikazi':prikazi,
            'nasprotnik': nasprotnik[0].ime,
            'datumi':datumi,
        })

def najboljsiNaDatum(request, datum):
    id_tekme = list(Tekma.objects.filter(datum = datum))
    id_tekme = id_tekme[0].id
    
    najvec_tock = Statistika.objects.filter(tekma_id = id_tekme).order_by('-tocke').first()
    najvec_podaj = Statistika.objects.filter(tekma_id = id_tekme).order_by('-podaje').first()
    najvec_skoki = Statistika.objects.filter(tekma_id = id_tekme).order_by('-skoki').first()
    najvec_ukradenih = Statistika.objects.filter(tekma_id = id_tekme).order_by('-ukradene').first()
    
    najvec_tock_igralec = Igralec.objects.filter(id = najvec_tock.igralec_id)
    najvec_podaj_igralec = Igralec.objects.filter(id = najvec_podaj.igralec_id)
    najvec_skoki_igralec = Igralec.objects.filter(id = najvec_skoki.igralec_id)
    najvec_ukradenih_igralec = Igralec.objects.filter(id = najvec_ukradenih.igralec_id)

    najboljsi_dosezki = [('Največ točk: ',najvec_tock_igralec[0].ime,najvec_tock.tocke),
                        ('Največ skokov: ',najvec_skoki_igralec[0].ime,najvec_skoki.skoki),
                        ('Največ podaj: ',najvec_podaj_igralec[0].ime,najvec_podaj.podaje),
                        ('Največ ukradenih:',najvec_ukradenih_igralec[0].ime, najvec_ukradenih.ukradene)]
    print(najboljsi_dosezki)
    return render(request, 'najboljsiNaDatum.html',{
                            'dosezki':najboljsi_dosezki,
                            'datum':datum,
    })

def dodajanje(request):
    if request.POST:
        form = IgralecForm(request.POST, request.FILES)
        if form.is_valid():
            igralec = form.save()
            return redirect('igralec', id=igralec.id)
    else:
        form = IgralecForm()
    args = {}
    args.update(request)
    args['form'] = form

    return render(request, 'dodajanje.html', args)
