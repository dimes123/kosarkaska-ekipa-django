from django import forms
from miami.models import *

class PovpForm(forms.Form):
    igralci = Igralec.objects.all().order_by('stevilka')
    choices = [(igralec.id, igralec.ime) for igralec in igralci]
    igralec = forms.ChoiceField(choices=choices, widget=forms.Select(), required=False)

class DateForm(forms.Form):
    zacetniDan = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    koncniDan = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )

class najboljsiIgralecForm(forms.Form):
    ekipe = Ekipa.objects.all()
    choices = [(ekipa.id, ekipa.ime) for ekipa in ekipe]
    ekipa = forms.ChoiceField(choices=choices, widget=forms.Select(), required=False)

