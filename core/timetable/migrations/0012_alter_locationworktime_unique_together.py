# Generated by Django 4.0.6 on 2022-07-13 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0011_alter_locationworktime_finish_break_time_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='locationworktime',
            unique_together={('location', 'day_week')},
        ),
    ]
