from django.conf import settings
from createsend import *

CreateSend.api_key = settings.API_KEY

cs = CreateSend()
clients = cs.clients()

for c in clients:
    print "%s: %s" % (c.ClientID, c.Name)
    client = Client(client_id=c.ClientID)
    lists = client.lists
    for l in lists():
        #print "list = %s" % list_obj
        #print "list = %s" % l.__dict__
        #print "list name = %s" % l.Name
        #print "list id = %s" % l.ListID
        list_obj = List(l.ListID)
        print "list title = %s" % list_obj.details().Title
        print "list id= %s" % list_obj.details().ListID
        print "list ConfirmedOptIn = %s" % list_obj.details().ConfirmedOptIn
        print "list unsubscribe page = %s" % list_obj.details().UnsubscribePage
        print "list confirmation success page = %s" % list_obj.details().ConfirmationSuccessPage
        '''
        active() values:
        "Results": [{}]
        "ResultsOrderedBy": "email",
        "OrderDirection": "asc",
        "PageNumber": 1,
        "PageSize": 1000,
        "RecordsOnThisPage": 5,
        "TotalNumberOfRecords": 5,
        "NumberOfPages": 1
        if list_obj.active("2000-03-20").Results:
            for r in list_obj.active("2000-03-20").Results:
                print "name = %s" % r.Name
                print "email = %s" % r.EmailAddress
                print "date = %s" % r.Date
                print "state = %s" % r.State
                print "custom fields = %s" % r.CustomFields
                """
                looks like we store the student/staff ID for some lists
                """
                if r.CustomFields:
                    for f in r.CustomFields:
                        print "custom fields: %s, %s" % (f.Key, f.Value)
        '''
        print "\n"
