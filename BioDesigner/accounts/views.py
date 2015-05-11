from accounts.models import User, UserSafety
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

# Create your views here.

def indexView(request):
    # check is allow auto login
    if (isAllowAutoLogin(request)):
        return HttpResponseRedirect('/home/dashboard')
    # render and return the page
    template = loader.get_template('accounts/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def isAllowAutoLogin(request):
    try:
        isAllowAutoLogin = request.session['isAllowAutoLogin']
        return isAllowAutoLogin
    except KeyError:
        return False

@csrf_exempt
def loginAction(request):
    """handle the login request

    handle the login request, validate and create session

    Args:
        request: the http request to be processed

    Returns: A http response which contains the json result
    """
    #get user inputs
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    isAutoLogin = request.POST.get('isAutoLogin', True)

    #the result to be returned
    results = {
            'isSuccessful': False,
            'isInfoEmpty': not username and not password,
            'isAccountValid': False,
    }

    # validation, create session and return result
    if not results['isInfoEmpty']:
        password = hashlib.sha1(password).hexdigest()
        results['isAccountValid'] = isAccountValid(username, password)
        results['isSuccessful'] = results['isAccountValid']
        if results['isSuccessful']:
            createSession(request, username, isAutoLogin)

    return HttpResponse(json.dumps(results), content_type="application/json")


def createSession(request, username, isAutoLogin):
    """create session for the user who has just logged index

    Args:
        request: the http request which contains session
        username: the username of the user who has just logged index
        isAutoLogin: whether the user allow auto login or not
    """

    request.session['isLoggedIn'] = True
    request.session['username'] = username
    request.session['isAutoLogin'] = isAutoLogin

def isAccountValid(username, password):
    try:
        User.objects.get(
            Q(username=username),
            Q(password=password)
        )
        return True
    except:
        return False

@csrf_exempt
def logoutAction(request):
    try:
        del request.session['isLoggedIn']
        del request.session['isAllowAutoLogin']
        del request.session['isAdministrator']
        del request.session['isReviewer']
    except:
        pass

    return HttpResponseRedirect('/accounts')

@csrf_exempt
def registerAction(request):
    """handle the register request

    handle the register request and send confirmation email

    Args:
        request: the http request
    Returns:
        return a http response which contents the result json that indicate the register reuslt
    """
    # get user inputs
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    print username
    print password
    print email
    result = {
            'isSuccessful': False,
            'errorMessage': '',
            'isInfoEmpty': not username and not password and not email,
    }

    #check whether the user or email exists
    if not isUserExists(username) and not isEmailExists(email) and not result['isInfoEmpty']:
        saveNewUser(username, password, email)
        result['isSuccessful'] = True
        createSession(request, username, False)
    return HttpResponse(json.dumps(result), content_type="application/json")

def saveNewUser(username, password, email):
    password = hashlib.sha1(password).hexdigest()
    newUser = User(username=username, password=password, email=email, is_confirmed=False)
    newUser.save()
    varifyEmail(email, newUser, username)

def varifyEmail(email, user, username):
    """email confirmation

    makesure the email is valid

    Args:
        email: the email to be confirmed
        user: the user of the email
    """
    # get active key with salt and email
    salt = hashlib.sha1(str(random.random())).hexdigest()[:10]
    active_key = hashlib.sha1(email+salt).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)

    # create new user safety
    newSafety = UserSafety(user_id=username, activation_key=active_key, key_expires=key_expires)
    newSafety.save()

    #send email with active key
    email_subject = 'BioDesigner Account confirmation'
    email_body = "Hello %s,\nThanks for your registeration.\nTo active you account \
    , please click this link within 48 hours\n\
    http://127.0.0.1:8000/accounts/confirm/%s" % (username, email)
    #send_mail(email_subject, email_body, 'BioDesigner@biodesigner.com',
     #[email],fail_silently=False)


def isUserExists(username):
    try:
        User.objects.get(username=username)
        return True
    except:
        return False

def isEmailExists(email):
    try:
        User.objects.get(email=email)
        return True
    except:
        return False

@csrf_exempt
def register_confirm(request, activation_key):
    """finish confirmation and active the account

    Args:
        request: the http request
        activation_key: the activation key
    Returns:
        Http redirect to successful page
    """
    user_safety = get_object_or_404(UserSafety, activation_key=activation_key)
    if user_safety.user.is_confirmed:
        return HttpResponseRedirect('/home/dashboard')
    if user_safety.key_expires < timezone.now():
        return render_to_response('accounts/confirmExpires.html')
    user = user_safety.user
    user.is_confirmed = True
    user.save()
    return render_to_response('accounts/confirmed.html')
