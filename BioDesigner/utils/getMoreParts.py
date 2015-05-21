import os
import django
import sys
import urllib2

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts

baseXmlUrl = 'http://parts.igem.org/cgi/xml/part.cgi?part='

def anaFASTA():
    #get the part from allparts.txt and save to DB
    getPartInfoDetail(partDBObj)
    
def getPartInfoDetail(partObj):
    req = urllib2.Request(baseXmlUrl+partObj.part_name)
    response = urllib2.urlopen(req)
    xmlStr = response.read()
    # analyse the xmlStr and save info to DB
    
    partObj.save()

def mainFunc():
    anaFASTA();

if __name__ == '__main__':
    mainFunc()