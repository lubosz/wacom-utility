# Identifies wacom tablet model
from wacom_data import TabletIdentities
import os


class TabletIdClass:
    def __init__(self, cloak=""):
        self.TabletIds = TabletIdentities()
        self.tablets = []

    def identify(self, cloak=""):
        if cloak != "":
            self.data = ["iProduct " + cloak]
        else:
            # self.Data = os.popen("lsusb -v | grep 'iProduct'").readlines()
            self.data = os.popen("lsusb").readlines()

        for item in self.data:
            if item.count("iProduct"):  # Identify by model name
                model = item.split(" ")[-1].replace("\n", "")
                tablet = self.identify_by_model(model)
                if tablet:
                    self.tablets.append(tablet)
            else:  # Identify by USB device code (more reliable)
                code = item.split(" ")[5].split(":")
                tablet = self.identify_by_usb_id(code[0], code[1])
                if tablet:
                    self.tablets.append(tablet)
        return self.tablets

    def identify_by_model(self, model):
        for item in self.TabletIds.Tablets:
            if item.Model == model:
                return item

    def identify_by_usb_id(self, vendor_id, device_id):
        if int(vendor_id, 16) == 0x56a:
            for item in self.TabletIds.Tablets:
                if item.ProductId == int(device_id, 16):
                    return item
