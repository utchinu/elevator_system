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
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET','POST','DELETE'])
def elevatorSystem(request):


    """
    To initialise the elevator sytem

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
    To get/update the elevator's is_in_order status
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
            print(request.data)
            elevator.is_in_order= ((request.data.get('is_in_order')).lower()=="true")
            elevator.save()
            elevator_json=get_customised_elevator_model(elevator)
            return Response(elevator_json,status=status.HTTP_200_OK) 
        
@api_view(['PATCH'])
def elevatorRequestForFloor(request,id):
    """
    When a particular elevator is requested for a particular floor
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
        elevator_system=Elevator_system.objects.all()[0]

        requested_floor=int(request.data.get('floor'))
        if requested_floor >= elevator_system.floors_cnt or requested_floor<0 :
            data={'message':'Elevator cannot be requested to this floor'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)    
        destinations=elevator.destinations
        cur_floor=elevator.current_floor
        if len(destinations)==0:
            if cur_floor!=requested_floor :
                destinations.append(requested_floor)
        else:
            destinations=add_floor_in_destinations(requested_floor,destinations)

        if elevator.door_status==False:
            move_elevator_to_next_floor(elevator)

        elevator_json=get_customised_elevator_model(elevator)
        return Response(elevator_json,status=status.HTTP_200_OK) 
    
@api_view(['GET','PATCH'])
def doorStatus(request,id):

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
            data["Door_status"]=get_door_status_string(elevator.door_status)
            return Response(data,status=status.HTTP_200_OK)
        else:
            elevator.door_status= ((request.data.get('door_status')).lower()=="open")
            elevator.save()
            elevator_json=get_customised_elevator_model(elevator)
            return Response(elevator_json,status=status.HTTP_200_OK)                              

@api_view(['GET'])
def nextDestination(request,id):
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

 