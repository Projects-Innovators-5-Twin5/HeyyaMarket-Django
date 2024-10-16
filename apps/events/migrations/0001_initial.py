# Generated by Django 5.0.6 on 2024-10-10 12:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('available_slots', models.IntegerField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('finished', 'Finished'), ('cancelled', 'Cancelled')], default='scheduled', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('refused', 'Refused'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
