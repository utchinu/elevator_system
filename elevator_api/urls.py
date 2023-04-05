
from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('elevator_system/',views.elevatorSystem),
    path('all_elevator_details/',views.allElevatorDetails),
    path('elevator_details/<int:id>/',views.elevatorDetails),
    path('maintainance_status/<int:id>/',views.maintainanceStatus),
]
