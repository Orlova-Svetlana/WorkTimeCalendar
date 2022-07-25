from .models import ProfessionalProfile, Specialization, Location, Worker, Schedule, Procedure, Appointment
from rest_framework import serializers
from datetime import timedelta, datetime


# Сериализатор: преобразует информацию, хранящуюся в базе данных и определенную с помощью моделей Django, в формат,
# который легко и эффективно передается через API.
# класс Meta описывает исходную модель и поля с названием данных, которые будут собираться

class ProfessionalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalProfile
        fields = ['id', 'name']
        # fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name', 'professional_profile', ]
        # fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'phone', 'email']


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'name', 'phone', 'email', 'professional_profile', 'specialization']


class ScheduleSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True, many=False)
    worker = WorkerSerializer(read_only=True, many=False)

    class Meta:
        model = Schedule
        fields = ['id', 'date', 'worker', 'location', 'start_work_time', 'finish_work_time']


class CustomSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']


class CustomWorkerSerializer(serializers.ModelSerializer):
    specialization = CustomSpecializationSerializer(read_only=True, many=False)

    class Meta:
        model = Worker
        fields = ['id', 'specialization']


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ['id', 'name', 'duration', 'specialization']


class AppointmentSerializer(serializers.ModelSerializer):
    procedure_name = serializers.SerializerMethodField('get_procedure_name')
    procedure_start_time = serializers.SerializerMethodField('get_procedure_start_time')
    procedure_end_time = serializers.SerializerMethodField('get_procedure_end_time')
    procedure_duration = serializers.SerializerMethodField('get_procedure_duration')

    def get_procedure_name(self, obj):
        name = obj.procedure.name
        return name

    def get_procedure_start_time(self, obj):
        new_start_time = datetime.combine(obj.schedule.date, obj.appointment_time)
        return new_start_time.time()

    def get_procedure_end_time(self, obj):
        new_start_time = datetime.combine(obj.schedule.date, obj.appointment_time)
        new_end_time = new_start_time + timedelta(minutes=obj.procedure.duration)
        return new_end_time.time()

    def get_procedure_duration(self, obj):
        return obj.procedure.duration

    def validate(self, attrs):
        instance = Appointment(**attrs)
        instance.clean()
        return attrs

    class Meta:
        model = Appointment
        # fields = ['id', 'procedure_name', 'procedure_start_time', 'procedure_end_time', 'procedure_duration', 'appointment_time', 'client_name', 'client_phone', 'client_email', 'procedure', 'schedule']
        fields = '__all__'


class CustomScheduleSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True, many=False)
    appointments = AppointmentSerializer(read_only=True, many=True)

    class Meta:
        model = Schedule
        fields = ['id', 'date', 'start_work_time', 'finish_work_time', 'worker', 'location', 'appointments']
        # fields = '__all__'

#
# class SpecializationProcedureSerializer(serializers.ModelSerializer):                       # новое для фильтров джанго
#     class Meta:
#         model = Procedure
#         fields = ['id', 'name', 'duration']
#         # fields = '__all__'
#
#
# class WorkerSpecializationSerializer(serializers.ModelSerializer):                          # новое для фильтров джанго
#     # procedure_set = SpecializationProcedureSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = Specialization
#         # fields = [
#         #     # 'url',
#         #     'id',
#         #     'name',
#         #     # 'professional_profile',
#         #     # 'procedure_set'
#         # ]
#         fields = '__all__'
#
#
# class WorkerScheduleSerializer(serializers.ModelSerializer):                                # новое для фильтров джанго
#     location = LocationSerializer(read_only=True, many=False)
#
#     class Meta:
#         model = Schedule
#         fields = ['id', 'date', 'location', 'start_work_time', 'finish_work_time']
#         # fields = '__all__'
#
#
# class TestSerializer(serializers.ModelSerializer):
#     professional_profile = ProfessionalProfileSerializer(read_only=True, many=False)
#     specialization = WorkerSpecializationSerializer(read_only=True, many=False)        # модификация для фильтров джанго
#     schedule_set = WorkerScheduleSerializer(read_only=True, many=True)               # модификация для фильтров джанго
#
#     class Meta:
#         model = Worker
#         fields = ['id', 'name', 'phone', 'email', 'professional_profile', 'specialization'
#             , 'schedule_set'
#         ]
#         # fields = '__all__'