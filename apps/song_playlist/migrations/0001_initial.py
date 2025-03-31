# Generated by Django 5.1.7 on 2025-03-31 05:08

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('playlists', '0001_initial'),
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongPlaylist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song_playlists', to='playlists.playlist')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song_playlists', to='songs.song')),
            ],
        ),
    ]
