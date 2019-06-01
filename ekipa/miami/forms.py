from django import forms
from miami.models import *

class PovpForm(forms.Form):
    def choices():
        igralci = Igralec.objects.all().order_by('stevilka')
        return [(igralec.id, igralec.ime) for igralec in igralci]
    igralec = forms.ChoiceField(choices=choices, widget=forms.Select(), required=False)

class DatumForm(forms.Form):
    zacetni_datum = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': '2017-10-18',
            'max': '2018-04-11',
        })
    )
    koncni_datum = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': '2017-10-18',
            'max': '2018-04-11',
        })
    )

class najboljsiIgralecForm(forms.Form):
    def choices():
        ekipe = Ekipa.objects.all()
        return [(ekipa.id, ekipa.ime) for ekipa in ekipe]
    ekipa = forms.ChoiceField(choices=choices, widget=forms.Select(), required=False)

class IgralecForm(forms.ModelForm):
    class Meta:
        model = Igralec
        fields = ['stevilka', 'ime', 'pozicija', 'teza', 'visina', 'leto_rojstva', 'slika', 'od', 'do']
        widgets = {
            'od': forms.DateInput(attrs={'type': 'date'}),
            'do': forms.DateInput(attrs={'type': 'date'})
        }