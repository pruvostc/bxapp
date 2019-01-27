#!/usr/bin/python3.7

'''
Date October 2018

@summary:Script to download RSS feeds on a regular basis
@author: Christian Pruvost
@note: Initial draft
'''
########## IMPORTING LIBRARIES ############
import codecs
import datetime
import time
import gzip
import hashlib # for md5 digest
#import operator
import os
import platform # used in creation date detection
#import re
import urllib.request # to fetch URL 
import urllib.parse # to encode/decode url
#import httplib
import xml.etree.ElementTree as ET
import json
CRISPYAPPSPOT = "https://crispy-snippets.appspot.com/datafeed"
#CRISPYAPPSPOT = "http://localhost:8080/datafeed"
VERBOSE = True

# canditates
'''
http://europa.eu/rapid/rss.htm
https://europa.eu/newsroom/rss-feeds_en
'''
urlList = [
             'https://www.economist.com/britain/rss.xml|The Economist (Britain)|1',
             'https://www.economist.com/europe/rss.xml|The Economist (Europe)|2',
             'http://feeds.bbci.co.uk/news/rss.xml|BBC Newsfeed (Top News)|3',
             'http://feeds.bbci.co.uk/news/uk/rss.xml|BBC Newsfeed (UK)|4',
             'http://feeds.bbci.co.uk/news/world/europe/rss.xml|BBC Newsfeed (Europe)|5',
             'http://www.lefigaro.fr/rss/figaro_economie.xml|LeFigaro Economie (France)|6',
             'https://observer.com/feed/|The Observer (Britain)|7',
             'http://europa.eu/rapid/search-result.htm?quickSearch=1&text=brexit&language=EN&format=RSS|European Commission (Europe)|8',
             'http://feeds.bbci.co.uk/news/politics/uk_leaves_the_eu/rss.xml|BBC Politics (UK)|9'
         ]

ns = {
    'dc' : 'http://purl.org/dc/elements/1.1/',
    'atom' : 'http://www.w3.org/2005/Atom',
    'media' :"http://search.yahoo.com/mrss/",
    'content' : "http://purl.org/rss/1.0/modules/content/"
}
# returns the creation date of a File
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

# convert timestamp milliseconds to yyyy-mm-dd hh:mm:ss
def timestamp_to_datetime(timestamp = 0):
    timestamp = int(timestamp) # truncate milliseconds since not needed for this
    return datetime.datetime.fromtimestamp(timestamp)
            
#fetch URL
def fetchURLasString(url):
    response = None
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept-Encoding', 'gzip, deflate') # will create issues once the content is compressed
        req.add_header('Accept-Language', 'en-US,en;q=0.8,fr;q=0.6')
        req.add_header('Upgrade-Insecure-Requests', '1')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
        req.add_header('If-None-Match', '"e1e85-55441ae463f40"')
        req.add_header('Connection', 'keep-alive')
        
        # some feeds do not re-deliver the data if the cache value has a recent date - leading to HTTP error 304
        req.add_header('If-Modified-Since', 'Fri, 14 Jul 2013 07:05:57 GMT') # old date to ensure we get the latest

        handle = urllib.request.urlopen(req) # open the connection and get the response
        
        # fiddle with headers
        if VERBOSE:
            headers = handle.info() # response header
            print(headers)
            print("Content-Type: ", handle.info()['Content-Type'])
        
        # detect if the content is compressed or not.
        if (handle.info()['Content-Encoding'] is not None) and (handle.info()['Content-Encoding'] == 'gzip'):
            #response = str(gzip.decompress(handle.read())) # otherwise we have a bytes variable, not a string
            response = gzip.decompress(handle.read())
        else:
            #response = str(handle.read())
            response = handle.read()

    except Exception as e:
        print(str(e)) # output the error
        #print httplib.HTTP_RESPONSE_CODES[str(e)]
    return response

# main processor
def processFile(thefile,federationName):
    #TODO - Do something with it (coming soon...)
    print("Processing:",thefile)

# generate querystring for the data feed
def getSignedURL(source):
    #msg = "src=" + src + "&s=" + stamp + secretToHide;
    
    # The time.time() function returns the number of seconds since the epoch, as seconds. 
    # Note that the "epoch" is defined as the start of January 1st, 1970 in UTC. 
    # So the epoch is defined in terms of UTC. [by squiguy, StackOverflow] 
    #utcmilliseconds = int(datetime.datetime.utcnow().timestamp()*1000)

    utcmilliseconds = int(time.time()*1000) # UTC time in milliseconds
    
    qstring = "src=" + str(urllib.parse.quote_plus(source,encoding="UTF-8")) + "&s="  + str(utcmilliseconds)
    print(">>>>" + str(urllib.parse.quote_plus(source,encoding="UTF-8")))
    #print(urllib.parse.urlencode(source))
    secretToHide = "30268606F8B95F76B300D27630AFAC4E"
    strToHash = qstring+secretToHide
    sha256Value = hashlib.sha256(strToHash.encode("utf-8")).hexdigest()
    qstring = qstring + "&sig=" + sha256Value 
    if VERBOSE:
        print(qstring)
    return CRISPYAPPSPOT + "?" + qstring
    
