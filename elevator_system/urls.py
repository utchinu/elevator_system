
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('elevator_api/',include('elevator_api.urls')),
]
