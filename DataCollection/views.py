from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# create a view that will return a list of all the data in the database
def DataList(request):
    return HttpResponse('List of all data')

def Latest(request):
    return HttpResponse('Latest datapoint')