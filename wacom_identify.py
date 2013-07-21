# Identifies wacom tablet model
from wacom_data import tabletidentities
import os

class TabletIdClass:
	def __init__(self, Cloak=""):
		self.TabletIds = tabletidentities()
	
	def Identify(self, Cloak=""):
		if Cloak != "":
			self.Data = ["iProduct " + Cloak]
		else:
			#self.Data = os.popen("lsusb -v | grep 'iProduct'").readlines()
			self.Data = os.popen("lsusb").readlines()
			
		self.Tablets = []
		for item in self.Data:
			if item.count("iProduct"):	# Identify by model name
				model = item.split(" ")[-1].replace("\n","")
				tablet = self.IdentifyByModel(model)				
				if tablet:
					self.Tablets.append(tablet)
			else:	# Identify by USB device code (more reliable)
				code = item.split(" ")[5].split(":")
				tablet = self.IdentifyByUSBId(code[0], code[1])
				if tablet:
					self.Tablets.append(tablet)
		return self.Tablets
		
	def IdentifyByModel(self,Model):
		for item in self.TabletIds.Tablets:
			if item.Model == Model:
				return item
				
	def IdentifyByUSBId(self,VendId, DevId):
		if int(VendId,16) == 0x56a:
			for item in self.TabletIds.Tablets:
				if item.ProductId == int(DevId,16):
					return item
