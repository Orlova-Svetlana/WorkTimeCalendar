# Generated by Django 4.0.6 on 2022-07-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0018_procedure_alter_location_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='procedure_duration',
            field=models.IntegerField(),
        ),
    ]
