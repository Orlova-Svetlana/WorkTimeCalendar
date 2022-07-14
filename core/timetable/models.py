from django.db import models
from django.core.exceptions import ValidationError


class ProfessionalProfile(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название профиля')

    def __str__(self):
        return self.name

    # class Meta:
    #     #verbose_name_plural = "Профессиональные профили"
    #     verbose_name = "Профессиональный профиль"


class Specialization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название специализации')
    professional_profile = models.ForeignKey('ProfessionalProfile', verbose_name='Профессиональный профиль', on_delete=models.CASCADE,)

    def __str__(self):
        return self.name

    # class Meta:
    #     #verbose_name_plural = "Специализации"
    #     verbose_name = "Специализация"


class LocationWorkTime(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE,)

    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'
    week = [(MONDAY, 'Понедельник'), (TUESDAY, 'Вторник'), (WEDNESDAY, 'Среда'), (THURSDAY, 'Четверг'), (FRIDAY, 'Пятница'),
            (SATURDAY, 'Суббота'), (SUNDAY, 'Воскресенье')]
    day_week = models.CharField(max_length=3, choices=week)
    start_work_time = models.TimeField()
    finish_work_time = models.TimeField()
    start_break_time = models.TimeField(null=True, blank=True)
    finish_break_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.location)

    class Meta:
        unique_together = ('location', 'day_week')


class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(max_length=100, verbose_name='E-mail')

    def __str__(self):
        return self.name

    # class Meta:
    #     #verbose_name_plural = "Локации"
    #     verbose_name = "Локация"


class Worker(models.Model):
    name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    professional_profile = models.ForeignKey('ProfessionalProfile', verbose_name='Профессиональный профиль', on_delete=models.SET_NULL, null=True)
    specialization = models.ForeignKey('Specialization', verbose_name='Специализация', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(max_length=100, verbose_name='E-mail')

    def __str__(self):
        return self.name

    #class Meta:
        #verbose_name_plural = "Специалисты"
        #verbose_name = "Специалист"


class Schedule(models.Model):
    date = models.DateField()
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    start_work_time = models.TimeField()
    finish_work_time = models.TimeField()

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        # weekday - 0 - 6 = mon -sun

        if self.start_work_time >= self.finish_work_time:
            raise ValidationError('Время начала работы должно быть раньше времени окончания работы')

        lwtl = list(LocationWorkTime.objects.filter(location=self.location_id, day_week=LocationWorkTime.day_week.field.choices[self.date.weekday()][0]))
        if len(lwtl) == 0:
            raise ValidationError('Локация в этот день недели не работает')
        for l in lwtl:
            if (self.start_work_time < l.start_work_time) or (self.finish_work_time > l.finish_work_time):
                raise ValidationError('Время работы выходит за пределы работы локации')
            if l.start_break_time and l.finish_break_time:
                if (l.start_work_time < self.start_work_time < l.finish_break_time) or (l.start_work_time < self.finish_work_time < l.finish_break_time):
                    raise ValidationError('Время работы не должно попадать в перерыв локации')

        schedules_list = list(Schedule.objects.filter(date=self.date, worker_id=self.worker_id))
        for sch in schedules_list:
            if (sch.start_work_time < self.start_work_time < sch.finish_work_time) or (sch.start_work_time < self.finish_work_time < sch.finish_work_time):
                raise ValidationError('Время работы не должно пересекаться с другими рабочими отрезками')

        super().save(*args, **kwargs)


# class Appointment(models.Model):
#     date = models.DateField()
#     worker_name = models.CharField(max_length=255)
#     appointment_time = models.TimeField()
#     procedure = models.CharField(max_length=255)
#     procedure_duration = models.TimeField()
#     location = models.CharField(max_length=255)
#     client_name = models.CharField(max_length=255)
#     phone = models.CharField(max_length=20)
