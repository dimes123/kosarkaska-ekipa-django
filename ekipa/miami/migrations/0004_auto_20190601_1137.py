# Generated by Django 2.1.5 on 2019-06-01 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miami', '0003_auto_20190530_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='igralec',
            name='ime',
            field=models.CharField(help_text='Ime igralca', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='igralec',
            name='slika',
            field=models.ImageField(blank=True, default='igralci/missing.jpg', null=True, upload_to='igralci/'),
        ),
        migrations.AlterField(
            model_name='igralec',
            name='stevilka',
            field=models.PositiveSmallIntegerField(help_text='Številka dresa igralca', unique=True),
        ),
    ]
