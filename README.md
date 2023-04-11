# Elevator_system:

## To run:
* Clone this repository and go to the directory.
* Create virtual environment and open the virtual environment.
* Install the dependencies mentioned in ***requirements.txt***
* Make database connections in ***elevator_system/elevator_system.py***
  ```
   DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'postgres',
       'USER': 'postgres',
        'PASSWORD': 'a',
        'HOST': 'localhost',
        'PORT': '5432',
    }
   } 
   
* Run migrations.
  ```
  python manage.py elevator_api makemigrations
  python manage.py run migrations
  ```

## All api's added
        
         GET /elevator_api/elevator_system/,
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
        
#### /elevator_api/elevator_system/
    GET: To get details of the elevator_system(it includes number of floors and number of number of elevtors in the system)
    POST: To initialise the elevator system.Parameters include :"floors_cnt","elevator_cnt"
    DELETE: To delete the existing elevator system
  
#### /elevator_api/all_elevator_details/
    GET: To get the details of all the elevators
 
####  /elevator_api/elevator_details/:id/
    GET: To get the details of a particular elevator(id will be provided)

#### /elevator_api/maintainance_status/:id/
    GET: To get the elevator's maintainance status
    PATCH:  To UPDATE the elevator's maintainance status.Parameters include :"is_in_order"(value can be "true" or "false").
  
#### /elevator_api/door_status/:id/  
    GET: To get the elevator's door status.
    PATCH:  To UPDATE the elevator's door status.Parameters include :"door_status"(value can be "open" or "close").

#### /elevator_api/next_destination/:id/   
     GET: To get the next destination of a particular elevator
     
#### /elevator_api/elevator_request_for_floor/:id/ 
    PATCH:When a particular elevator is requested for a particular floor("floor" has to be provided with 'elevator id').
    This api will update the destination string(append this req_floor at a location which minimises the overall duration of the elevator).
    Parameters include("floor").

#### /elevator_api/request_for_floor/'
    PATCH:When a floor is requested irrespective of the elevator("floor" has to be provided).
    This api will find the elevator with which given floor can be reached in minimum time.
    Then will update the destination string of that elevator.Parameters include("floor").
    

