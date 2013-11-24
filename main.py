import json
import logging
import threading

import tkSimpleDialog
from Tkinter import *
# from RepeatingTimer import *
from time import sleep
from tooltip import *


from ocd.devices import Device, DeviceList
from ocd.communicator import DevCommunicator
from ocd.user import Users
from ocd.notification import PostNotification


class App(object):
    
    def __init__(self, master):
        self.buttons = []
        self.innerMap = {}
        self.frame = Frame(master)
        self.frame.pack()
        self.devs = DeviceList()
        self.timer = threading.Timer(1, self.refresh_vals, args=[""])
        self.timer.start()
        self.devs.addDevice("fridge", "device", "on")
        self.devs.addDevice("door", "lock", "locked");
        self.devs.addDevice("clothing iron", "device", "off");
        self.users = Users()
        self.users.addUser("Tolea", "tolean777@gmail.com")
        self.devs.printDeviceList()
        self.initStaticButtons()
        self.initDeviceButtons()
        self.devc = DevCommunicator()
        self.notification = PostNotification("http://ocdoctor.herokuapp.com/notification")

    def sendMessageToUser(self, devname, status, user):
        payload = {"device_name": devname, "status": status}
        self.notification.send(payload)
        print "sending message to user: " + user.name + " that " + devname + " is " + status #!
        self.initDeviceButtons()

    def sendUrgentMessage(self, devname, status):
        for user in self.users.getList():
            self.sendMessageToUser(devname, status, user)

    def refresh_vals(self, message):
        try:
            f = open('ocd/values.txt', 'r')
            for line_raw in f:
                
                line = line_raw.rstrip()
                print line
                devname =  line[:line.find(':')]
                status = line[line.find(':') + 1:]
                for dev in self.devs.getList():
                    #print devname
                    if (dev.name == devname):
                        if (dev.status != status):   #status has changed and we just learnt 
                            dev.status = status
                            self.sendUrgentMessage(devname, status)
            f.close()
            
        except(IOError):
            print "no input file"
        self.timer = threading.Timer(1, self.refresh_vals, args=[""])
        print threading.active_count()
        if (self != None):
            self.timer.start()

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
            b = Button(self.frame, text = dev.name, bg=col, command = lambda it = i: self.toggleButton(it - 1))
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
        self.devc.askDevice(dev, "toggle")
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
        Label(master, text="interface").grid(row=3)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)        
        self.e4.grid(row=3, column=1)
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
    root.destroy() # optional; see description below
