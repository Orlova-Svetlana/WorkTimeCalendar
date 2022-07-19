from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime


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
    location = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Локация')

    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'
    week = [(MONDAY, 'Понедельник'), (TUESDAY, 'Вторник'), (WEDNESDAY, 'Среда'), (THURSDAY, 'Четверг'), (FRIDAY, 'Пятница'),
            (SATURDAY, 'Суббота'), (SUNDAY, 'Воскресенье')]
    day_week = models.CharField(max_length=3, choices=week, verbose_name='День недели')
    start_work_time = models.TimeField(verbose_name='Начало рабочего дня')
    finish_work_time = models.TimeField(verbose_name='Окончание рабочего дня')
    start_break_time = models.TimeField(null=True, blank=True, verbose_name='Перерыв с')
    finish_break_time = models.TimeField(null=True, blank=True, verbose_name='Перерыв до')

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
    date = models.DateField(verbose_name='Дата')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, verbose_name='Ф.И.О.')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Локация')
    start_work_time = models.TimeField(verbose_name='Начало рабочего периода')
    finish_work_time = models.TimeField(verbose_name='Конец рабочего периода')

    def __str__(self):
        return str(self.date)

    # def clean_fields(self, exclude=None):
    #     pass
    #
    # def full_clean(self, exclude=None, validate_unique=True):
    #     pass

    def clean(self):
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
                if (l.start_break_time < self.start_work_time < l.finish_break_time) or (l.start_break_time < self.finish_work_time < l.finish_break_time):
                    raise ValidationError('Время работы не должно попадать в перерыв локации')

        schedules_list = list(Schedule.objects.filter(date=self.date, worker_id=self.worker_id))
        for sch in schedules_list:
            if (sch.start_work_time < self.start_work_time < sch.finish_work_time) or (sch.start_work_time < self.finish_work_time < sch.finish_work_time):
                raise ValidationError('Время работы не должно пересекаться с другими рабочими отрезками')


class Procedure(models.Model):
    specialization = models.ForeignKey('Specialization', verbose_name='Специализация', on_delete=models.SET_NULL,
                                       null=True)
    name = models.CharField(max_length=100, verbose_name='Процедура')
    procedure_duration = models.IntegerField(verbose_name='Длительность процедуры в мин')

    def __str__(self):
        return f'{self.name} ({str(self.specialization)})'


class Appointment(models.Model):
    date = models.DateField(verbose_name='Дата')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, verbose_name='Ф.И.О. специалиста')
    procedure = models.ForeignKey('Procedure', on_delete=models.CASCADE, verbose_name='Процедура')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Локация')
    appointment_time = models.TimeField(verbose_name='Время записи')
    client_name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    client_phone = models.CharField(max_length=20, verbose_name='Телефон')
    client_email = models.EmailField(max_length=100, verbose_name='E-mail')

    def clean(self):
        worker_work_time_list = list(Schedule.objects.filter(worker=self.worker_id, location=self.location_id, date=self.date))
        if not worker_work_time_list:
            raise ValidationError('Специалист в этот день в этой локации не работает')

        appointment_time_list = list(Appointment.objects.filter(worker=self.worker_id, location=self.location_id, date=self.date))

        worker = Worker.objects.filter(pk=self.worker_id, specialization__procedure=self.procedure_id)
        if not worker:
            raise ValidationError('Специалист не выполняет выбранную процедуру')

        procedure = Procedure.objects.get(pk=self.procedure_id)

        new_start_time = datetime.combine(self.date, self.appointment_time)
        new_end_time = new_start_time + timedelta(minutes=procedure.procedure_duration)

        for app in appointment_time_list:
            app_start_time = datetime.combine(app.date, app.appointment_time)
            app_end_time = app_start_time + timedelta(minutes=Procedure.objects.get(pk=app.procedure_id).procedure_duration)

            if (app_start_time < new_start_time < app_end_time) or (app_start_time < new_end_time < app_end_time):
                raise ValidationError('Время записи не должно попадать в уже имеющуюся запись')

        for wor in worker_work_time_list:
            wor_start_time = datetime.combine(wor.date, wor.start_work_time)
            wor_end_time = datetime.combine(wor.date, wor.finish_work_time)

            if not (wor_start_time < new_start_time < wor_end_time) or not (wor_start_time < new_end_time < wor_end_time):
                raise ValidationError('Время записи должно попадать в рабочее время специалиста')

