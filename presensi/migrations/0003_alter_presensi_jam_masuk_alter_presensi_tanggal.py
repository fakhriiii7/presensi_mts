# Generated by Django 5.2.1 on 2025-05-23 17:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presensi', '0002_presensi_guru_alter_abstractuser_role_kelas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presensi',
            name='jam_masuk',
            field=models.TimeField(default=datetime.time(0, 10, 58, 421157)),
        ),
        migrations.AlterField(
            model_name='presensi',
            name='tanggal',
            field=models.DateField(default=datetime.date(2025, 5, 24)),
        ),
    ]
