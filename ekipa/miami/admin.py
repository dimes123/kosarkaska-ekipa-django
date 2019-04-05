from django.contrib import admin
from .models import Ekipa, Igralec,Tekma,Statistika

# Register your models here.
admin.site.register(Ekipa)
admin.site.register(Igralec)
admin.site.register(Tekma)
admin.site.register(Statistika)