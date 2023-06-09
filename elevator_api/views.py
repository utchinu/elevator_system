from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Elevator_system
from .serializers import Elevator_system_Serializer,Elevator_Serializer
from .utils import *
import json
#from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /elevator_api/elevator_system/',
        'POST /elevator_api/elevator_system/',
        'DELETE /elevator_api/elevator_system/',

        'GET /elevator_api/all_elevator_details/',
        'GET /elevator_api/elevator_details/:id/',
        'GET /elevator_api/maintainance_status/:id/',
        'PATCH /elevator_api/maintainance_status/:id/',

        'GET /elevator_api/door_status/:id/',
        'PATCH /elevator_api/door_status/:id/',

        'GET /elevator_api/next_destination/:id/',

        'PATCH /elevator_api/elevator_request_for_floor/:id/',

        'PATCH /elevator_api/request_for_floor/'
    ]
    return Response(routes)

@api_view(['GET','POST','DELETE'])
def elevatorSystem(request):


    """
    POST:To initialise the elevator sytem
    GET: To get the details of the elevator system
    DELETE: To delete the existing eleavator system

    """
    if request.method=='POST':
        elevator_system_cnt=Elevator_system.objects.all().count()
        if elevator_system_cnt==1:
            data={'message':'Elevator system is already initialised'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        data={
            'floors_cnt':request.data.get('floors_cnt'),
            'elevator_cnt': request.data.get('elevator_cnt'),
        }
        serializer=Elevator_system_Serializer(data=data)
        if serializer.is_valid():
            es_obj=serializer.save()
            initialise_elevator_from_elevator_system(es_obj=es_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='GET':
        elevator_system_cnt=Elevator_system.objects.all().count()
        if elevator_system_cnt==0:
            data={'message':'Elevator system is not initialised'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        else:
            es_obj=Elevator_system.objects.all()[0]
            serializer1=Elevator_system_Serializer(es_obj)

            return Response(serializer1.data, status=status.HTTP_201_CREATED)
        
    elif request.method =='DELETE':
        elevator_system_cnt=Elevator_system.objects.all().count()
        if elevator_system_cnt==0:
            data={'message':'Elevator system is not initialised'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        es_obj=Elevator_system.objects.all()
        es_obj.delete()
        return Response({"res":"Elevator system deleted!"},status=status.HTTP_200_OK)        
        
@api_view(['GET'])
def elevatorDetails(request,id):
    """
    GET: To get the details of a particular elevator(id will be provided)
    """


    elevator_system_cnt=Elevator_system.objects.all().count()
    if elevator_system_cnt==0:
        data={'message':'Elevator system is not initialised'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)     
    elevator=Elevator.objects.filter(elevator_id = id)[0]
    if elevator == None:
        data={'message':'Elevator with given key does not exist'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        elevator_json=get_customised_elevator_model(elevator)
        return Response(elevator_json,status=status.HTTP_200_OK) 
    
@api_view(['GET'])
def allElevatorDetails(request):

    """
    GET: To get the details of all the elevators
    """
    elevator_system_cnt=Elevator_system.objects.all().count()
    if elevator_system_cnt==0:
        data={'message':'Elevator system is not initialised'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)     
    all_elevators=Elevator.objects.all()
    all_elevators_mod=[] 
    for e in all_elevators:
        all_elevators_mod.append(get_customised_elevator_model(e))
    all_elevators_mod_json=json.dumps(all_elevators_mod)
    return Response(all_elevators_mod,status=status.HTTP_200_OK)


@api_view(['GET','PATCH'])
def maintainanceStatus(request,id):
    """
    GET: To get the elevator's maintainance status(id will be provided)
    PATCH:  To UPDATE the elevator's maintainance status(id will be provided)
    """

    elevator_system_cnt=Elevator_system.objects.all().count()
    if elevator_system_cnt==0:
        data={'message':'Elevator system is not initialised'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)     
    elevator=Elevator.objects.filter(elevator_id = id)[0]

    if elevator == None:
        data={'message':'Elevator with given key does not exist'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method=='GET':
            data={}
            data["Eleavtor_id"]=elevator.elevator_id
            data["Elevator_is_in_order"]=get_maintainance_string(elevator.is_in_order)
            return Response(data,status=status.HTTP_200_OK)
        elif request.method=='PATCH':
            elevator.is_in_order= ((request.data.get('is_in_order')).lower()=="true")
            if elevator.is_in_order == False:
                elevator.destinations.clear()
                elevator.current_floor=0
                elevator.door_status=False
            elevator.save()
            elevator_json=get_customised_elevator_model(elevator)
            return Response(elevator_json,status=status.HTTP_200_OK) 
        
@api_view(['PATCH'])
def elevatorRequestForFloor(request,id):
    """
        PATCH:When a particular elevator is requested for a particular floor("floor" has to be provided with 'elevator id').
        This api will update the destination string(append this req_floor at a location which minimises the overall duration of the elevator)
    """
    elevator_system_cnt=Elevator_system.objects.all().count()
    if elevator_system_cnt==0:
        data={'message':'Elevator system is not initialised'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)     
    elevator=Elevator.objects.filter(elevator_id = id)[0]

    if elevator == None:
        data={'message':'Elevator with given key does not exist'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
    elif elevator.is_in_order == False:
        data={'message':'Elevator is not in order currently'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)        
    else:
        elevator_system=Elevator_system.objects.all()[0]

        requested_floor=int(request.data.get('floor'))
        if requested_floor >= elevator_system.floors_cnt or requested_floor<0 :
            data={'message':'Elevator cannot be requested to this floor'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)    
        
        #print(elevator.destinations)
        cur_floor=elevator.current_floor
        if len(elevator.destinations)==0:
            if cur_floor!=requested_floor :
                elevator.destinations.append(requested_floor)
        else:
            elevator.destinations=add_floor_in_destinations(elevator.current_floor,requested_floor,elevator.destinations)


        #print(elevator.destinations)
        elevator.save()

        if elevator.door_status==False:
            move_elevator_to_next_floor(elevator)

        elevator_json=get_customised_elevator_model(elevator)
        return Response(elevator_json,status=status.HTTP_200_OK) 
    
@api_view(['GET','PATCH'])
def doorStatus(request,id):

    """
        GET: To get the elevator's door status(id will be provided)
        PATCH:  To UPDATE the elevator's door status(id will be provided)
    """
    elevator_system_cnt=Elevator_system.objects.all().count()
    if elevator_system_cnt==0:
        data={'message':'Elevator system is not initialised'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)     
    elevator=Elevator.objects.filter(elevator_id = id)[0]

    if elevator == None:
        data={'message':'Elevator with given key does not exist'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method=='GET':
            data={}
            data["Eleavtor_id"]=elevator.elevator_id
            return Response(data,status=status.HTTP_200_OK)
        else:
            elevator.door_status= ((request.data.get('door_status')).lower()=="open")
            elevator.save()
            if elevator.door_status==False:
                move_elevator_to_next_floor(elevator)
            elevator_json=get_customised_elevator_model(elevator)
            return Response(elevator_json,status=status.HTTP_200_OK)                              

@api_view(['GET'])
def nextDestination(request,id):
    """
    GET: To get the next destination of a particular elevator
    """
    elevator_system_cnt=Elevator_system.objects.all().count()
    if elevator_system_cnt==0:
        data={'message':'Elevator system is not initialised'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)     
    elevator=Elevator.objects.filter(elevator_id = id)[0]

    if elevator == None:
        data={'message':'Elevator with given key does not exist'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        if len(elevator.destinations)==0:
            data={'message':'Next destination deos not exist'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)                     
        data={}
        data["Eleavtor_id"]=elevator.elevator_id
        data["Next_destination"]=elevator.destinations[0]
        return Response(data,status=status.HTTP_200_OK)       

@api_view(['PATCH'])
def RequestForFloor(request):

    """
        PATCH:When a floor is requested irrespective of the elevator("floor" has to be provided).
        This api will find the elevator with which given floor can be reached in minimum time.
        Then will update the destination string of that elevator
    """
    elevator_system_cnt=Elevator_system.objects.all().count()
    if elevator_system_cnt==0:
        data={'message':'Elevator system is not initialised'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)     
    elevator_list=Elevator.objects.filter(is_in_order = True)

    if len(elevator_list)==0:
        data={'message':'No working elevator exists'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)          

    requested_floor=int(request.data.get('floor'))
    elevator_system=Elevator_system.objects.all()[0]
    if requested_floor >= elevator_system.floors_cnt or requested_floor<0 :
        data={'message':'Elevator cannot be requested to this floor'}
        return Response(data,status=status.HTTP_400_BAD_REQUEST)      

    chosen_elevator=elevator_list[0]
    chosen_dist=1e18

    for e in elevator_list:
        temp_dist=get_distance_for_floor_in_elevator(e.current_floor,requested_floor,e.destinations)
        if temp_dist<chosen_dist:
            chosen_dist=temp_dist
            chosen_elevator=e
    
 
    cur_floor=chosen_elevator.current_floor
    if len(chosen_elevator.destinations)==0:
        if cur_floor!=requested_floor :
            chosen_elevator.destinations.append(requested_floor)
    else:
        chosen_elevator.destinations=add_floor_in_destinations(chosen_elevator.current_floor,requested_floor,chosen_elevator.destinations)

    chosen_elevator.save()

    if chosen_elevator.door_status==False:
        move_elevator_to_next_floor(chosen_elevator)

    elevator_json=get_customised_elevator_model(chosen_elevator)
    return Response(elevator_json,status=status.HTTP_200_OK)    