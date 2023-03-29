from .models import Elevator_system,Elevator
import json

def initialise_elevator_from_elevator_system(es_obj:Elevator_system):
    for i in range(0,es_obj.elevator_cnt):
        ele=Elevator()
        ele.elevator_id=i+1
        ele.is_in_order=True
        ele.destinations=[]
        ele.Elevator_system=es_obj
        ele.door_status=False
        ele.save()

def get_door_status_string(door:bool):
    if door == True:
        return "OPEN"
    else:
        return "CLOSE"
    
def get_maintainance_string(is_in_order:bool):
    if is_in_order==True:
        return "Working Fine"
    else:
        return "Not in order"

def get_destination_string(destinations:list):
    dest_str="( "
    for d in destinations:
        dest_str+=str(d)+", "
    dest_str+=")"
    return dest_str

def get_customised_elevator_model(elevator:Elevator):
    elevator_dict={}
    elevator_dict["elevator_id"]=elevator.elevator_id
    elevator_dict["destinations"]=get_destination_string(elevator.destinations)
    elevator_dict["door_status"]=get_door_status_string(elevator.door_status)
    elevator_dict["is_in_order"]=get_maintainance_string(elevator.is_in_order)

    return elevator_dict
