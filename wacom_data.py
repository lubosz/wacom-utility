# Loads settings on various models of tablets
import xml.dom.minidom


class TabletIdentities:
    def __init__(self):
        self.Tablets = []
        self.Tablets.append(Tablet("MODEL_PP_0405", "Wacom PenPartner", 0x00))
        self.Tablets.append(Tablet("ET_0405", "Wacom Graphire", 0x10))
        self.Tablets.append(Tablet("ET_0405", "Wacom Graphire2 4x5", 0x11))
        self.Tablets.append(Tablet("ET_0507", "Wacom Graphire2 5x7", 0x12))
        self.Tablets.append(Tablet("ET_0405", "Wacom Graphire3 4x5", 0x13))
        self.Tablets.append(Tablet("ET_0608", "Wacom Graphire3 6x8", 0x14))
        self.Tablets.append(Tablet("CTE_440", "Wacom Graphire4 4x5", 0x15))
        self.Tablets.append(Tablet("CTE_640", "Wacom Graphire4 6x8", 0x16))
        self.Tablets.append(Tablet("GD_0405-U", "Wacom Intuos 4x5", 0x20))
        self.Tablets.append(Tablet("GD_0608-U", "Wacom Intuos 6x8", 0x21))
        self.Tablets.append(Tablet("GD_0912-U", "Wacom Intuos 9x12", 0x22))
        self.Tablets.append(Tablet("GD_1212-U", "Wacom Intuos 12x12", 0x23))
        self.Tablets.append(Tablet("GD_1218-U", "Wacom Intuos 12x18", 0x24))
        self.Tablets.append(Tablet("MODEL_PL400",   "Wacom PL400", 0x30))
        self.Tablets.append(Tablet("MODEL_PL500",   "Wacom PL500", 0x31))
        self.Tablets.append(Tablet("MODEL_PL600",   "Wacom PL600", 0x32))
        self.Tablets.append(Tablet("MODEL_PL600SX", "Wacom PL600SX", 0x33))
        self.Tablets.append(Tablet("MODEL_PL550",   "Wacom PL550", 0x34))
        self.Tablets.append(Tablet("MODEL_PL800",   "Wacom PL800", 0x35))
        self.Tablets.append(Tablet("MODEL_PL700",   "Wacom PL700", 0x37))
        self.Tablets.append(Tablet("MODEL_PL510",   "Wacom PL510", 0x38))
        self.Tablets.append(Tablet("MODEL_DTU710",  "Wacom PL710", 0x39))
        self.Tablets.append(Tablet("MODEL_DTF720",  "Wacom DTF720", 0xC0))
        self.Tablets.append(Tablet("MODEL_DTF521",  "Wacom DTF521", 0xC4))
        self.Tablets.append(Tablet("MODEL_DTU1931", "Wacom DTU1931", 0xC7))
        self.Tablets.append(Tablet("XD-0405-U", "Wacom Intuos2 4x5", 0x41))
        self.Tablets.append(Tablet("XD-0608-U", "Wacom Intuos2 6x8", 0x42))
        self.Tablets.append(Tablet("XD-0912-U", "Wacom Intuos2 9x12", 0x43))
        self.Tablets.append(Tablet("XD-1212-U", "Wacom Intuos2 12x12", 0x44 ))
        self.Tablets.append(Tablet("XD-1218-U", "Wacom Intuos2 12x18", 0x45))
        self.Tablets.append(Tablet("XD-0608-U", "Wacom Intuos2 6x8", 0x47))
        self.Tablets.append(Tablet("MODEL-VOL", "Wacom Volito", 0x60))
        self.Tablets.append(Tablet("FT-0203-U", "Wacom PenStation", 0x61))
        self.Tablets.append(Tablet("CTF-420-U", "Wacom Volito2 4x5", 0x62))
        self.Tablets.append(Tablet("CTF-220-U", "Wacom Volito2 2x3", 0x63))
        self.Tablets.append(Tablet("CTF-421-U", "Wacom PenPartner2", 0x64))
        self.Tablets.append(Tablet("CTF_430-U", "Wacom Bamboo1", 0x69))
        self.Tablets.append(Tablet("MTE_450", "Wacom Bamboo", 0x65))
        self.Tablets.append(Tablet("CTE_450", "Wacom BambooFun 4x5", 0x17))
        self.Tablets.append(Tablet("CTE_650", "Wacom BambooFun 6x8", 0x18))
        self.Tablets.append(Tablet("CTE_631", "Wacom Bamboo1 Medium", 0x19))
        self.Tablets.append(Tablet("PTU-600", "Wacom Cintiq Partner", 0x03))
        self.Tablets.append(Tablet("TPC-090", "Wacom Tablet PC90", 0x90))
        self.Tablets.append(Tablet("TPC-093", "Wacom Tablet PC93", 0x93))
        self.Tablets.append(Tablet("TPC-09A", "Wacom Tablet PC9A", 0x9A))
        self.Tablets.append(Tablet("DTZ-21ux",  "Wacom Cintiq21UX", 0x3F))
        self.Tablets.append(Tablet("DTZ-20wsx", "Wacom Cintiq20WSX", 0xC5))
        self.Tablets.append(Tablet("DTZ-12wx",  "Wacom Cintiq12WX", 0xC6))
        self.Tablets.append(Tablet("PTZ-430",   "Wacom Intuos3 4x5", 0xB0))
        self.Tablets.append(Tablet("PTZ-630",   "Wacom Intuos3 6x8", 0xB1))
        self.Tablets.append(Tablet("PTZ-930",   "Wacom Intuos3 9x12", 0xB2))
        self.Tablets.append(Tablet("PTZ-1230",  "Wacom Intuos3 12x12", 0xB3))
        self.Tablets.append(Tablet("PTZ-1231W", "Wacom Intuos3 12x19", 0xB4))
        self.Tablets.append(Tablet("PTZ-631W",  "Wacom Intuos3 6x11", 0xB5))
        self.Tablets.append(Tablet("PTZ-431W",  "Wacom Intuos3 4x6", 0xB7))
        self.Tablets.append(Tablet("PTK-440", "Wacom Intuos4 4x6", 0xB8))
        self.Tablets.append(Tablet("PTK-640", "Wacom Intuos4 6x9", 0xB9))
        self.Tablets.append(Tablet("PTK-840", "Wacom Intuos4 8x13", 0xBA))
        self.Tablets.append(Tablet("PTK-1240", "Wacom Intuos4 12x19", 0xBB))
        self.Tablets.append(Tablet("PTH-451", "Wacom Intuos5 Pro S", 0x314))
        self.Tablets.append(Tablet("CTH-460", "Wacom Bamboo Pen 6x4", 0xD1))
        self.Tablets.append(Tablet("CTH-461", "Wacom Bamboo Fun", 0xD2))
        self.Tablets.append(Tablet("CTH-661", "Wacom BambooFun 2FG 6x8", 0xD3))
        self.Tablets.append(Tablet("CTL-460", "Wacom BambooFun 2FG 4x5", 0xD4))
        self.Tablets.append(Tablet("CTH-460K", "Wacom BambooPT 2FG 4x5", 0xD6))
        self.Tablets.append(Tablet("CTL-471", "Wacom Bamboo One S", 0x300))

    # self.Tablets.append(
    # tablet("PTK-540WL", "Wacom Intuos4 Wireless Bluetooth", 0x00)) # Stub, this needs special support


