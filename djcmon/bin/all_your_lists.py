from django.conf import settings
from createsend import *

CreateSend.api_key = settings.API_KEY

cs = CreateSend()
clients = cs.clients()

email = "test@test.com"

for c in clients:
    print "%s: %s" % (c.ClientID, c.Name)
    client = Client(client_id=c.ClientID)
    lists = client.lists
    for l in lists():
        list_obj = List(l.ListID)
        print "list title = %s" % list_obj.details().Title
        subscriber = Subscriber(l.ListID)
        try:
            me = subscriber.get(l.ListID,email)
            # the following returns too much info
            #me = Subscriber(l.ListID,email)
            print "subscriber = %s" % subscriber.__dict__
            # unsubscribe
            # subscriber.unsubscribe()
        except:
            pass
        #print "fake web = %s" % subscriber.fake_web
        #if subscriber.fake_web:
        #    print "subscriber = %s" % subscriber.__dict__
        """
        if list_obj.active("2000-03-20").Results:
            for r in list_obj.active("2000-03-20").Results:
                print "name = %s" % r.Name
                print "email = %s" % r.EmailAddress
                print "date = %s" % r.Date
                print "state = %s" % r.State
        """
    print "\n"
