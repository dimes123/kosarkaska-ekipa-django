from django.shortcuts import render, get_object_or_404, redirect
from miami.models import *
from django.db.models import Avg, Max
from django import forms
from django.http import HttpResponseRedirect
from .forms import PovpForm, DatumForm, najboljsiIgralecForm, IgralecForm
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
    ekipa = get_object_or_404(Ekipa, kratica='MIA')
    seznam_igralcev = Igralec.objects.all().order_by('stevilka')

    if request.POST:
        zacetek = request.POST.get('zacetni_datum')
        konec = request.POST.get('koncni_datum')
        print(zacetek, konec)
        tekme = Tekma.objects.filter(datum__range=[zacetek, konec])
        return render(request, 'tekme_med_dvema.html', {
                      'zacetek': zacetek,
                      'konec': konec,
                      'form': DatumForm(),
                      'tekme': tekme  
        })
    else:
        return render(request, 'ekipa.html', {
                        'podatki_o_ekipi': ekipa,
                        'seznam_igralcev': seznam_igralcev,
                        'form': DatumForm(),
        })

def tekme(request, zacetek, konec):
    return render(request, 'tekme_med_dvema.html', {
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
    maximum = igralec.maximum()
    average = igralec.povprecje()
    return render(request, 'povpigralec.html', {
                    'igralec': igralec,
                    'max': maximum,
                    'avg': average,
    })

def najboljsi(request):
    ekipa = request.GET.get('ekipa')
    if ekipa is None:
        return render(request,'najboljsi_form.html',{
            'form': najboljsiIgralecForm(),
        })
    else:
        nasprotnik = list(Ekipa.objects.filter(id = ekipa))
        datumi = Tekma.objects.filter(nasprotnik = ekipa)
        return render(request, 'najboljsi_rezultat.html',{
            'nasprotnik': nasprotnik[0].ime,
            'datumi':datumi,
        })

def najboljsiNaDatum(request, datum):
    tekma = Tekma.objects.get(datum=datum)

    igralci = [('Največ točk: ', tekma.najboljsi_igralec('tocke')),
                        ('Največ skokov: ', tekma.najboljsi_igralec('skoki')),
                        ('Največ podaj: ', tekma.najboljsi_igralec('podaje')),
                        ('Največ ukradenih:', tekma.najboljsi_igralec('ukradene'))]
    return render(request, 'najboljsi_na_datum.html',{
                            'dosezki': igralci,
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
