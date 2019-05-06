from django import forms
from miami.models import *

class PovpForm(forms.Form):
    igralci = Igralec.objects.all().order_by('stevilka')
    IGRALCI = []
    for i in range(len(igralci)):
        IGRALCI.append((i,igralci[i].ime))
    igralec = forms.ChoiceField(choices=IGRALCI, widget=forms.Select(), required=False)