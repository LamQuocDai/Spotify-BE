# Generated by Django 5.1.7 on 2025-03-28 05:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singer_name', models.CharField(max_length=100)),
                ('song_name', models.CharField(max_length=100)),
                ('url', models.URLField(max_length=1000)),
                ('image', models.URLField(blank=True, max_length=10000, null=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='songs.genre')),
            ],
        ),
    ]