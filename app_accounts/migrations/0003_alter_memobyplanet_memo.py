# Generated by Django 3.2.18 on 2023-06-12 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memobyplanet',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
    ]