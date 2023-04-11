
from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('elevator_system/',views.elevatorSystem),
    path('all_elevator_details/',views.allElevatorDetails),
    path('elevator_details/<int:id>/',views.elevatorDetails),
    path('maintainance_status/<int:id>/',views.maintainanceStatus),
    path('door_status/<int:id>/',views.doorStatus),
    path('next_destination/<int:id>/',views.nextDestination),
    path('elevator_request_for_floor/<int:id>/',views.elevatorRequestForFloor),
    path('request_for_floor/',views.RequestForFloor),
]
