import os
import django
import sys
import xml.sax
import datetime
from BeautifulSoup import BeautifulSoup
import urllib2

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import teams, functions, tracks

regionList = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_North America']

def getTeamDict(baseURL):
    print 'get html doc'
    result = dict()
    req = urllib2.Request(baseURL)
    response = urllib2.urlopen(req)
    htmlStr = response.read()
    print 'geting wiki url'
    teamDict = analyseHTMLPage(htmlStr)
    for key in teamDict:
        print 'writing team: ' + key
        #if os.path.exists('./team/' + key + '.txt'):
        #    print 'passing: ' + key
        #    continue
        track = getTeamAbstruct(teamDict[key])
        if 'not been assigned' in track:
            track = 'none'
        else:
            track = track[19:-4]
        newTrack = tracks.objects.get_or_create(track=track)
        newTeam = teams(name=key, track=newTrack)
        newTeam.save()
    return result

def analyseHTMLPage(htmlStr):
    resultDict = dict()
    soup = BeautifulSoup(htmlStr)
    for regionStr in regionList:
        regionTable = soup.find(id=regionStr)
        aTag = regionTable.findAll('a')
        for a in aTag:
            resultDict[a.string] = a['href']
    return resultDict

def getTeamAbstruct(wikiURL):
    req = urllib2.Request(wikiURL)
    cookieStr = 'team_ID=' + wikiURL[len(wikiURL)-4:len(wikiURL)]
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Cookie', cookieStr)
    print cookieStr
    response = urllib2.urlopen(req)
    htmlStr = response.read()
    soup = BeautifulSoup(htmlStr)
    #get track
    #print soup
    trackTable = soup.find(id='table_tracks')
    abstractTr = str(trackTable.find('tr').td.contents)

    return abstractTr

if __name__ == '__main__':
    django.setup()
    getTeamDict('http://igem.org/Team_List?year=2013')