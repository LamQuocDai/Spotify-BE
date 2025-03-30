# Generated by Django 5.1.7 on 2025-03-30 14:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_alter_genre_id_alter_song_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='id',
            field=models.UUIDField(default=uuid.UUID('52bd6993-9384-4e41-8ce8-77f061e67a8f'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='song',
            name='id',
            field=models.UUIDField(default=uuid.UUID('fa5f3de8-a783-4eae-a2a6-0cbc6f0f2171'), editable=False, primary_key=True, serialize=False),
        ),
    ]
