# -*- coding: utf-8 -*-

''' downloader for www.scene.org'''
'''use ftp download'''
import ftplib
import threading
from time import sleep
import logging
import os

filelist = []
threadlist = []

    

site = 'ftp.scene.org'#main site
group = 'farb-rausch'#group
path = 'pub/music/groups/%s'%group#full path: /music/groups/group/

#logger setting
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('download.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

#callback function for retrlines
def filecallback(file):
    #mp3 filter
    if file.find('.mp3') != -1:
        print file
        filelist.append(file)
    
    
ftp = ftplib.FTP(site)
logger.info('connected')
ftp.login()
logger.info('logined')
ftp.cwd(path)
ftp.retrlines('NLST', filecallback)
logger.info('get all files')


def downloadfile(ftp, file):
    logger.info('downloading %s' % (file))
    if not os.path.exists(group):
        os.makedirs(group)
    tmpfile = open('%s/%s'%(group,file), 'wb')
    ftp.retrbinary('RETR ' + file ,tmpfile.write)
    tmpfile.close()
    logger.info('download finish %s' % (file))
class myThread (threading.Thread):
        def __init__(self, threadID,filename):
            self.threadID = threadID
            self.filename = filename
            threading.Thread.__init__(self)
            self.ftp = None
        def run(self):
            ok = True
            while ok:
                try:
                    self.ftp = ftplib.FTP(site)
                    self.ftp.login()
                    self.ftp.cwd(path)
                    logger.info('thread[%d]: downloading %s' % (self.threadID, self.filename))
                    if not os.path.exists(group):
                        os.makedirs(group)
                    tmpfile = open('%s/%s'%(group,self.filename), 'wb')
                    self.ftp.retrbinary('RETR ' + self.filename ,tmpfile.write)        
                    tmpfile.close()
                    logger.info('thread[%d]: download finish %s' % (self.threadID, self.filename))
                    self.ftp.quit()
                    ok = False
                    
                except:
                    sleep(5)

n = 1
for i in filelist:
    t = myThread(n, i)
    n += 1
    threadlist.append(t)
    t.start()
for i in threadlist:
    i.join()
logger.info('download all finish')
'''
for i in filelist:
    downloadfile(ftp, i)
'''
ftp.close()
