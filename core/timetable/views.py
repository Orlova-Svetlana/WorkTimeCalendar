from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse('timetable index')

def client(request):
    return HttpResponse('timetable client')

def worker(request):
    return HttpResponse('timetable worker')