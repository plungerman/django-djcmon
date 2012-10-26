from django.conf import settings
from createsend import *

CreateSend.api_key = settings.API_KEY

cs = CreateSend()
clients = cs.clients()

email = "test@test.com"

client = Client(client_id=settings.CARTHAGE_CM_ID)
sub = False
count = 0
for l in client.lists():
    list_obj = List(l.ListID)
    print "list title = %s" % list_obj.details().Title
    subscriber = Subscriber(l.ListID)
    try:
        me = subscriber.get(l.ListID,email)
        print me.__dict__
        if me.State == "Active":
            sub = True
            count += 1
    except:
        pass

print "count = %s" % count
print "sub = %s" % sub
