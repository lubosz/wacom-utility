# Xorg Modification utility
# Tested on Ubuntu Jaunty x86_64

from copy import copy
import os

def SetXorgConfig(value):
    CheckXorgConf()
    f1 = open("/etc/X11/xorg.conf", 'r')
    data = f1.readlines()
    f1.close()

    if value==0:		# Remove custom configuration
        exclusion = []	# Line numbers to exclude
        for item in data:
            exclusion.append(0)


        for i in range(0,len(data)):
            line = data[i]
            line = line.split("#")[0]	# Remove commenting from analysis
            if StdParse(line).count("section\"inputdevice\""):
                State = 0	# State triggers if it's a wacom configuration
                for subline in data[i+1:]:
                    if StdParse(subline).count("driver\"wacom\""):
                        State = 1
                    if StdParse(subline).count("endsection"):
                        break
                # If State = 1, mark all lines until next endsection
                if State == 1:
                    for j in range(i,len(data)):
                        subline = data[j]
                        exclusion[j] = 1
                        if StdParse(subline).count("endsection"):
                            break
            # Remove all entries from serverlayout
            if StdParse(line).count("section\"serverlayout\""):
                for device in CheckXorgConfig()[1]:
                    for j in range(i+1,len(data)):
                        subline = data[j]
                        if StdParse(subline).count("endsection"):
                            break
                        if StdParse(subline).count("inputdevice\""+device+"\""):
                            exclusion[j] = 1
            # Compile the new file
            newdata = []
            for i in range(0,len(data)):
                if exclusion[i]==0:
                    newdata.append(data[i])
    elif value==1:
        newdata = copy(data)
        hasserverlayout = 0
        for i in range(0,len(data)):
            line = data[i]
            line = line.split("#")[0]	# Remove commenting from analysis
            if StdParse(line).count("section\"serverlayout\""):
                hasserverlayout = 1
                q = 0
                for item in GetSLData():
                    newdata.insert(i+1+q,item+"\n")
                    q = q + 1
                break
        for item in GetIDData():
            newdata.append(item+"\n")
        if hasserverlayout == 0:
            newdata.append("Section \"ServerLayout\"\n")
            newdata.append("Identifier \"Default Layout\"\n")
            for item in GetSLData():
                newdata.append(item+"\n")
            newdata.append("EndSection\n")


    # Write the new file to a temporary directory
    f1 = open("/tmp/xorg.conf", 'w')
    f1.writelines(newdata)
    f1.close()
    # Backup
    os.system("cp /etc/X11/xorg.conf ~/.xorg_wacom_utility_backup")
    # Copy
    os.system("gksu cp /tmp/xorg.conf /etc/X11/xorg.conf")



def CheckXorgConfig():
    # Checks for existance of a section using wacom driver
    # Does not check validity of configuration
    State = 0	# 0=Unconfigured 1=Configured 2=Broken
    Devices = []
    CheckXorgConf()
    f1 = open("/etc/X11/xorg.conf", 'r')
    data = f1.readlines()
    f1.close()
    for i in range(0,len(data)):
        line = data[i]
        line = line.split("#")[0]	# Remove commenting
        if StdParse(line).count("section\"inputdevice\""):
            for subline in data[i+1:]:
                if StdParse(subline).count("endsection"):
                    break
                if StdParse(subline).count("driver\"wacom\""):
                    State = 1
                if StdParse(subline).count("option\"type\""):
                    Devices.append(StdParse(subline).split("\"")[-2])
    if State == 1:	# Check for presence of all listed devices in serverlayout section
        for i in range(0,len(data)):
            line = data[i]
            line = line.split("#")[0]	# Remove commenting
            if StdParse(line).count("section\"serverlayout\""):
                for device in Devices:
                    Ok = 0
                    for subline in data[i+1:]:
                        if StdParse(subline).count("endsection"):
                            break
                        if StdParse(subline).count("inputdevice\""+device+"\""):
                            Ok = 1
                    if Ok == 0:
                        State = 2


    return State,Devices

def StdParse(line):	# Format with no spaces, tabs, and double quotes only
    return line.replace(" ","").replace("\t","").replace("\'","\"").replace("\n","").lower()

def CheckXorgConf():
    # If xorg.conf doesn't exist, create blank template
    # Distros such as Fedora 10 do not come with xorg.conf created
    try:
        os.stat("/etc/X11/xorg.conf")
    except:
        newdata = ["Section \"ServerLayout\"\n","EndSection"]
        f1 = open("/tmp/xorg.conf", 'w')
        f1.writelines(newdata)
        f1.close()
        # Copy
        os.system("gksu cp /tmp/xorg.conf /etc/X11/xorg.conf")

def GetSLData():
    return ["\tInputDevice   \"stylus\"  \"SendCoreEvents\"",\
        "\tInputDevice   \"eraser\"  \"SendCoreEvents\"",\
        "\tInputDevice   \"cursor\"  \"SendCoreEvents\"\t# For non-LCD tablets only",\
        "\tInputDevice   \"pad\"  \"SendCoreEvents\"\t# For Intuos3/CintiqV5/Graphire4/Bamboo tablets"]

def GetIDData():
    data = """Section "InputDevice"
    Driver        "wacom"
    Identifier    "stylus"
    Option        "Device"        "/dev/input/wacom" # USB ONLY?
    Option        "Type"          "stylus"
    Option        "USB"           "on"               # USB ONLY
EndSection

Section "InputDevice"
    Driver        "wacom"
    Identifier    "eraser"
    Option        "Device"        "/dev/input/wacom" # USB ONLY?
    Option        "Type"          "eraser"
    Option        "USB"           "on"               # USB ONLY
EndSection

Section "InputDevice"
    Driver        "wacom"
    Identifier    "cursor"
    Option        "Device"        "/dev/input/wacom" # USB ONLY?
    Option        "Type"          "cursor"
    Option        "USB"           "on"               # USB ONLY
EndSection

Section "InputDevice"
    Driver        "wacom"
    Identifier    "pad"
    Option        "Device"        "/dev/input/wacom"    # USB ONLY
    Option        "Type"          "pad"
    Option        "USB"           "on"                  # USB ONLY
EndSection"""
    return data.split("\n")
