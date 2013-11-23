from Tkinter import *

class I2C_emulator:
    def __init__(self):
        print "i2c emulator started"

class SPI_emulator:
    def __init__(self):
        print "spi emulator started"
class OneWire_emulator:
    def __init__(self):
        print "spi emulator started"

class DevCommunicator:
    def __init__(self):
        print "asd"



class User:
    def __init__(self, name, googleId):
        self.name = name
        self.googleId = googleId

class Users:
    def __init__(self):
        table = []
    def addUser(self, name, googleId):
        self.table.append(User(name, googleId))
    def removeUser(self, name):
        for user in self.table:
            if (user.name == name):
                self.table.remove(user)
    

class Device:
    def __init__(self, name, dev_type, dev_default_status = "off"):
        self.name = name;
        self.dev_type = dev_type;
        self.status = dev_default_status
    def printData(self):
        print self.name, ":", self.dev_type;


class DeviceList:
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



class App:

    def initDeviceButtons(self):
        i = 0
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for dev in self.devs.getList():
            i += 1
            if (dev.status == "off"):
                col = "green"
            else:
                col = "red"
            self.buttons.append(Button(self.frame, text = dev.name, fg=col, command = lambda it = i: self.toggleButton(it - 1)))
        for button in self.buttons:
            print "110"
            button.pack(side=LEFT)
    
    def toggleButton(self, number):
#        self.buttons[number].config(fg = "blue")
        st = self.devs.getitem(number).status
        if (st == "on"):
            self.devs.getitem(number).status = "off";
        else:
            self.devs.getitem(number).status = "on";
        self.initDeviceButtons()
        print("fail", number)
                
    def __init__(self, master):
        self.buttons = []
        self.innerMap = {}
        self.frame = Frame(master)
        self.frame.pack()
        self.devs = DeviceList()

        self.devs.addDevice("holodilinik", "device")
        self.devs.addDevice("door", "lock");
        self.devs.addDevice("mashinka", "device");

        self.devs.printDeviceList()
        self.initStaticButtons()
        self.initDeviceButtons()
    
    def addDeviceDialog(self):
        d = MyDialog_dev(root)
        if (d.result != None):    
            self.devs.addDevice(d.result['name'], d.result['type'])
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
        self.addDeviceButton = Button(self.frame, text="add device", command=self.addDeviceDialog)
        self.addDeviceButton.pack(side=BOTTOM)
    
    def say_hi(self):
        print "hi there, everyone!"



import tkSimpleDialog

class MyDialog_dev(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="name").grid(row=0)
        Label(master, text="type").grid(row=1)

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
        self.result["type"] = second;
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




root = Tk()
app = App(root)
root.mainloop()
#root.destroy() # optional; see description below
