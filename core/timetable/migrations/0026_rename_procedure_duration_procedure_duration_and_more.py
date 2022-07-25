# Generated by Django 4.0.6 on 2022-07-22 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0025_appointment2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='procedure',
            old_name='procedure_duration',
            new_name='duration',
        ),
        migrations.AlterField(
            model_name='appointment2',
            name='procedure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='timetable.procedure', verbose_name='Процедура'),
        ),
        migrations.AlterField(
            model_name='appointment2',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='timetable.schedule'),
        ),
    ]