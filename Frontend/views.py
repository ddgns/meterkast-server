from django.shortcuts import render
from django.http import HttpResponse
import DataCollection.worker as worker

# Create your views here.
def index(request):
    # get the latest data from the worker
    collector_instance = worker.collector()
    value_store = collector_instance.reader.value_store
    data = {
        "verbruikstand": value_store["verbruik stand 1"] + value_store["verbruik stand 2"],
        "leverstand": value_store["lever stand 1"] + value_store["lever stand 2"],
        "vermogen": value_store["verbruik"] - value_store["leveren"],
        "gas": value_store["aardgas"]
    }
    
    return render(request, 'index.html', data)
