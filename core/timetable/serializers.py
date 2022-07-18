from .models import ProfessionalProfile, Specialization, Location, Worker, Schedule, Procedure, Appointment
from rest_framework import serializers

# Сериализатор: преобразует информацию, хранящуюся в базе данных и определенную с помощью моделей Django, в формат,
# который легко и эффективно передается через API.
# класс Meta описывает исходную модель и поля с названием данных, которые будут собираться

class ProfessionalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalProfile
        fields = ['url', 'id', 'name']


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['url', 'id', 'name', 'professional_profile',]
        # fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['url', 'id', 'name', 'address', 'phone', 'email']


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['url', 'id', 'name', 'phone', 'email', 'professional_profile', 'specialization']


class ScheduleSerializer(serializers.ModelSerializer):
    # location = LocationSerializer(read_only=True, many=False)
    # worker = WorkerSerializer(read_only=True, many=False)

    class Meta:
        model = Schedule
        fields = ['url', 'date', 'worker', 'location', 'start_work_time', 'finish_work_time']


class ProcedureSerializer(serializers.ModelSerializer):
    # specialization = SpecializationSerializer(read_only=True, many=False)

    class Meta:
        model = Procedure
        fields = ['url', 'id', 'name', 'procedure_duration', 'specialization']


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    pass
#     worker = serializers.PrimaryKeyRelatedField(many=False, queryset=Worker.objects.all())
#     procedure = serializers.PrimaryKeyRelatedField(many=False, queryset=Procedure.objects.all())
#     location = serializers.PrimaryKeyRelatedField(many=False, queryset=Location.objects.all())
#
#     class Meta:
#         model = Appointment
#         fields = ['date', 'worker', 'procedure', 'location', 'appointment_time', 'client_name', 'client_phone', 'client_email']







#
# class SpecializationProcedureSerializer(serializers.ModelSerializer):                       # новое для фильтров джанго
#     class Meta:
#         model = Procedure
#         fields = ['url', 'id', 'name', 'procedure_duration']
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
#         fields = ['url', 'id', 'date', 'location', 'start_work_time', 'finish_work_time']
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
#         fields = ['url', 'id', 'name', 'phone', 'email', 'professional_profile', 'specialization'
#             , 'schedule_set'
#         ]
#         # fields = '__all__'