# Generated by Django 4.0.6 on 2022-07-25 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0029_alter_appointment2_appointment_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]
