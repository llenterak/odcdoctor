from collections import namedtuple


User = namedtuple('User', ["name", "googleCloudId"])


class Users(object):
    def __init__(self):
        self.table = []

    def addUser(self, name, googleCloudId):
        self.table.append(User(name, googleCloudId))


    def getList(self):
        return self.table
    def removeUser(self, name):
        for user in self.table:
            if (user.name == name):
                self.table.remove(user)
