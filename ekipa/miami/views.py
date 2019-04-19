from django.shortcuts import render, get_object_or_404
from miami.models import *

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
    igralec = get_object_or_404(Igralec)
    return render(request, 'igralec.html', {
        'igralec': igralec,
    })