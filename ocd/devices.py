class Device(object):

    def __init__(self, name, dev_type, dev_default_status):
        self.name = name;
        self.dev_type = dev_type;
        self.status = dev_default_status
        self.defaultStatus = dev_default_status;        

    def printData(self):
        print self.name, ":", self.dev_type;


class DeviceList(object):
    def __init__(self):
        self.innerList = []

    def printDeviceList(self):
        for dev in self.innerList:
            dev.printData()

    def getList(self):
        return self.innerList

    def getitem(self, it):
        return self.innerList[it]

    def addDevice(self, name, type, defaultStatus = "off"):
        self.innerList.append(Device(name, type, defaultStatus))

    def removeDevice(self, name):
        for dev in self.innerList:
            if (dev.name == name):
                self.innerList.remove(dev)
# format:
# name, devtype, status -- all strings
# 
    def getDiseasedDevicesList(self):
        deadDevs = []
        for dev in self.innerList:
            if (dev.status != dev.defaultStatus):
                deadDevs.append(dev)
        return deadDevs
