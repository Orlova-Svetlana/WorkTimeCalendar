from django.contrib.auth.models import User, Group
from .models import Appointment, Worker, Procedure, Location
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    worker = serializers.PrimaryKeyRelatedField(many=False, queryset=Worker.objects.all())
    procedure = serializers.PrimaryKeyRelatedField(many=False, queryset=Procedure.objects.all())
    location = serializers.PrimaryKeyRelatedField(many=False, queryset=Location.objects.all())

    class Meta:
        model = Appointment
        fields = ['date', 'worker', 'procedure', 'location', 'appointment_time', 'client_name', 'client_phone', 'client_email']