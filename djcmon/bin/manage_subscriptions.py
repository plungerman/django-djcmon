from django.conf import settings
from createsend import *

CreateSend.api_key = settings.API_KEY

cs = CreateSend()
clients = cs.clients()

email = "test@test.com"

#print "%s: %s" % (c.ClientID, c.Name)
#client = Client(client_id=c.ClientID)
client = Client(client_id=settings.CLIENT_ID)
lists = client.lists
for l in lists():
    list_obj = List(l.ListID)
    print "list title = %s" % list_obj.details().Title
    print "list id = %s" % l.ListID
    subscriber = Subscriber(l.ListID)
"""
        try:
            me = subscriber.get(l.ListID,email)
            # the following returns too much info
            #me = Subscriber(l.ListID,email)
            print "subscriber list = %s" % subscriber.list_id
            #print "subscriber = %s" % subscriber.__dict__
            # {'fake_web': False, 'email_address': None, 'list_id': u'listidhash'}
            #print "subscriber = %s" % me.__dict__
            print "subscriber state = %s" % me.State
            print "subscriber email = %s" % me.EmailAddress
            #{'__module__': 'createsend.utils', u'Name': u'', '__dict__': <attribute '__dict__' of 'CreateSendModel' objects>, u'State': u'Active', u'EmailAddress': u'test@test.com', u'Date': u'2010-02-17 15:13:00', u'CustomFields': [<class 'createsend.utils.CreateSendModel'>, <class 'createsend.utils.CreateSendModel'>, <class 'createsend.utils.CreateSendModel'>], '__weakref__': <attribute '__weakref__' of 'CreateSendModel' objects>, '__doc__': None}

            # unsubscribe
            # subscriber.unsubscribe()
        except:
            pass
            #email_address = subscriber.add(l.ListID, email, "Subscriber", [], True)
            #self.assertEquals(email_address, "subscriber@example.com")

        #print "fake web = %s" % subscriber.fake_web
        #if subscriber.fake_web:
        #    print "subscriber = %s" % subscriber.__dict__
        if list_obj.active("2000-03-20").Results:
            for r in list_obj.active("2000-03-20").Results:
                print "name = %s" % r.Name
                print "email = %s" % r.EmailAddress
                print "date = %s" % r.Date
                print "state = %s" % r.State
        print "\n"
"""
