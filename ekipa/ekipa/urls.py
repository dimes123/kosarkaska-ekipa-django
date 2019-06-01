"""ekipa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from miami import views

urlpatterns = [
    path('', views.index, name='index'),
    path('igralci/', views.igralci, name='igralci'),
    path('igralci/<int:id>/', views.igralec, name='igralec'),
    path('ekipa/', views.ekipa, name='ekipa'),
    path('ekipa/<int:zacetek><int:konec>', views.ekipa, name='ekipa_tekme'),
    path('povprecja/', views.povprecja, name='povprecja'),
    path('povpigralec/<int:id>/', views.povpigralec, name='povpigralec'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dodajanje/', views.dodajanje, name='dodajanje'),
    path('brisanje/<int:id>/', views.brisanje, name='brisanje'),

    path('najboljsi/',views.najboljsi, name='najboljsiIgralec'),
    path('najboljsiNaDatum/<str:datum>', views.najboljsiNaDatum, name='najboljsiNaDatum'),
    path('registracija/', views.registracija, name='registracija'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
