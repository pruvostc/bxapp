from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime, os, codecs
import json
from utils import favicon

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
    
            response = ""
            i = 0
            for newsitem in result["items"]:
                i = i + 1
                date = datetime.datetime.fromtimestamp(newsitem['date']/1000.0)
                date = date.strftime("%Y-%m-%d %H:%M")
                if i > 1:
                    response = response + "<div class=\"divider\"></div>" 
                response = response + "<div class=\"newsblock\"><div class=\"newsdate\">" + date + ' - </div>' + \
                "<div class=\"newstitle\">" + \
                "<a href=\"" + newsitem['url'] + "\">" + newsitem['title'] + \
                '</a></div>' + \
                "<div class=\"item_origin\">"+ newsitem['feedname'] +'</div>' +\
                "<div class=\"item_desc\">" + \
                newsitem['desc'] + "</div>" + \
                '</div>'
                
                
            #response = response
        except:
            response = resultresponse = "<div>Oops, Something went wrong! Please come back later...</div>"
    
    return response

def getUKNews():
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
            with codecs.open(dirpath + 'uk.json','r',encoding="UTF-8") as json_file:  
                result = json.load(json_file)
            json_file.close()
    
            response = ""
            i = 0
            MAX = 12
            counter = {}
            for newsitem in result["items"]:
                i = i + 1
                date = datetime.datetime.fromtimestamp(newsitem['date']/1000.0)
                date = date.strftime("%Y-%m-%d %H:%M")
                if i >= 1 and i <= MAX :
                    
                    if newsitem['feedname'] in counter:
                        counter[newsitem['feedname']] = counter[newsitem['feedname']] + 1
                    else:
                        counter[newsitem['feedname']] = 1
                        
                    if counter[newsitem['feedname']] <= 4:
                        response = response + "<div class=\"newsblock\"><div class=\"newsdate\">" + date + ' - </div>' + \
                        "<div class=\"newstitle\">" + \
                        "<a href=\"" + newsitem['url'] + "\">" + newsitem['title'] + \
                        '</a></div>' + \
                        "<div class=\"item_origin\">"+ newsitem['feedname'] +'</div>' +\
                        "<div class=\"item_desc\">" + \
                        newsitem['desc'] + "</div>" + \
                        '</div>'
                    else:
                        i = i-1 # fetch one more instead
                        continue
                    
                    if i >= 1:
                        response = response + "<div class=\"divider\"></div>" 
                        
                if i == MAX + 1:
                    response = response + "<p><!-- see more  \u00BB --></p>"
            #response = response
        except:
            response = resultresponse = "<div>Oops, Something went wrong! Please come back later...</div>"
    
    return response

def getInclusionDetails():
    adInsert = '''<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
  (adsbygoogle = window.adsbygoogle || []).push({
    google_ad_client: "ca-pub-8994644884274858",
    google_adtest: "on",
    enable_page_level_ads: true
  });
</script>'''
    return adInsert

def index(request):
    #return HttpResponse("Hello, world. You're at the home index.")
    PageName = 'brexit.index'
    now = datetime.datetime.now()
    euNews = getEuropeanNews()
    ukNews = getUKNews()
    faviconText = favicon.TEXT
    googleAds = getInclusionDetails()
    context = {'PageName': PageName, 
               'time' : now, 
               'euSide': euNews, 
               'ukSide': ukNews, 
               'googleAds': googleAds, 
               'faviconText': faviconText }
    return render(request, 'brexit/index.html', context)

def referendum(request):
    #return HttpResponse("Hello, world. You're at the home index.")
    PageName = 'brexit.referendum'
    faviconText = favicon.TEXT
    googleAds = getInclusionDetails()
    context = {'PageName': PageName,  
               'googleAds': googleAds, 
               'faviconText': faviconText }
    return render(request, 'brexit/referendum.html', context)

def whatisbrexit(request):
    PageName = 'brexit.whatisbrexit'
    faviconText = favicon.TEXT
    googleAds = getInclusionDetails()
    context = {'PageName': PageName,  
               'googleAds': googleAds, 
               'faviconText': faviconText }
    return render(request, 'brexit/whatisbrexit.html', context)

def migration(request):
    PageName = 'brexit.migration'
    faviconText = favicon.TEXT
    googleAds = getInclusionDetails()
    context = {'PageName': PageName,  
               'googleAds': googleAds, 
               'faviconText': faviconText }
    return render(request, 'brexit/migration.html', context)

def whatnext(request):
    PageName = 'brexit.migration'
    faviconText = favicon.TEXT
    googleAds = getInclusionDetails()
    context = {'PageName': PageName,  
               'googleAds': googleAds, 
               'faviconText': faviconText }
    return render(request, 'brexit/whatnext.html', context)

def echarts(request):
    #return HttpResponse("Hello, world. You're at the home index.")
    PageName = 'brexit.echarts'
    faviconText = favicon.TEXT
    googleAds = getInclusionDetails()
    context = {'PageName': PageName,  
               'googleAds': googleAds, 
               'faviconText': faviconText }
    return render(request, 'brexit/echarts.html', context)