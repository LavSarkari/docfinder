# Generated by Django 5.0.2 on 2025-04-06 12:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='doctordocument',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='doctors.doctor'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='specializations',
            field=models.ManyToManyField(to='doctors.specialization'),
        ),
        migrations.AddIndex(
            model_name='doctor',
            index=models.Index(fields=['clinic_city', 'clinic_state'], name='doctors_doc_clinic__268be5_idx'),
        ),
        migrations.AddIndex(
            model_name='doctor',
            index=models.Index(fields=['verified'], name='doctors_doc_verifie_bd67df_idx'),
        ),
    ]
