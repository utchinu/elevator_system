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
        
