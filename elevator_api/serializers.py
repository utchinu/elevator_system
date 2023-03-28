from rest_framework import serializers
from .models import Elevator_system,Elevator


class Elevator_system_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator_system
        fields = '__all__'

class Elevator_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'

    