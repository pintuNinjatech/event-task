# Generated by Django 4.0 on 2024-06-25 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCacheTable',
            fields=[
                ('cache_key', models.CharField(max_length=255, primary_key=True)),
                ('value', models.TextField()),
                ('expires', models.DateTimeField(db_index=True)),
            ],
            options={
                'db_table': 'event_cache_table',
            },
        ),
    ]