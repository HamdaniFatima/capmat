# Generated by Django 3.0 on 2020-04-14 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='capteur',
            name='description_projet',
            field=models.TextField(max_length=100000, null=True, verbose_name='Description du capteur '),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='dimensions',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dimensions '),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='nature_evt',
            field=models.CharField(blank=True, max_length=270, null=True, verbose_name='Nature d’événement à détecter '),
        ),
    ]