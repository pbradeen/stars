"""
Version that goes through the directory and cleans up directory names and creates directories for files
"""
version = '1.0'

import os
import sys
import time
import shutil
# import datetime
# from subprocess import call
from time import gmtime, strftime
import ConfigParser
import traceback
import string
import re
# import io
from pIMDB import pIMDB
from urllib import urlopen
import urllib2


def GetMovieData (name):
    try:
        movie = re.sub(r'[^a-zA-Z0-9\']+', ' ', name)
        imdb = pIMDB(movie)
        imdb.parse_imdb_page()
        webpage = imdb.imdb_link
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        #infile = opener.open('http://en.wikipedia.org/w/index.php?title=movie %s&printable=yes' % (name))
        #wikidata = infile.read()
        infile = opener.open(webpage)
        imdbdata = infile.read()       
        return imdbdata  # + wikidata
    except Exception ,e:
        print "Error %s with name: %s" %(str(e),name)
        return ""
    

        
        
def FileStats (filename):
    import hashlib
    m = hashlib.md5()
    ifile = open(filename, 'rb')
    for line in ifile:
        m.update(line)
    return "%s" % (m.hexdigest())

def getconfdef(config,section,param,default):
    try:
        retval=config.get(section,param)
    except:
        retval=default
    return retval

logpath = ""

def logmsg(msg):
        logfile = open(logpath,'a')
        logfile.write(msg + '\n')
        logfile.close
def bylength(word1, word2):
    """
    write your own compare function:
    returns value > 0 of word2 longer then word1
    returns value = 0 if the same length
    returns value < 0 of word1 longer than word2
    """
    return len(word2) - len(word1)


def cleanup (filename):
    newdirectory = string.replace(filename,".","")   # take out periods
    newdirectory = string.replace(newdirectory,"_","")   # take out periods
    newdirectory = string.replace(newdirectory,"-","")   # take out periods
    newdirectory = string.replace(newdirectory," ","")   # take out periods
    newdirectory = newdirectory.lower()
    return newdirectory

#
#  Main code
# Loop to go through directory and find files.  then put files into new directories
#
if __name__ == '__main__':



    try:
    
        config = ConfigParser.RawConfigParser(allow_no_value=True)
    
        config.read("/etc/organizer.conf")
    
        frompath= getconfdef(config,"directories","from","i:/unsorted")
        
        topath = getconfdef(config,'directories','to','i:/virp')
    
        tmp = getconfdef(config,"directories","tmp","e:/temp")
    
        logpath = "e:/movie.log"
        infofile = 'info.txt'
        validextensions = [".avi",".mp4",".wmv",".srt",".mpg",".mkv",".mpeg",".mv4",".mov"]
        
    
                
    
        print "Version "+ version +" started up:"
        print "From: " + frompath
        print "Log: " + logpath
        print "Temp :" + tmp
        
        starnames=os.listdir(topath)
        starnames.sort(cmp=bylength) #Sort longest to shortest
        print starnames
        dirList=os.listdir(frompath)
        os.chdir(frompath)
        for fname in dirList:
            try:
                fromdir = frompath+'/'+fname

                cleanname = cleanup(fname)
                #print "Clean Name: %s" % (cleanname)
                for star in starnames:
                    cleanstar=star.lower().replace(' ','')
                    if cleanname.find(cleanstar)!= -1:
                        print 'Found %s in %s' % (cleanstar,fname)
                        try:
                            todir = topath+'/'+star
                            shutil.move(fromdir, todir)
                            print 'Moved %s to %s' %(fromdir,todir)
                            break
                        except Exception, e:
                            print 'Error %s moving %s to %s' % (str(e),fromdir,todir)
                            break
                else:
                    print 'Nothing found in %s' % (fname)
                     
            except :
                traceback.print_exc()
    except :  
        traceback.print_exc()
print 'done'