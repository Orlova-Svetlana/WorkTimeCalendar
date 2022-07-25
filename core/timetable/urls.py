from django.urls import path, include
from rest_framework import routers
from . import views


clientRouter = routers.DefaultRouter()
clientRouter.register(prefix=r'professionalprofiles', viewset=views.ProfessionalProfileViewSet, basename='professionalprofiles')
clientRouter.register(prefix=r'specializations', viewset=views.SpecializationViewSet, basename='specializations')
clientRouter.register(prefix=r'locations', viewset=views.LocationViewSet, basename='locations')
clientRouter.register(prefix=r'workers', viewset=views.WorkersViewSet, basename='workers')
clientRouter.register(prefix=r'schedules', viewset=views.SchedulesViewSet, basename='schedules')
clientRouter.register(prefix=r'procedures', viewset=views.ProcedureViewSet, basename='procedures')
clientRouter.register(prefix=r'appointments', viewset=views.AppointmentViewSet, basename='appointments')


workerRouter= routers.DefaultRouter()
workerRouter.register(r'workers', views.WWorkersViewSet)
workerRouter.register(r'locations', views.WLocationViewSet)
workerRouter.register(r'schedules', views.WSchedulesViewSet)
workerRouter.register(r'procedures', views.WProcedureViewSet)



urlpatterns = [
    # path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/client/', include(clientRouter.urls)),
    # path('api/v1/worker/', include(workerRouter.urls)),
    # path('admin/', views.admin_view),
]
