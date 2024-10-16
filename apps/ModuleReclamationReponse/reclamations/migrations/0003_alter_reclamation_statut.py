# Generated by Django 5.0.6 on 2024-10-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamations', '0002_reclamation_date_creation_reclamation_priorite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamation',
            name='statut',
            field=models.CharField(choices=[('en_attente', 'En attente'), ('resolue', 'Résolue'), ('refusé', 'Refusée')], default='en_attente', max_length=50),
        ),
    ]
