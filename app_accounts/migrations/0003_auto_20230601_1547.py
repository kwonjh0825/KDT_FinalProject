# Generated by Django 3.2.18 on 2023-06-01 15:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountbyplanet',
            old_name='backgounrd_image',
            new_name='background_image',
        ),
        migrations.AddField(
            model_name='accountbyplanet',
            name='admin_level',
            field=models.IntegerField(choices=[(1, 'user'), (2, 'staff'), (3, 'admin')], default=1),
        ),
        migrations.AddField(
            model_name='accountbyplanet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountbyplanet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]