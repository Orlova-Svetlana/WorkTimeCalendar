from django.db import models


class ProfessionalProfile(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название профиля')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Профессиональные профили"
        verbose_name = "Профессиональный профиль"



class Specialization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название специализации')
    professional_profile = models.ForeignKey('ProfessionalProfile', verbose_name='Профессиональный профиль', on_delete=models.CASCADE,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Специализации"
        verbose_name = "Специализация"



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
    start_work_time = models.TimeField(null=True, blank=True)
    finish_work_time = models.TimeField(null=True, blank=True)
    start_break_time = models.TimeField(null=True, blank=True)
    finish_break_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.location

    class Meta:
        unique_together = ('location', 'day_week')



class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(max_length=100, verbose_name='E-mail')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Локации"
        verbose_name = "Локация"



class Worker(models.Model):
    name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    professional_profile = models.ForeignKey('ProfessionalProfile', verbose_name='Профессиональный профиль', on_delete=models.SET_NULL, null=True)
    specialization = models.ForeignKey('Specialization', verbose_name='Специализация', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(max_length=100, verbose_name='E-mail')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Специалисты"
        verbose_name = "Специалист"


class Schedule(models.Model):
    date = models.DateField()
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    start_work_time = models.TimeField(null=True, blank=True)
    finish_work_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.date


# class Appointment(models.Model):
#     date = models.DateField()
#     worker_name = models.CharField(max_length=255)
#     appointment_time = models.TimeField()
#     procedure = models.CharField(max_length=255)
#     procedure_duration = models.TimeField()
#     location = models.CharField(max_length=255)
#     client_name = models.CharField(max_length=255)
#     phone = models.CharField(max_length=20)
