from django.conf import settings
from createsend import *

CreateSend.api_key = settings.API_KEY

cs = CreateSend()
clients = cs.clients()

for c in clients:
    print "%s: %s" % (c.ClientID, c.Name)
