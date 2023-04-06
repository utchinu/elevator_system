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

def get_elevator_direction(cur_floor,next_floor):
    if next_floor>cur_floor:
        return("UP")
    else:
        return("DOWN")
    

def add_floor_in_destinations(cur_floor:int,req_floor:int,destinations:list):
    if req_floor in destinations or cur_floor in destinations:
        return destinations
    
    dir=get_elevator_direction(cur_floor,destinations[0])
    is_added=False

    for i in range(0,len(destinations)):
        new_dir=get_elevator_direction(cur_floor,destinations[i])
        if new_dir==dir:
            if req_floor>min(cur_floor,destinations[i]) and req_floor<max(cur_floor,destinations[i]):
                is_added=True
                destinations=destinations.insert(i,req_floor)
                break
        else:
            if new_dir=="UP":
                if req_floor<cur_floor:
                    is_added=True
                    destinations=destinations.insert(i,req_floor)
                    break
            else:
                if req_floor>cur_floor:
                    is_added=True
                    destinations=destinations.insert(i,req_floor)
                    break
        cur_floor=destinations[i]
    
    if is_added==False:
        destinations.append(req_floor)
    return destinations
    
def move_elevator_to_next_floor(elevator:Elevator):
    if len(elevator.destinations)==0:
        return

    elevator.current_floor=elevator.destinations[0]
    for i in range(1,len(elevator.destinations)):
        elevator.destinations[i-1]=elevator.destinations[i]
    elevator.destinations.pop()
    elevator.door_status=True
    elevator.save()
    return


                
                

    