from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime, os, codecs
import json

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
        response = "<div>Oops, Something went wrong! Please come back later...</div>"
    else:
        try:
            with codecs.open(dirpath + 'eu.json','r') as json_file:  
                result = json.load(json_file)
            json_file.close()
    
            response = '<div class="itemblock">'
            for newsitem in result["items"]:
                response = response + "<div class=\"newstitle\"><li>" + newsitem['title'] + '</div>'
            response = response + "</div>"
        except:
            response = resultresponse = "<div>Oops, Something went wrong! Please come back later...</div>"
    
    return response


def index(request):
    #return HttpResponse("Hello, world. You're at the home index.")
    PageName = 'brexit.index'
    now = datetime.datetime.now()
    euNews = getEuropeanNews()
    context = {'PageName': PageName, 'time' : now, 'euSide': euNews}
    return render(request, 'brexit/index.html', context)
