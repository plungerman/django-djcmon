import base64
import datetime
import os

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from djtools.utils.mail import send_mail

from djcmon import Department, Contact, Newsletter
from djcmon.forms import ManagerForm

from createsend import *


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
        'id': lid,
        'title': list_obj.details().Title,
        'description': desc,
        'email': email,
        'action': action,
    }
    frum = settings.EMAIL_NOTIFICATION
    send_mail(
        request,
        [email],
        subject,
        frum,
        template,
        data,
        reply_to=[frum,],
    )

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
    if (action == 'unsubscribe' and not sub) or (
        action == 'subscribe' and count == 1):
        subject = '{0} request: {1}'.format(action.capitalize(), email)
        template = 'alert.html'
        send_mail(
            request,
            [frum,],
            subject,
            FEMAIL,
            template,
            data,
            reply_to=[email,],
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
        email = request.GET.get('email')
        action = request.GET.get('action')
        form = ManagerForm(use_required_attribute=False)
    elif request.POST:
        email = request.POST.get('email')
        action = 'Manager'
        form = ManagerForm(request.POST, use_required_attribute=False)
    else:
        return HttpResponseRedirect(reverse('newsletters_home'))

    try:
        validate_email(email)
        valid_email = True
    except:
        valid_email = False

    if email and valid_email or form.is_valid():
        contact = None
        newsletters_pub = []
        if True:
            #request.session['djcmon_data'] = form.cleaned_data
            request.session['djcmon_data'] = form.data
            # connect to API and retrieve clients
            cs = CreateSend({'api_key': settings.API_KEY})

            client = Client(
                client_id=settings.CARTHAGE_CM_ID,
                auth={'api_key': settings.API_KEY},
            )
            newsletters_pub = []
            for l in settings.DESCRIPTIONS:
                lid = l[0]
                desc = l[1]
                list_obj = List(list_id=lid, auth={'api_key': settings.API_KEY})
                subscriber = Subscriber(
                    list_id=lid, auth={'api_key': settings.API_KEY},
                )
                try:
                    me = subscriber.get(list_id=lid, email_address=email)
                    subscriber = Contact(me.State,me.Name,me.EmailAddress,me.Date)
                    contact = subscriber
                except Exception as error:
                    subscriber = None
                n = Newsletter(list_obj.details().Title, desc, lid)
                n.subscriber = subscriber
                newsletters_pub.append(n)

        return render(
            request, 'manager.html', {
                'contact': contact,
                'email': email,
                'action': action,
                'newsletters_pub': newsletters_pub,
            }
        )
    else:
        return render(
            request, 'base.html',
            {'form': form, 'email': email, 'valid_email': valid_email},
        )


def home(request):
    form = ManagerForm(use_required_attribute=False)
    return render(
        request, 'base.html', {'form':form, 'home':True,}
    )
