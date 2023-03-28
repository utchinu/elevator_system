from django.db import models
from django.contrib.postgres.fields import ArrayField

class Elevator_system(models.Model): 
    floors_cnt=models.IntegerField()
    elevator_cnt=models.IntegerField()


    def __str__(self):
        return ("floor cnt:"+str(self.floors_cnt)+"\n elevator_cnt :"+str(self.elevator_cnt))


class Elevator(models.Model):
    Elevator_system=models.ForeignKey("Elevator_system",on_delete=models.CASCADE)
    elevator_id=models.IntegerField(primary_key=True)
    door_status=models.BooleanField(default=False)
    is_in_order=models.BooleanField(default=True)
    destinations=ArrayField(models.IntegerField())

    def __str__(self):
        return ("Elevator_id:"+str(self.elevator_id))


