from django.conf import settings
from createsend import *

CreateSend.api_key = settings.API_KEY

cs = CreateSend()
clients = cs.clients()

newsletters = []
client = Client(client_id=settings.CLIENT_ID)
lists = client.lists
for l in lists():
    list_obj = List(l.ListID)
    print "list title = %s" % list_obj.details().Title
    print "list id = %s" % l.ListID
    subscriber = Subscriber(l.ListID)
    n = Newsletter(list_obj.details().Title, l.ListID)
    n.subscriber = subscriber
    newsletters.append(n)
"""
for l in client.lists:
    list_obj = List(l.ListID)
    subscriber = Subscriber(l.ListID)
    n = Newsletter(list_obj.details().Title, l.ListID)
    n.subscriber = subscriber
    newsletters.append(n)
"""
print newsletters
