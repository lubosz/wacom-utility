# xsetwacom interface
import os
from copy import copy
from tablet_capplet import GetPressCurve, GetClickForce


class XSetWacom:
    def listInterfaces(self):
        # List all input devices
        devlist = os.popen("xsetwacom --list devices").readlines()
        devices = []
        for device in devlist:
            devices.append(device.split("id:")[0].strip())
        return devices

    def listModifiers(self):
        # List all modification key commands
        data = open("keymap.txt", "r").readlines()
        ret = []
        for item in data:
            if item[0] != "#" and item[0] != "" and item[0] != "\n":
                ret.append([item.split("\t")[0],"".join(item.split("\t")[1:]).replace("\n","")])
        return ret

    def getConfiguration(self, device, function):
        data = os.popen("xsetwacom get '" + device + "' " + function).read()
        return data.replace("\n", "")

    def getTypeAndName(self, device, function):
        # 0 = Ign
        # 1 = Mouse
        # 2 = Key
        data = self.getConfiguration(device,function)
        if data == "0":
            return 0, "Ignore"
        elif data[0:8].upper() == "DBLCLICK":
            return 1, "Double Click"
        elif len(data) == 1 and int(data) > 0:
            return 1, self.lookUpMouseButton(int(data))
        else:
            return 2, data.replace("CORE KEY ", "")

    def lookUpMouseButton(self,button):
        if button == 1:
            return "Left Click"
        elif button == 2:
            return "Right Click"
        elif button == 3:
            return "Middle Click"
        elif button == 4:
            return "Scroll Wheel Up"
        elif button == 5:
            return "Scroll Wheel Down"
        else:
            return str(button)

    def lookUpMouseName(self,name):
        for item in self.listMouseActions():
            if item[1] == name:
                return item[0]
        return "0"

    def listMouseActions(self):
        return [["button 1","Left Click"],["button 2","Right Click"],["button 3","Middle Click"],["button 4","Scroll Wheel Up"],["button 5","Scroll Wheel Down"],["DBLCLICK 1","Double Click"]]

    def setByTypeAndName(self,device,type,object,name=""):
        # 0 = ign | 1 = Mouse | 2 = Keybd | 3 = TPCButton (name=on/off)

        if type == 0:
            function = "0"
        elif type == 1:
            function = "\'" + self.lookUpMouseName(name) + "\'"
        elif type == 2:
            function = "\"CORE KEY " + name + "\""
        elif type == 3:
            function = "\'TPCButton " + name + "\'"
        print ("xsetwacom set '" + device + "' " + object + " " + function)
        result = os.popen("xsetwacom set '" + device + "' " + object + " " + function).read()

    def verifyString(self,string):
        result = 1
        if string.count("\'") + string.count("\"") + string.count("\\") + string.count("\t") > 0:
            result = 0
        for item in string.split(" "):
            if len(item) > 1:
                ver = 0
                for litem in self.listModifiers():
                    if item.upper() == litem[0].upper():
                        ver = 1
                if ver == 0:
                    result = 0
        return result

    def saveToXSession(self, Tablet):
        # Saves configuration so it runs on startup
        self.purgeXSession()
        commands = []
        # Generate commands based on current configuration
        for interface in self.listInterfaces():
            if "pad" in interface.lower():
                for button in Tablet.Buttons:
                    result = os.popen("xsetwacom get '" + interface + "' " + button.Callsign).read()
                    result = result.replace("\n","")
                    if len(result) == 1:
                        result = self.lookUpMouseName(self.lookUpMouseButton(int(result)))
                    commands.append("xsetwacom set '" + interface + "' " + button.Callsign + " \"" + result + "\"\n")
            else:
                points = GetPressCurve(interface)
                if points:
                    commands.append("xsetwacom set '" + interface + "' PressureCurve " + str(points[0]) + " " + str(points[1]) + " " + str(points[2]) + " " + str(points[3]) + "\n")
                result = GetClickForce(interface)
                if result: commands.append("xsetwacom set '" + interface + "' Threshold " + str(result) + "\n")
        # Save configuration to .xsession
        f1 = open(os.path.expanduser("~/.wacom_utility"), 'a')
        f1.writelines(commands)
        f1.close()

    def purgeXSession(self):
        # Purges .wacom_utility file of any previous configuration
        try:
            os.stat(os.path.expanduser("~/.wacom_utility"))
        except:
            return
        f1 = open(os.path.expanduser("~/.wacom_utility"), 'r')
        data = f1.readlines()
        f1.close()
        newdata = copy(data)
        for line in data:
            if line[0:9] == "xsetwacom":
                newdata.remove(line)
        f2 = open(os.path.expanduser("~/.wacom_utility"), 'w')
        f2.writelines(newdata)
        f2.close()
