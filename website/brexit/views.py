from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime

def index(request):
    #return HttpResponse("Hello, world. You're at the home index.")
    PageName = 'brexit.index'
    now = datetime.datetime.now()
    context = {'PageName': PageName, 'time' : now}
    return render(request, 'brexit/index.html', context)