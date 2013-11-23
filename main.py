import logging

import tkSimpleDialog
from Tkinter import *
from tooltip import *


class I2C_emulator(object):
    def __init__(self):
        logging.info("i2c emulator started")


class SPI_emulator(object):
    def __init__(self):
        print "spi emulator started"


class OneWire_emulator(object):
    def __init__(self):
        print "spi emulator started"


class DevCommunicator(object):

    def __init__(self):
        self.innerMap = {}
        self.innerMap['fridge'] = "fridgeHandler"
        self.innerMap['door'] = "doorHandler"
        self.innerMap['clothing iron'] = "ironHandler"


    def fridgeHandler(self, message): 
        if (message == "turn off"):
            return "fridge turned off"
        if (message == "turn on"):
            return "fridge turned on"
        else:
            return "unknown message to fridge"

    def doorHandler(self, message):
        if (message == "unlock"):
            return "door unlocked"
        if (message == "lock"):
            return "door locked"
        else:
            return "unknown message to door"

    def ironHandler(self, message):
        if (message == "turn off"):
            return "clothing iron turned off"
        if (message == "turn on"):
            return "clothing iron turned on. Why would you do that remotely? 0_o"
        else:
            return "unknown message to clothing iron"
    
    def askDevice(self, deviceName, message):
        try:
            print getattr(self,self.innerMap[str(deviceName)])(message)
        except(KeyError):
            print("Device not bound to Raspberry hub!");


class User(object):
    def __init__(self, name, googleCloudId):
        self.name = name
        self.googleCloudId = googleCloudId


class Users(object):
    def __init__(self):
        table = []

    def addUser(self, name, googleCloudId):
        self.table.append(User(name, googleCloudId))

    def removeUser(self, name):
        for user in self.table:
            if (user.name == name):
                self.table.remove(user)


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


class App(object):
    def __init__(self, master):
        self.buttons = []
        self.innerMap = {}
        self.frame = Frame(master)
        self.frame.pack()
        self.devs = DeviceList()

        self.devs.addDevice("fridge", "device", "on")
        self.devs.addDevice("door", "lock", "locked");
        self.devs.addDevice("clothing iron", "device", "off");

        self.devs.printDeviceList()
        self.initStaticButtons()
        self.initDeviceButtons()
        self.devc = DevCommunicator()

    def initDeviceButtons(self):
        i = 0
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for dev in self.devs.getList():
            i += 1
            if (dev.status == dev.defaultStatus):
                col = "green"
            else:
                col = "red"
            b = Button(self.frame, text = dev.name, fg=col, command = lambda it = i: self.toggleButton(it - 1))
            b.pack(side=LEFT)
            self.buttons.append(b)
            t1 = ToolTip(b, follow_mouse=1, text=dev.status)
#        for button in self.buttons:
#            print "110"
 #            button.pack(side=LEFT)

    def toggleButton(self, number):
        dev = self.devs.getitem(number)
        if (dev.status != dev.defaultStatus):
            dev.status = dev.defaultStatus;
        else:
            dev.status = "alternateStatus";
        print dev.name
        self.devc.askDevice(str(dev.name), "toggle")
        self.initDeviceButtons()
        print("fail", number)
                
    
    
    def addDeviceDialog(self):
        d = MyDialog_dev(root)
        if (d.result != None):    
            self.devs.addDevice(d.result['name'], d.result['type'], d.result['default'])
            self.initDeviceButtons()
            
        print "invoked addDevDialog"

    def addUserDialog(self):
        d = MyDialog_user(root)
        if (d.result != None):    
            self.devs.addUser(d.result['name'], d.result['id'])
        print "invoked addDevDialog"
                
    def initStaticButtons(self):
        self.addUserButton = Button(self.frame, text="add user", command=self.addUserDialog)
        self.addUserButton.pack(side=BOTTOM)
        b = Button(self.frame, text="add device", command=self.addDeviceDialog)
        self.addDeviceButton = b
        self.addDeviceButton.pack(side=BOTTOM)

    def say_hi(self):
        print "hi there, everyone!"





class MyDialog_dev(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="name").grid(row=0)
        Label(master, text="type").grid(row=1)
        Label(master, text="default").grid(row=2)


        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)        
        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        third = self.e3.get()
        self.result = {}
        self.result["name"] = first;
        self.result["type"] = second;
        self.result["default"] = second;
        #print first, second # or something

class MyDialog_user(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="name").grid(row=0)
        Label(master, text="google id").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        self.result = {}
        self.result["name"] = first;
        self.result["id"] = second;
        #print first, second # or something



if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
    #root.destroy() # optional; see description below
