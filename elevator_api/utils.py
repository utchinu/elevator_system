from .models import Elevator_system,Elevator


def initialise_elevator_from_elevator_system(es_obj:Elevator_system):
    for i in range(0,es_obj.elevator_cnt):
        ele=Elevator()
        ele.elevator_id=i+1
        ele.is_in_order=True
        ele.destinations=[]
        ele.Elevator_system=es_obj
        ele.door_status=False
        ele.save()