from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime, os, codecs

def getEuropeanNews():
    dirpath = "./"
    if 'USERNAME' in os.environ and os.environ['USERNAME'] != '':
        dirpath = "/Users/" + os.environ['USERNAME'] + "/data/"
    if 'HOME' in os.environ and os.environ['HOME'] != '':
        dirpath = os.environ['HOME'] + "/data/"
    CACHE = 'cache/'
    response = ''
    if not os.path.isdir(dirpath + CACHE):
        print("ERROR: Unable to open folder :" + dirpath + CACHE)
        response = "Oops, Something went wrong! Please come back later..."
    else:
        response = "eu news goes here"
        theFile = dirpath + CACHE + '9_3f44483c097dcd65b344b9290e1c0823.xml'
        c_file = codecs.open(theFile, "rb") #in order to be able to write bytes to the file the 'b' is required
        response = c_file.read()
        c_file.close()
    
    return response


def index(request):
    #return HttpResponse("Hello, world. You're at the home index.")
    PageName = 'brexit.index'
    now = datetime.datetime.now()
    euNews = getEuropeanNews()
    context = {'PageName': PageName, 'time' : now, 'euSide': euNews}
    return render(request, 'brexit/index.html', context)
