from django.contrib import admin
from .models import Location, Worker, Schedule, ProfessionalProfile, Specialization, LocationWorkTime
# , Appointment,


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name','address','phone','email']


class WorkerAdmin(admin.ModelAdmin):
    # list_display = ['name','professional_profile','specialization','phone','email', 'custom_field']
    list_display = ['name','professional_profile','specialization','phone','email']

    # def custom_field(self, obj):
    #     return f'{obj.professional_profile} {obj.specialization}'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "specialization":
            pid = request.POST.get('professional_profile', '')
            if pid:
                kwargs["queryset"] = Specialization.objects.filter(professional_profile__in=pid)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['date','worker','location','start_work_time','finish_work_time']


class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ['name']


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name','professional_profile']


class LocationWorkTimeAdmin(admin.ModelAdmin):
    list_display = ['location', 'day_week','start_work_time','finish_work_time','start_break_time','finish_break_time']


admin.site.register(Location, LocationAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Schedule, ScheduleAdmin)
# admin.site.register(Appointment)
admin.site.register(ProfessionalProfile)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(LocationWorkTime, LocationWorkTimeAdmin)