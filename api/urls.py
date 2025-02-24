from django.contrib import admin
from django.urls import path,include
from .message import getMessage
urlpatterns = [
    
    
    
    path('getMessage/',getMessage.as_view())



]
