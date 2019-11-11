from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime, os, codecs
import json
from utils import favicon
from utils import footer
from utils import emailUtil

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

def index(request):
    PageName = 'coachingmagic.index'
    now = datetime.datetime.now()
    context = {'PageName': PageName, 
               'time' : now, 
               'googleAds': __GoogleAdsense,
               'googleAnalytics': __GoogleAnalytics,
               'faviconText': favicon.TEXT,
               'footer': footer.TEXT }
    return render(request, 'excellingyourself/index.html', context)


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
