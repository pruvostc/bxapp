'''
Date October 2018

@summary:Script to download RSS feeds on a regular basis
@author: Christian Pruvost
@note: Initial draft
'''

import codecs
import datetime
import gzip
import hashlib # for md5 digest
#import operator
import os
import platform # used in creation date detection
#import re
import urllib.request # to fetch URL 
#import httplib
#import xml.etree.ElementTree as ET

urlList = [
             'https://www.economist.com/britain/rss.xml|The Economist (Britain)',
             'https://www.economist.com/europe/rss.xml|The Economist (Europe)'
         ]


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
        #headers = handle.info() # response header
        #print(headers)
        #print("Content-Type: ", handle.info()['Content-Type'])
        
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
    #hello
    print("Processing:",thefile)

# Main 
def main():
    
    #print(os.environ)        

    #useCache = True
    dirpath = "/Users/" + os.environ['USERNAME'] +"/data/"
    CACHE = 'cache/'
    VERBOSE = True
        
    for entry in urlList:
        (url,siteName) = entry.split('|')
        
        print(",,,,--------- (start) ------- " + siteName + " ----------------------------")
        
        # an MD5 hash is generate for each URL, to be used as a filename
        md5value = hashlib.md5(url.encode('utf-8')).hexdigest()
        
        #create the cache directory if it does not exists
        if not os.path.isdir(dirpath + CACHE):
            #create the directory
            os.mkdir(dirpath + CACHE)
            
        theFile = dirpath + CACHE + md5value + '.xml'
          
        # checks if the cached file exist for this url and read it if it does
           
        if os.path.isfile(theFile):
            #read the file
            if VERBOSE:
                print("using cached version (" + theFile +") created: " + str(timestamp_to_datetime(creation_date(theFile))))
            
            processFile(theFile,siteName)

        else:
            #fetch the latest and create the file if not in cache
            response = fetchURLasString(url)
            if response is not None:
                #save it in the cache
                c_file = codecs.open(theFile, "wb") #in order to be able to write bytes to the file the 'b' is required
                c_file.write(response)
                c_file.close()
                
                processFile(theFile,siteName)
                
            else:
                print("ERROR: Unable to cache : " + url)
        
        print(",,,,------------------------- " + siteName + " ----------- (end) ----------\n")
    
if __name__ == '__main__':
    main()
    
