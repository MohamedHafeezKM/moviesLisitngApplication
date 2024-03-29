# Generated by Django 5.0.1 on 2024-01-21 14:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('movie', models.ManyToManyField(related_name='favorite_movies', to='mainapp.movie')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favroites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
