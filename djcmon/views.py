from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.urlresolvers import reverse

from djtools.utils.mail import send_mail

from djcmon import Department, Contact, Newsletter
from djcmon.forms import ManagerForm

from createsend import *

import base64, os, datetime

NOW = str(datetime.datetime.now().strftime("%m/%d/%Y"))
YEAR = int(datetime.datetime.now().strftime("%Y"))
MONTH = int(datetime.datetime.now().strftime("%m"))
FEMAIL = settings.DEFAULT_FROM_EMAIL

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def subscription(request,action):
    """
    subscribe or unsubscribe a contact to a newsletter via ajax POST or GET.
    POST/GET data:
        list id
        email
    returns response message for display to user
    """
    # we will need GET for email confirmations
    if request.POST:
        lid = request.POST["lid"]
        email = request.POST["email"]
    elif request.GET:
        lid = request.GET["lid"]
        email = request.GET["email"]
        #action = request.GET.get('action')
    else:
        return HttpResponseRedirect(reverse("newsletters_home"))
    CreateSend.api_key = settings.API_KEY
    subscriber = Subscriber(lid, email)
    list = List(lid)
    # action
    if action == "unsubscribe":
        response = subscriber.unsubscribe()
    elif action == "subscribe":
        response = subscriber.add(lid, email, "", [], True)
    else:
        return HttpResponseRedirect(reverse("newsletters_home"))

    # send email confirmation
    subject = "%s request for Carthage Newsletter: %s" % (action.capitalize(),list.details().Title)
    template = "confirmation_email.html"

    for d in settings.DESCRIPTIONS:
        if d[0] == lid:
            desc = d[1]

    data = {'id':lid,'title':list.details().Title,'description':desc,'email':email,'action':action}
    send_mail(request, [email,], subject, FEMAIL, template, data)

    # check user status on lists
    sub = False
    count = 0
    client = Client(client_id=settings.CARTHAGE_CM_ID)
    for l in client.lists():
        list_obj = List(l.ListID)
        subscriber = Subscriber(l.ListID)
        try:
            me = subscriber.get(l.ListID,email)
            if me.State == "Active":
                sub = True
                count += 1
        except:
            pass

    # send notification if no lists or first list.
    # OJO: eventually this will go directly to CX
    if (action == "unsubscribe" and not sub) or (action == "subscribe" and count == 1):
        subject = "%s request: %s" % (action.capitalize(), email)
        template = "alert.html"
        data = {'email':email,'action':action,}
        send_mail(request, settings.EMAIL_NOTIFICATION, subject, FEMAIL, template, data)

    if request.POST:
        return render_to_response('ajax_response.html', {'response':response, }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse("newsletters_manager")+ "?email=%s" % email)

def manager(request):
    """
    accepts an email address and returns the client list of newsletters
    to which said email belongs

    OJO: can't use custom fields, only email.
    http://help.campaignmonitor.com/topic.aspx?t=86
    """
    if request.GET:
        email = request.GET['email']
        action = request.GET.get('action')
    elif request.POST:
        email = request.POST['email']
        action = "Manager"
    else:
        return HttpResponseRedirect(reverse("newsletters_home"))

    try:
        validate_email(email)
        valid_email = True
    except:
        valid_email = False

    if email and valid_email:
        contact = None
        # connect to API and retrieve clients
        CreateSend.api_key = settings.API_KEY
        cs = CreateSend()
        client = Client(client_id=settings.CARTHAGE_CM_ID)
        newsletters_pub = []
        #for l in client.lists():
        for l in settings.DESCRIPTIONS:
            lid = l[0]
            desc = l[1]
            #list_obj = List(l.ListID)
            list_obj = List(lid)
            subscriber = Subscriber(lid)
            try:
                me = subscriber.get(lid,email)
                subscriber = Contact(me.State, me.Name, me.EmailAddress, me.Date)
                contact = subscriber
            except:
                subscriber = None
            n = Newsletter(list_obj.details().Title, desc, lid)
            n.subscriber = subscriber
            newsletters_pub.append(n)

        return render_to_response(
            'manager.html', {
                'contact':contact, 'email':email, 'action':action,
                'newsletters_pub':newsletters_pub
            },
            context_instance=RequestContext(request)
        )
    else:
        form = ManagerForm()
        return render_to_response(
            'home.html',
            {'form': form,'email':email,'valid_email':valid_email},
            context_instance=RequestContext(request)
        )

def home(request):
    form = ManagerForm()
    return render_to_response(
        'home.html', {'form':form,'home':True},
        context_instance=RequestContext(request)
    )
