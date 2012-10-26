from django.conf import settings
from createsend import *

CreateSend.api_key = settings.API_KEY

cs = CreateSend()

library_client_id = ""

list_id = ""
lib_list = List(list_id)
details = lib_list.details()

print "list details:\n\n"
print details.__dict__
print "\n\n"

subscriber = Subscriber(list_id)
#, "test@test.com")
#print subscriber.__dict__
#print subscriber

#me = subscriber.get(list_id,email)
email = "test@test.com"
me = subscriber.get(list_id,email)

print "subscriber:\n\n"
print me.__dict__
print "\n\n"


