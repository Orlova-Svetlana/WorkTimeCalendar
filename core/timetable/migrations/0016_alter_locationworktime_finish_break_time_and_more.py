# Generated by Django 4.0.6 on 2022-07-14 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0015_alter_schedule_finish_work_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationworktime',
            name='finish_break_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='locationworktime',
            name='finish_work_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='locationworktime',
            name='start_break_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='locationworktime',
            name='start_work_time',
            field=models.TimeField(),
        ),
    ]
