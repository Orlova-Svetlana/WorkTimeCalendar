from .models import ProfessionalProfile, Specialization, Location, Worker, Schedule, Procedure, Appointment
from rest_framework import viewsets
from .serializers import ProfessionalProfileSerializer, SpecializationSerializer, LocationSerializer, WorkerSerializer, \
    ScheduleSerializer, ProcedureSerializer, AppointmentSerializer\
    # , TestSerializer
from datetime import date


# Вид (ViewSet): определяет функции (чтение, создание, обновление, удаление), которые будут доступны через API.
# Здесь можно прописать локигу фильтров простым кодом или через django_filters

# def admin_view(request):
#     html = 'Admin Panel'
#     return HttpResponse(html)


class ProfessionalProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfessionalProfileSerializer
    queryset = ProfessionalProfile.objects.all()


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SpecializationSerializer
    queryset = Specialization.objects.all()

    def get_queryset(self):
        filters_dict = {}
        professional_profile = self.request.query_params.get('professional_profile')
        if professional_profile:
            filters_dict['professional_profile'] = professional_profile

        return Specialization.objects.filter(**filters_dict)


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def get_queryset(self):
        filters_dict = {}
        locations_list = []
        worker_id = self.request.query_params.get('worker')
        if worker_id:
            worker_scheduls = Schedule.objects.filter(worker=worker_id)
            if worker_scheduls:
                for i in worker_scheduls:
                    locations_list.append(i.location.id)
                filters_dict['id__in'] = locations_list

        return Location.objects.filter(**filters_dict)


class WorkersViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        filters_dict = {}
        professional_profile = self.request.query_params.get('professional_profile')
        if professional_profile:
            filters_dict['professional_profile'] = professional_profile

        specialization = self.request.query_params.get('specialization')
        if specialization:
            filters_dict['specialization'] = specialization

        location = self.request.query_params.get('location')
        if location:
            filters_dict['location'] = location

        procedure = self.request.query_params.get('procedure')
        if procedure:
            filters_dict['procedure'] = procedure

        queryset = Worker.objects.filter(**filters_dict)
        return queryset


class SchedulesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.filter(date__gte=date.today())

    def get_queryset(self):
        filters_dict = {'date__gte': date.today()}
        worker = self.request.query_params.get('worker')
        if worker:
            filters_dict['worker'] = worker

        queryset = Schedule.objects.filter(**filters_dict)
        return queryset


class ProcedureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProcedureSerializer
    queryset = Procedure.objects.all()

    def get_queryset(self):
        filters_dict = {}
        worker_id = self.request.query_params.get('worker')
        if worker_id:
            worker = Worker.objects.get(pk=worker_id)
            if worker:
                filters_dict['specialization'] = worker.specialization.id

        specialization = self.request.query_params.get('specialization')
        if specialization:
            filters_dict['specialization'] = specialization

        queryset = Procedure.objects.filter(**filters_dict)
        return queryset


class AppointmentViewSet(viewsets.ViewSet):
    serializer_class = AppointmentSerializer


# class TestViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = TestSerializer
#     queryset = Worker.objects.all().distinct()
#     filterset_fields = [
#         'specialization',
#         'professional_profile',
#         'specialization__procedure',
#         'schedule__location',
#     ]