# Main 
def main():
    fetchData()
    buildNewsFeed()
    
def fetchData():    
    #print(os.environ)        

    #useCache = True
    dirpath = "/Users/" + os.environ['USERNAME'] + "/data/"
    if 'HOME' in os.environ and os.environ['HOME'] != '':
        dirpath = os.environ['HOME'] + "/data/"
    CACHE = 'cache/'
        
    for entry in urlList:
        (url,siteName,refnum) = entry.split('|')
        
        print(",,,,--------- (start) ------- " + siteName + " ----------------------------")
        
        # an MD5 hash is generate for each URL, to be used as a filename
        md5value = hashlib.md5(url.encode('utf-8')).hexdigest()
        
        #create the cache directory if it does not exists
        if not os.path.isdir(dirpath):
            #create the directory 'data'
            os.mkdir(dirpath)
        if not os.path.isdir(dirpath + CACHE):
            #create the directory 'cache'
            os.mkdir(dirpath + CACHE)
        
        # the output file for this particilar <refnum>  
        theFile = dirpath + CACHE + refnum + '_' + md5value + '.xml'
          
        # checks if the cached file exist for this url and read it if it does
           
        if os.path.isfile(theFile) and int(time.time()-creation_date(theFile)) < 43200: # more than 12h (43200s)
            #read the file
            if VERBOSE:
                print(str(timestamp_to_datetime(creation_date(theFile))), str(timestamp_to_datetime(time.time())))
                print("using cached version (" + theFile +") created: " + str(timestamp_to_datetime(creation_date(theFile))))
            
            processFile(theFile,siteName)

        else:
            #fetch the latest and create the file if not in cache
            ####NEED TO FETCH THE CONVERTEDURL FOR APPSPOT.COM
            print("CRISPYURL: " + getSignedURL(url))
            response = fetchURLasString(getSignedURL(url))
            #response = fetchURLasString(url)
            if response is not None:
                #save it in the cache
                #output = response.decode()
                #output = "".join( chr(x) for x in response)

                c_file = codecs.open(theFile, "wb") #in order to be able to write bytes to the file the 'b' is required
                c_file.write(response)
                c_file.close()
                
                processFile(theFile,siteName)
                
            else:
                print("ERROR: Unable to cache : " + url)
        
        print(",,,,------------------------- " + siteName + " ----------- (end) ----------\n")

def buildNewsFeed():
    # location - same as in fetchData()...
    dirpath = "/Users/" + os.environ['USERNAME'] + "/data/"
    if 'HOME' in os.environ and os.environ['HOME'] != '':
        dirpath = os.environ['HOME'] + "/data/"
    CACHE = 'cache/'
    if not os.path.isdir(dirpath + CACHE):
        print("ERROR: Unable to open folder :" + dirpath + CACHE)
    else:
        fileList = os.listdir(dirpath + CACHE)
        #go through all the feed files
        
        AlljsonData = {}
        for name in fileList:
            if name.endswith('.xml'):
                print("-----------extracting news from " + dirpath + CACHE + name + " ----------")
                feednum = name[:1]
                root = ET.parse(dirpath + CACHE + name)
                length = len(root.findall('channel/item',ns))
                i = 0
                for item in root.findall('channel/item',ns):
                    i = i+1
                    jsonData = {}
                    jsonData.update(getElem(item,'title','title'))
                    jsonData.update(getElem(item,'desc','description'))
                    jsonData.update(getElem(item,'url','link'))
                    #<pubDate>Sun, 27 Jan 2019 18:22:32 GMT</pubDate>
                    jsonData.update(getElem(item,'date','pubDate'))
                    jsonData['feednum'] = feednum
                    if 'items' in AlljsonData:
                        AlljsonData['items'].extend([jsonData])
                    else:
                        AlljsonData['items'] = [jsonData]
        print(json.dumps(AlljsonData, indent=4, sort_keys=True))
        #filter4Brexit(AlljsonData)
        #deduplicate(AlljsonData)
        

def getElem (item, elem, string_xpath, namespace = ns):
    element = {}
    for entryElem in item.findall(string_xpath, namespace):
        if ET.iselement(entryElem):
            element[elem] = entryElem.text
    return element


if __name__ == '__main__':
    main()
    