class Tablet:
    def __init__(self, Model, Name, ProductId):
        self.Name = Name
        self.Model = Model
        self.ProductId = ProductId
        self.Buttons = []
        self.GraphicWidth = -1

        try:
            # Attempt to load button map
            XML = xml.dom.minidom.parse("images/pad/"+self.Model+".xml")
        except:
            return

        try:
            # Load Custom Pad Descriptions
            XBase = XML.getElementsByTagName("padsettings")
            self.GraphicWidth = int(XBase[0].attributes["graphicwidth"].value)
            XPlateau = XBase[0].getElementsByTagName("button")
            for item in XPlateau:
                XName = item.attributes["name"].value
                XNumber = item.attributes["number"].value
                XCallsign = item.attributes["callsign"].value
                X1 = item.getElementsByTagName("x1")[0].childNodes[0].data
                Y1 = item.getElementsByTagName("y1")[0].childNodes[0].data
                X2 = item.getElementsByTagName("x2")[0].childNodes[0].data
                Y2 = item.getElementsByTagName("y2")[0].childNodes[0].data
                self.Buttons.append(Button(XName, XNumber, XCallsign, int(X1), int(Y1), int(X2), int(Y2)))
        except:
            print("Error loading " + "images/pad/" + self.Model + ".xml")


class Button:
    def __init__(self, Name, Number, Callsign, X1, Y1, X2, Y2):
        self.Name = Name
        self.Number = Number
        self.Callsign = Callsign
        self.X1 = X1
        self.Y1 = Y1
        self.X2 = X2
        self.Y2 = Y2
