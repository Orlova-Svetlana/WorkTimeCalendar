# Generated by Django 4.0.6 on 2022-07-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0016_alter_locationworktime_finish_break_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationworktime',
            name='finish_break_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='locationworktime',
            name='start_break_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]