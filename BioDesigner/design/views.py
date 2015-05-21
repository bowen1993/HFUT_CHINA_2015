from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json
import datetime
import random
from search_part import ambiguousSearch, getPart
from accounts.models import User
from design.models import project, functions, tracks, user_project

@csrf_exempt
def searchParts(request):
    keyword = request.GET.get('keyword')
    results = ambiguousSearch(keyword)
    return HttpResponse(json.dumps(results), content_type="application/json")

@csrf_exempt
def getParts(request):
    partName = request.GET.get('partname')
    results = getPart(partName)
    return HttpResponse(json.dumps(results), content_type="application/json")

@csrf_exempt
def dashboardView(request):
    try:
        isLoggedIn = request.session['isLoggedIn']
        isAccountConfirm = isAccountActive(request)
        if isLoggedIn and isAccountConfirm:
            template = loader.get_template('home/dashboard.html')
            context = RequestContext(request, {})
            return HttpResponse(template.render(context))
        else:
            return HttpResponseRedirect('/')
    except KeyError:
        return HttpResponseRedirect('/')

def isAccountActive(request):
    try:
        username = request.session['username']
        return User.objects.get(username=username).is_confirmed
    except KeyError:
        return False

def isLoggedIn(request):
    try:
        isLoggedIn = request.session['isLoggedIn']
        return isLoggedIn
    except KeyError:
        return False

def getCurrentUserObj(request):
    username = request.session['username']
    userObj = User.objects.get(username=username)
    return userObj

def newProject(name, user, function, track):
    try:
        projectObj = project(project_name=name, creator=user, function_id=function, track_id=track)
        projectObj.save()
        userPjctObj = user_project(user=user, project=projectObj)
        userPjctObj.save()
        return True
    except:
        return False

@csrf_exempt
def createProject(request):
    result = {
        'isSuccessful': False,
    }
    if not isLoggedIn(request):
        return result
    name = request.POST.get('name', '')
    userObj = getCurrentUserObj(request)
    function_id = int(request.POST.get('function', ''))
    track_id = int(request.POST.get('track', ''))
    result['isSuccessful'] = newProject(name, userObj, function_id, track_id)
    reuslt['project_name'] = name
    return HttpResponse(json.dumps(result), content_type="application/json")



