from django.shortcuts import *
from django.views.generic import *
from django.urls import *




def Index(request):
    return render(request,'index.html')
