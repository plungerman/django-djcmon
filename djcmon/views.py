from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.urlresolvers import reverse

from djforms.core.views import send_mail
from djzbar.utils.informix import do_sql

from communications import Department, Contact, Newsletter
from communications.forms import ManagerForm

from createsend import *

import base64, os, datetime

NOW = str(datetime.datetime.now().strftime("%m/%d/%Y"))
YEAR = int(datetime.datetime.now().strftime("%Y"))
MONTH = int(datetime.datetime.now().strftime("%m"))
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
        lid = request.POST["lid"]
        email = request.POST["email"]
    elif request.GET:
        lid = request.GET["lid"]
        email = request.GET["email"]
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
    data = {'id':lid,'title':list.details().Title,'description':settings.DESCRIPTIONS[lid],'email':email,'action':action}
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
        recipients = ["lpiela@carthage.edu","mtokarz@carthage.edu",]
        send_mail(request, recipients, subject, FEMAIL, template, data)

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
    elif request.POST:
        email = request.POST['email']
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

        return render_to_response('manager.html', {'contact':contact, 'email':email, 'newsletters_pub':newsletters_pub, }, context_instance=RequestContext(request))
    else:
        form = ManagerForm()
        return render_to_response('home.html', {'form': form,'email':email,'valid_email':valid_email,}, context_instance=RequestContext(request))

def person_detail(email):
    """
    """

    try:
        validate_email(email)
        where = 'WHERE email_rec.line1 = "%s" ' % email
    except:
        return None

    sql = ( 'SELECT id_rec.id, profile_rec.priv_code, profile_rec.birth_date, '
            'job_rec.job_title, job_rec.title_rank, id_rec.firstname, '
            'id_rec.lastname, aname_rec.line1 as alt_name,id_rec.addr_line1, '
            'id_rec.addr_line2, id_rec.city, id_rec.st, id_rec.zip, '
            'id_rec.phone as homephone, aa_rec.line3 as office_location, '
            'aa_rec.phone, email_rec.line1 as email '
            'FROM id_rec '
            'LEFT JOIN profile_rec on id_rec.id = profile_rec.id '
            'LEFT JOIN aa_rec as aname_rec on '
                '(id_rec.id = aname_rec.id AND aname_rec.aa = "ANDR") '
            'LEFT JOIN aa_rec as email_rec on '
                '(id_rec.id = email_rec.id AND email_rec.aa = "EML1"), '
            'job_rec, pos_table, aa_rec '
            '%s '
            'AND job_rec.id = id_rec.id '
            'AND aa_rec.id = id_rec.id '
            'AND aa_rec.aa in ("EML1","SCHL") '
            'AND job_rec.tpos_no = pos_table.tpos_no '
            'AND job_rec.beg_date < "%s" '
            'AND (job_rec.end_date is null or job_rec.end_date > "%s") '
            'AND pos_table.active_date < "%s" '
            'AND (pos_table.inactive_date is null '
                'OR pos_table.inactive_date > "%s") '
            'ORDER BY job_rec.title_rank' % (where,NOW,NOW,NOW,NOW) )

    objects = do_sql(sql)
    person = ''
    for obj in objects:
        person = obj
    if person:
        return person
    else:
        return None

def home(request):
    form = ManagerForm()
    return render_to_response('home.html', {'form':form,'home':True, }, context_instance=RequestContext(request))
