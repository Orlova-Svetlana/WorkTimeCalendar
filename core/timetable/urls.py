from django.urls import path, include
from rest_framework import routers
from . import views


clientRouter = routers.DefaultRouter()
clientRouter.register(r'professionalprofiles', views.ProfessionalProfileViewSet)
clientRouter.register(r'specializations', views.SpecializationViewSet)
clientRouter.register(r'locations', views.LocationViewSet)
clientRouter.register(r'workers', views.WorkersViewSet)
clientRouter.register(r'schedules', views.SchedulesViewSet)
clientRouter.register(r'procedures', views.ProcedureViewSet)
# clientRouter.register(r'appointments', views.ViewSet)
#clientRouter.register(r'test', views.TestViewSet)


workerRouter= routers.DefaultRouter()
workerRouter.register(r'workers', views.WWorkersViewSet)
workerRouter.register(r'locations', views.WLocationViewSet)
workerRouter.register(r'schedules', views.WSchedulesViewSet)
workerRouter.register(r'procedures', views.WProcedureViewSet)



urlpatterns = [
    # path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/client/', include(clientRouter.urls)),
    path('api/v1/worker/', include(workerRouter.urls)),
    # path('admin/', views.admin_view),
]
