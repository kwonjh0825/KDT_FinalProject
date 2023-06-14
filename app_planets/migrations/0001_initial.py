# Generated by Django 3.2.18 on 2023-06-14 16:24

import app_planets.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accountbyplanet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_accounts.accountbyplanet')),
            ],
        ),
        migrations.CreateModel(
            name='Emote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emotion', models.CharField(max_length=10)),
                ('accountbyplanet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_accounts.accountbyplanet')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_planets.comment')),
            ],
        ),
        migrations.CreateModel(
            name='InappropriateWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('Tech', 'Tech'), ('Game', 'Game'), ('Music', 'Music'), ('Sports', 'Sports'), ('Food', 'Food'), ('Hobby', 'Hobby')], max_length=20)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='planets/')),
                ('plan', models.CharField(choices=[('Free', 'Free'), ('Premium', 'Primium')], default='Free', max_length=10)),
                ('is_public', models.CharField(choices=[('Private', 'Private'), ('Public', 'Public')], default='Private', max_length=10)),
                ('need_confirm', models.BooleanField(choices=[(True, 'Approval'), (False, 'Direct')], default=False)),
                ('maximum_capacity', models.DecimalField(decimal_places=0, default=50, max_digits=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('invite_code', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=app_planets.models.Post.upload_to_directory)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accountbyplanet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_accounts.accountbyplanet')),
                ('emotion', models.ManyToManyField(related_name='emotion_post', through='app_planets.Emote', to='app_accounts.Accountbyplanet')),
                ('planet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_planets.planet')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Recomment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accountbyplanet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_accounts.accountbyplanet')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomments', to='app_planets.comment')),
            ],
        ),
        migrations.CreateModel(
            name='VoteTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_planets.post')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_accounts.accountbyplanet')),
                ('votetopic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_planets.votetopic')),
            ],
        ),
        migrations.CreateModel(
            name='TermsOfService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('content', models.CharField(max_length=100)),
                ('Planet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_planets.planet')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_planets.comment')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_planets.post')),
                ('recomment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_planets.recomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='emote',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_planets.post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='emotion',
            field=models.ManyToManyField(related_name='emotion_comment', through='app_planets.Emote', to='app_accounts.Accountbyplanet'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_planets.post'),
        ),
    ]
