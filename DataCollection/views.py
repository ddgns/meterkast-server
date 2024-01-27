from django.shortcuts import render
from django.http import HttpResponse
import DataCollection.worker as worker
from django.http import JsonResponse

# add a scheduled task to run the data collection script every 5 seconds
collector = worker.collector()
collector.start()

# Create your views here.
# create a view that will return a list of all the data in the database
def DataList(request):
    return HttpResponse('List of all data')

def Latest(request):
    return JsonResponse(collector.reader.value_store)