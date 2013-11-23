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
