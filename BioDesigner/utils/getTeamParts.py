import os
import django
import sys
from BeautifulSoup import BeautifulSoup
import urllib2

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import teams, team_parts, parts

regionList2014 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_North America']
regionList2013 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_North America']
regionList2012 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_Americas East', 'table_Teams_from_Americas West']
regionList2011 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Americas']
regionList2010 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Canada', 'table_Teams_from_Latin America', 'table_Teams_from_US']
regionList2007 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Canada', 'table_Teams_from_Latin America', 'table_Teams_from_US', 'table_Teams_from_Other']
regionList2006 = ['table_Teams_from_Other']



def getTeamDict(baseUrl):
    result = dict()
    req = urllib2.Request(baseUrl)
    response = urllib2.urlopen(req)
    htmlStr = response.read()
    teamDict = analyseHTMLPage(htmlStr)
    for teamname in teamDict:
        saveParts(teamDict[teamname]['url'], teamname)
        
def saveParts(wikiUrl, teamname):
    req = urllib2.Request(wikiUrl)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    response = urllib2.urlopen(req)
    htmlStr = response.read()
    soup = BeautifulSoup(htmlStr)
    # get favorite parts
    try:
        partsTable1 = soup.find(id='Table_1')
        part_names = partsTable1.findAll('a')
        for part in part_names:
            print '%s,2010,%s' % (teamname, part.string)
    except:
        pass
    try:
        partTable2 = soup.find(id='Table_2')
        part_names = partTable2.findAll('a')
        for part in part_names:
            print '%s,2010,%s' % (teamname, part.string)
    except:
        pass


def analyseHTMLPage(htmlStr):
    resultDict = dict()
    soup = BeautifulSoup(htmlStr)
    for regionStr in regionList2010:
        regionTable = soup.find(id=regionStr)
        aTag = regionTable.findAll('a')
        for a in aTag:
            idIndex = a.string.find('=')
            resultDict[a.string] = {
                'id' : a['href'][idIndex+1:],
                'url' : a['href']
            }
    return resultDict

def mainFunc():
    print 'team,year,partname'
    getTeamDict("http://igem.org/Team_Parts?year=2010")

if __name__ == '__main__':
    django.setup()
    mainFunc()