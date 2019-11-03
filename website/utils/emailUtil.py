#!/usr/bin/python3.7

'''
Date October 2019

@summary:Script to send email using google mail
@author: Christian Pruvost
@note: Initial SMTP handler script
'''
########## IMPORTING LIBRARIES ###########
import sys
import logging, logging.handlers
from logging.handlers import SMTPHandler
from website import secretsettings   #secret_app_k=secretsettings.secret_app_k

# sendMail tool using a google secret application Key 
def sendMail(fromname = 'No Name', email = 'noEmail@provided.com', subjectData ='No Subject', data = 'no message provided...'):
    recipients = ['coachingmarvel@gmail.com']
    log = logging.getLogger("mylogger")
    log.setLevel(logging.DEBUG)
    emailh = logging.handlers.SMTPHandler(mailhost=('smtp.gmail.com',587),
        fromaddr=email,
        toaddrs=recipients,
        subject=subjectData,
        credentials=('coachingmarvel@gmail.com',secretsettings.secret_app_k),
        secure=())
    emailh.setLevel(logging.INFO)
    log.addHandler(emailh)
    log.info(data + '\n---------------\n\nsent by website contact us from:\n' + fromname)
    
    
if __name__ == '__main__':
    main()
    
