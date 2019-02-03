from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from djtools.utils.mail import send_mail

from djcmon import Department, Contact, Newsletter
from djcmon.forms import ManagerForm

from createsend import *

import base64, os, datetime

NOW = str(datetime.datetime.now().strftime('%m/%d/%Y'))
YEAR = int(datetime.datetime.now().strftime('%Y'))
MONTH = int(datetime.datetime.now().strftime('%m'))
FEMAIL = settings.DEFAULT_FROM_EMAIL

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
        lid = request.POST['lid']
        email = request.POST['email']
    elif request.GET:
        lid = request.GET['lid']
        email = request.GET['email']
        #action = request.GET.get('action')
    else:
        return HttpResponseRedirect(
            reverse('newsletters_home')
        )
    cs = CreateSend({'api_key': settings.API_KEY})
    subscriber = Subscriber(
        list_id=lid, email_address=email, auth={'api_key': settings.API_KEY}
    )
    list_obj = List(list_id=lid, auth={'api_key': settings.API_KEY})
    # action
    if action == 'unsubscribe':
        response = subscriber.unsubscribe()
    elif action == 'subscribe':
        response = subscriber.add(lid, email, '', [], True, 'unchanged')
    else:
        return HttpResponseRedirect(
            reverse('newsletters_home')
        )

    # send email confirmation
    subject = '{} request for Carthage Newsletter: {}'.format(
        action.capitalize(),list_obj.details().Title
    )
    template = 'confirmation_email.html'

    for d in settings.DESCRIPTIONS:
        if d[0] == lid:
            desc = d[1]

    data = {
        'id':lid,'title':list_obj.details().Title,
        'description':desc,'email':email,'action':action
    }
    send_mail(request, [email,], subject, FEMAIL, template, data)

    # check user status on lists
    sub = False
    count = 0
    client = Client(
        client_id=settings.CARTHAGE_CM_ID, auth={'api_key': settings.API_KEY}
    )
    for l in client.lists():
        list_obj = List(list_id=l.ListID, auth={'api_key': settings.API_KEY})
        subscriber = Subscriber(
            list_id=l.ListID, auth={'api_key': settings.API_KEY}
        )
        try:
            me = subscriber.get(list_id=l.ListID, email_address=email)
            if me.State == 'Active':
                sub = True
                count += 1
        except:
            pass

    # send notification if no lists or first list.
    # OJO: eventually this will go directly to CX
    if (action == 'unsubscribe' and not sub) or (
        action == 'subscribe' and count == 1):
        subject = '{} request: {}'.format(action.capitalize(), email)
        template = 'alert.html'
        data = {'email':email,'action':action,}
        send_mail(
            request, settings.EMAIL_NOTIFICATION, subject,
            FEMAIL, template, data
        )

    if request.POST:
        return render(
            request, 'ajax_response.html',
            {'response':response, }
        )
    else:
        return HttpResponseRedirect(
            reverse('newsletters_manager') + '?email={}'.format(email)
        )


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
        action = 'Manager'
    else:
        return HttpResponseRedirect(reverse('newsletters_home'))

    try:
        validate_email(email)
        valid_email = True
    except:
        valid_email = False

    if email and valid_email:
        contact = None
        # connect to API and retrieve clients
        cs = CreateSend({'api_key': settings.API_KEY})

        client = Client(
            client_id=settings.CARTHAGE_CM_ID, auth={'api_key': settings.API_KEY}
        )
        newsletters_pub = []
        for l in settings.DESCRIPTIONS:
            lid = l[0]
            desc = l[1]
            list_obj = List(list_id=lid, auth={'api_key': settings.API_KEY})
            subscriber = Subscriber(
                list_id=lid, auth={'api_key': settings.API_KEY}
            )
            try:
                me = subscriber.get(list_id=lid, email_address=email)
                subscriber = Contact(me.State,me.Name,me.EmailAddress,me.Date)
                contact = subscriber
            except:
                subscriber = None
            n = Newsletter(list_obj.details().Title, desc, lid)
            n.subscriber = subscriber
            newsletters_pub.append(n)

        return render(
            request, 'manager.html', {
                'contact':contact, 'email':email, 'action':action,
                'newsletters_pub':newsletters_pub
            }
        )
    else:
        form = ManagerForm()
        return render(
            request, 'home.html',
            {'form': form,'email':email,'valid_email':valid_email}
        )

def home(request):
    form = ManagerForm()
    return render(
        request, 'home.html', {'form':form,'home':True}
    )

'''
# broken as of django 1.9
@login_required
def saml_test(request):
    form = ManagerForm()
    return render(
        request, 'saml_test.html'
    )
'''
