class Client(object):

    def __init__(self, name=None, newsletters=None):
        self.name = name
        self.newsletters = newsletters

class Subscriber(object):

    def __init__(self, state=False, email=None, date=None):
        self.state = state
        self.email = email
        self.date = date

class Newsletter(object):

    def __init__(self, title=None, listid=None):
        self.title = title
        self.listid = listid
        self.subscriber = Subscriber()


if __name__ == "__main__":

    s = Subscriber(True, "test@test.com", date=None)
    n = Newsletter("Test One", "1234567890")
    n.subscriber = s
    c = Client("ClientName", [n,])

    print c.name
    for n in c.newsletters:
        print n.title
        print n.listid
        print n.subscriber.state
        print n.subscriber.email
        print n.subscriber.date
