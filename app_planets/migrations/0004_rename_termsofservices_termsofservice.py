# Generated by Django 3.2.18 on 2023-05-24 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_planets', '0003_planet_is_public'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TermsOfServices',
            new_name='TermsOfService',
        ),
    ]
