from django.conf import settings

from djcmon import Contact, Newsletter

from createsend import *

cs = CreateSend({'api_key': settings.API_KEY})

client = Client(client_id=settings.CARTHAGE_CM_ID, auth={'api_key': settings.API_KEY})

newsletters_pub = []

for l in settings.DESCRIPTIONS:
    lid = l[0]
    desc = l[1]

    #list_obj = List(list_id=lid, auth=client.auth)
    list_obj = List(list_id=lid, auth={'api_key': settings.API_KEY})

    #print("list title = {}".format(list_obj.details().Title))
    #print("list id = {}".format(l.ListID))
    #subscriber = Subscriber(list_id=lid, auth=client.auth)
    subscriber = Subscriber(list_id=lid, auth={'api_key': settings.API_KEY})
    me = subscriber.get(list_id=lid, email_address='eyoung@carthage.edu')
    subscriber = Contact(me.State,me.Name,me.EmailAddress,me.Date)
    contact = subscriber
    n = Newsletter(list_obj.details().Title, desc, lid)
    n.subscriber = subscriber
    newsletters_pub.append(n.__dict__)

"""
for l in client.lists:
    list_obj = List(l.ListID)
    subscriber = Subscriber(l.ListID)
    n = Newsletter(list_obj.details().Title, l.ListID)
    n.subscriber = subscriber
    newsletters.append(n)
"""
print newsletters_pub
