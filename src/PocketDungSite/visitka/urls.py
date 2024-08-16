from django.urls import path  
from . import views  

app_name = "wiki" #пространство имен для приложения visitka
urlpatterns = [ 
    path("", views.index, name="index"),
]