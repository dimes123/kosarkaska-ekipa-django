from django import forms
from miami.models import *

class PovpForm(forms.Form):
    def choices():
        igralci = Igralec.objects.all().order_by('stevilka')
        return [(igralec.id, igralec.ime) for igralec in igralci]
    igralec = forms.ChoiceField(choices=choices, widget=forms.Select(), required=False)

class DatumForm(forms.Form):
    zacetni_datum = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    koncni_datum = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
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
            'od': forms.DateInput(attrs={'type': 'date'})
        }