from django.contrib import admin
from .models import Location, Worker, Schedule, ProfessionalProfile, Specialization, LocationWorkTime, Procedure, Appointment


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'email']


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    # list_display = ['name','professional_profile','specialization','phone','email', 'custom_field']
    list_display = ['name', 'professional_profile', 'specialization', 'phone', 'email']

    # def custom_field(self, obj):
    #     return f'{obj.professional_profile} {obj.specialization}'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "specialization":
            pid = request.POST.get('professional_profile', '')
            if pid:
                kwargs["queryset"] = Specialization.objects.filter(professional_profile__in=pid)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'worker', 'location', 'start_work_time', 'finish_work_time']


@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'professional_profile']


@admin.register(LocationWorkTime)
class LocationWorkTimeAdmin(admin.ModelAdmin):
    list_display = ['location', 'day_week', 'start_work_time', 'finish_work_time', 'start_break_time', 'finish_break_time']


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['specialization', 'name', 'duration']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'procedure', 'schedule', 'appointment_time', 'client_name', 'client_phone','client_email']
