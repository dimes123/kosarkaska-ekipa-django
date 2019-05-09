from django import forms
from miami.models import *

class PovpForm(forms.Form):
    igralci = Igralec.objects.all().order_by('stevilka')
    choices = [(igralec.id, igralec.ime) for igralec in igralci]
    igralec = forms.ChoiceField(choices=choices, widget=forms.Select(), required=False)
