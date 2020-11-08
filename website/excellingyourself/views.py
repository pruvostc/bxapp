from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime, os, codecs
import json
from utils import favicon
from utils import footer
from utils import emailUtil


#print("RUNNING_ENV", settings.RUNNING_ENV)
__myEnv = os.environ["RUNNING_ENV"]

__GoogleAnalytics = '''
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-137783783-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-137783783-1');
</script>
'''

__GoogleAdsense = '''<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
  (adsbygoogle = window.adsbygoogle || []).push({
    google_ad_client: "ca-pub-8994644884274858",
    google_adtest: "on",
    enable_page_level_ads: true
  });
</script>'''


def getNLPNews():
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
        print("Starting to read the file..." + dirpath + 'nlp.json')
        try:
            with codecs.open(dirpath + 'nlp.json','r',encoding='utf8') as json_file:
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
                "<!--div class=\"item_origin\">"+ newsitem['feedname'] +'</div-->' +\
                "<div class=\"item_desc\">" + \
                newsitem['desc'] + "</div>" + \
                '</div>'
                
                
            #response = response
        except:
            response = resultresponse = "<div>Oops, Something went wrong! Please come back later...</div>"
    
    return response

def index(request):
    PageName = 'excellingyourself.index'
    now = datetime.datetime.now()
    nlpNews = getNLPNews()
    context = {'PageName': PageName, 
               'time' : now,
               'nlpnews' : nlpNews,
               'googleAds': __GoogleAdsense,
               'googleAnalytics': __GoogleAnalytics,
               'faviconText': favicon.TEXT,
               'footer': footer.TEXT }
    return render(request, 'excellingyourself/index.html', context)

def vueforum(request):
    PageName = 'excellingyourself.vueforum'
    now = datetime.datetime.now()
    envURL = 'http://localhost:8000/' if (__myEnv == 'dev') else 'https://www.theblueplanet.net/'
    context = {'PageName': PageName, 
               'time' : now,
               'envUrl' : envURL,
               'googleAds': __GoogleAdsense,
               'googleAnalytics': __GoogleAnalytics,
               'faviconText': favicon.TEXT,
               'footer': footer.TEXT }
    #print(context)
    return render(request, 'forum/index.html', context)

def contact(request):
    fromField = request.POST.get('name', '')
    email = request.POST.get('email', '')
    subject = request.POST.get('subject', '')
    message = request.POST.get('text', '')
    #aaa= fromField + ' ' + email + ' ' + subject + ' ' + message
    #aaa=message
    
    emailUtil.sendMail(fromField,email,subject,message)
    
    PageName = 'excellingyourself.emailsent'
    now = datetime.datetime.now()
    context = {'PageName': PageName, 
               'time' : now, 
               'subject' : subject,
               'googleAds': __GoogleAdsense,
               'googleAnalytics': __GoogleAnalytics,
               'faviconText': favicon.TEXT,
               'footer': footer.TEXT }
    return render(request, 'excellingyourself/emailsent.html', context)
