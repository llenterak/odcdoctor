from collections import namedtuple


User = namedtuple('User', ["name", "googleCloudId"])


class Users(object):
    def __init__(self):
        table = []

    def addUser(self, name, googleCloudId):
        self.table.append(User(name, googleCloudId))

    def removeUser(self, name):
        for user in self.table:
            if (user.name == name):
                self.table.remove(user)
