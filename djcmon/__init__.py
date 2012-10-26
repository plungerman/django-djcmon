"""
object containers to hold API data
"""

class Department(object):

    def __init__(self, name=None, newsletters=None):
        self.name = name
        self.newsletters = newsletters

class Contact(object):

    def __init__(self, state=False, name=None, email=None, date=None):
        self.state = state
        self.name = name
        self.email = email
        self.date = date

class Newsletter(object):

    def __init__(self, title=None, description=None, listid=None):
        self.title = title
        self.description = description
        self.listid = listid
        self.subscriber = Contact()

