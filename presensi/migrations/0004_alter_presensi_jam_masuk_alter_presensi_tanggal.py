# Generated by Django 5.2.1 on 2025-06-13 10:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presensi', '0003_alter_presensi_jam_masuk_alter_presensi_tanggal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presensi',
            name='jam_masuk',
            field=models.TimeField(default=datetime.time(17, 5, 5, 579102)),
        ),
        migrations.AlterField(
            model_name='presensi',
            name='tanggal',
            field=models.DateField(default=datetime.date(2025, 6, 13)),
        ),
    ]
