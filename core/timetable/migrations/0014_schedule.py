# Generated by Django 4.0.6 on 2022-07-13 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0013_delete_appointment_delete_schedule_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_work_time', models.TimeField(blank=True, null=True)),
                ('finish_work_time', models.TimeField(blank=True, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.location')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.worker')),
            ],
        ),
    ]
