#!/usr/bin/env python2
# Import global modules
# Dep: pygtk python-xml.dom.minidom wacom-tools

import sys
import gtk
import pygtk
import gobject
import gtk.glade
import cairo
import pango
import os
import gc
from copy import copy

# Import local modules

from wacom_identify import TabletIdClass
from wacom_interface import xSetWacom
import wacom_xorg
from dialogbox import DialogBox
from cairo_framework import Pad
from tablet_capplet import GraphicsTabletApplet

class Main:
	def __init__(self):
		# Set working directory
		os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
		# Check command line args
		for item in sys.argv:
			if item=="--configure" or item=="-c":
				f1 = open(os.path.expanduser("~/.wacom_utility"), 'r')
				data = f1.readlines()
				f1.close()
				for line in data:	# Check that we are running this stuff on startup
					if line[0] != "#":
						if line.split("=")[0] == "configureonlogin":
							self.ConfigureOnLogin = int(line.split("=")[1])
				if self.ConfigureOnLogin == 1:
					for line in data:
						if line.count("=")==0 and line[0] != "#":
							os.popen(line)
				sys.exit()

		# Set up GTK Window
		self.PressureMachine = None
		self.Create_Window()
		
		# Identify Wacom Product
		self.TabletIdObject = TabletIdClass()
		self.xSetWacomObject = xSetWacom()
		self.Tablets = self.TabletIdObject.Identify()
		self.Tablet=None
		# Load configuration file
		self.SaveConfig = 1

		try:
			os.stat(os.path.expanduser("~/.wacom_utility"))
		except:
			f1 = open(os.path.expanduser("~/.wacom_utility"), 'w')
			f1.writelines("forcemodel=''\n")
			f1.writelines("configureonlogin=1\n")
			f1.close()

		f1 = open(os.path.expanduser("~/.wacom_utility"), 'r')
		data = f1.readlines()
		f1.close()
		for line in data:
			if line[0] != "#":
				if line.split("=")[0] == "configureonlogin":
					self.ConfigureOnLogin = int(line.split("=")[1])
				elif line.split("=")[0] == "forcemodel":
					self.Tablets = self.TabletIdObject.Identify(line.split("=")[1].replace("\"","").replace("\'","").replace("\n",""))
		
		# If no tablets identified
		if len(self.Tablets) == 0:
			widget = self.wTree.get_widget("tablet-icon")
			file = "images/generic.png"
			widget.set_from_file(file)
			# Set tablet name
			widget = self.wTree.get_widget("tablet-label")
			widget.set_label("No graphics tablets detected")
			gtk.main()
			return
		# Check for autostart desktop file, if not present, generate it
		try:
			os.stat(os.path.expanduser("~/.config/autostart/Wacom_Utility.desktop"))
		except:
			# Ensure directories .config/autostart exist
			try:
				os.stat(os.path.expanduser("~/.config"))
				try:
					os.stat(os.path.expanduser("~/.config/autostart"))
				except:
					os.system("mkdir ~/.config/autostart")
			except:
				os.system("mkdir ~/.config")
				os.system("mkdir ~/.config/autostart")
			f1 = open(os.path.expanduser("~/.config/autostart/Wacom_Utility.desktop"), 'w')
			f1.writelines("#!/usr/bin/env xdg-open\n\n")
			f1.writelines("[Desktop Entry]\n")
			f1.writelines("Version=1.0\n")
			f1.writelines("Encoding=UTF-8\n")
			f1.writelines("Name=Wacom_Utility\n")
			f1.writelines("Type=Application\n")
			f1.writelines("Exec=/usr/share/wacom-utility/wacom_utility.py -c\n")
			f1.writelines("Terminal=false\n")
			f1.writelines("Icon=None\n")
			f1.writelines("Comment=Apply tablet settings on boot\n")
			f1.writelines("Categories=Utility;\n")
			f1.writelines("Hidden=false\n")
			f1.writelines("Name[en_CA]=Wacom_Utility.desktop\n")
			f1.writelines("Comment[en_CA]=This applies settings on boot\n")
			f1.writelines("X-GNOME-Autostart-enabled=true\n")
			f1.close()
		
		
		# Set the first tablet discovered to be the configured device
		self.Tablet = self.Tablets[0]
		# Configure Window
		
		self.window.set_size_request(600+self.Tablet.GraphicWidth,400)
		
		# Attempt to load custom icon for tablet model
		widget = self.wTree.get_widget("tablet-icon")
		try:
			file = "images/"+self.Tablet.Model+".png"
			os.stat(file)
		except:
			file = "images/generic.png"
		widget.set_from_file(file)
		
		# Set tablet name
		widget = self.wTree.get_widget("tablet-label")
		widget.set_label(self.Tablet.Name)
		
		# Set up treeview list for input devices
		devices = self.xSetWacomObject.ListInterfaces()
		widget = self.wTree.get_widget("input-list")
		widget.connect("cursor-changed",self.SelectDevice)
		list = gtk.ListStore(str)
		col = gtk.TreeViewColumn("Input Device")
		widget.append_column(col)
		celltext = gtk.CellRendererText()
		col.pack_start(celltext)
		col.add_attribute(celltext,'text',0)
		widget.set_model(list)
		for device in devices:
			list.append([device])
		list.append(["options"])
		
		# Set up selection of modifiers
		widget = self.wTree.get_widget("availkeys")
		list = gtk.ListStore(str, str)
		widget.set_model(list)
		data = self.xSetWacomObject.ListModifiers()
		for item in data:
			list.append(item)
		celltext = gtk.CellRendererText()
		widget.pack_start(celltext)
		widget.add_attribute(celltext,'text',1)
		widget.set_active(0)
		# Set up modify action window
		self.ModKeyWindow = self.wTree.get_widget("ModifyKey")
		self.ModKeyWindow.set_title("Edit Button Action")
		self.ModKeyWindow.set_transient_for(self.window)
		# Set up radio buttons
		widget0 = self.wTree.get_widget("rb1")
		widget1 = self.wTree.get_widget("rb2")
		widget1.set_group(widget0)
		widget2 = self.wTree.get_widget("rb3")
		widget2.set_group(widget0)
		
		# Set up selection of mouse actions
		widget = self.wTree.get_widget("MouseConfig")
		list = gtk.ListStore(str, str)
		widget.set_model(list)
		data = self.xSetWacomObject.ListMouseActions()
		for item in data:
			list.append(item)
		celltext = gtk.CellRendererText()
		widget.pack_start(celltext)
		widget.add_attribute(celltext,'text',1)
		widget.set_active(0)
		widget = self.wTree.get_widget("modhelp")
		widget.connect("button-press-event",self.Help,2)
		
		# Check for old xorg.conf configuration and offer to remove it
		
		if wacom_xorg.CheckXorgConfig()[0]:
			self.DialogBox.NewMessage("<b>Wacom Control Panel has detected an old configuration</b>\n\nWacom Control Panel now supports the new hotplugging support introduced with Ubuntu 9.04. Your xorg.conf contains tablet configuration that must be removed in order to use these new features. Clicking ok will remove these settings for you. Please enter your password if required to do so.\n\n<b>Your tablet will work as normal again after you log out and log back in again.</b>","Update old configuration")
			wacom_xorg.SetXorgConfig(0)
			os.system("/bin/sh -c 'gnome-session-save --logout-dialog' &")
			sys.exit()
		# Gtk main loop
		
		gtk.main()

	def do_donate(self,w,e):
		import os
		os.system("gnome-open \"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=YYBBSPYDAA7V8&lc=CA&item_name=Wacom%20Control%20Panel&currency_code=CAD&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted\"")

	
	def Create_Window(self):
		# Create widgets
		self.wTree = gtk.glade.XML("wacom_utility.glade")
		self.window = self.wTree.get_widget("window1")
		self.window.set_title("Wacom Tablet Configuration")
		self.window.connect("destroy",self.Close)
		# Set default button actions
		widget = self.wTree.get_widget("button-close")
		widget.connect("button-press-event",self.Close)
		widget = self.wTree.get_widget("button-help")
		widget.connect("button-press-event",self.Help,1)
		self.window.show_all()
		self.DialogBox = DialogBox(self.window,self.wTree)
		self.SelectedItem = "Welcome Screen"
		self.ChangeScreen()
	
	def Help(self,widget,event,page):
		#Page = 1: Main help
		#Page = 2: Pad settings help
		# Fixme: help not yet implamented
		os.system("/bin/sh -c \"gnome-open 'http://www.gtk-apps.org/content/show.php/Wacom+Control+Panel?content=104309'\"")
	
	def Close(self, widget=None,event=None):
		if self.SaveConfig == 1:
			if self.Tablet:
				self.xSetWacomObject.SaveToXSession(self.Tablet)
		else:
			self.xSetWacomObject.PurgeXSession()
		gtk.main_quit()
	
	def CheckBoxClick(self,widget,setting):
		value = int(widget.get_active())
		self.ChangeSetting(setting,value)
	
	def ChangeSetting(self,setting,value):
		if setting==1:
			self.ChangeSettingFile("configureonlogin",value)
			self.ConfigureOnLogin=value
		elif setting==2:
			wacom_xorg.SetXorgConfig(value)
			self.DialogBox.NewMessage("You need to log out and log back in again for the new configuration to take effect.\n\nA backup has been made in your home directory.","Wacom Control Panel")
			self.ChangeScreen()
	
	def ChangeSettingFile(self,setting,value):
		# Purges .wacom_utility file of any previous configuration and updates new
		try:
			os.stat(os.path.expanduser("~/.wacom_utility"))
		except:
			return	
		f1 = open(os.path.expanduser("~/.wacom_utility"), 'r')
		data = f1.readlines()
		f1.close()
		newdata = copy(data)
		for line in data:
			if line[0:len(setting)] == setting:
				newdata.remove(line)
		newdata.insert(0,setting+"="+str(value)+"\n")
		f2 = open(os.path.expanduser("~/.wacom_utility"), 'w')
		f2.writelines(newdata)
		f2.close()

	def SelectDevice(self,widget):
		Dataset = widget.get_model()
		Index = widget.get_cursor()
		activerow = Index[0][0]
		self.SelectedItem = Dataset[activerow][0]
		self.ChangeScreen()
	
	
	def ChangeScreen(self):
		container = self.wTree.get_widget("mainbox")
		if len(container.get_children()) == 2:
			container.remove(container.get_children()[1])
		if self.PressureMachine:
			self.PressureMachine.Stop()	
			del self.PressureMachine
			gc.collect()
			self.PressureMachine=None
			# Removing its gdk.window reference

		# Get a second copy of the tree structure
		wTree = gtk.glade.XML("wacom_utility.glade")
		if self.SelectedItem == "Welcome Screen":
			# Place container for this screen
			widget = wTree.get_widget("WelcomeScreen")
			widget.reparent(self.window)
			container.pack_end(widget)
		
		elif self.SelectedItem.lower().count("pad"):
			# Place container for this screen
			widget = wTree.get_widget("PadContainer")
			widget.reparent(self.window)
			container.pack_end(widget)

			# Configures Pad Graphic
			widget = Pad()
			widget.Set_Parameters(self.Tablet)
			widget.set_size_request(self.Tablet.GraphicWidth,-1)
			container = wTree.get_widget("padbox")
			container.pack_start(widget)
			widget.show()
			
			# Configures button maps
			container = wTree.get_widget("padbuttonlist")
			for item in self.Tablet.Buttons:
				placeholder = gtk.HBox()
				widget1 = gtk.Label()
				widget1.set_use_markup(True)
				widget1.set_markup("<span foreground='#000000' font_desc='sans 18' stretch='normal' weight='normal'>"+str(item.Number)+"</span>")
				
				widget2 = gtk.Label(item.Name)
				widget3 = gtk.Label(self.xSetWacomObject.GetTypeAndName(self.SelectedItem, item.Callsign)[1])
				widget4 = gtk.Button(stock="gtk-edit")
				widget4.connect("button-press-event",self.ShowModWindow, item)
				placeholder.pack_start(widget1,0,0,4)
				placeholder.pack_start(widget2,0,0,4)
				placeholder.pack_end(widget4,0,0,4)
				placeholder.pack_end(widget3,0,0,4)
				container.pack_start(placeholder,0,1,10)
			container.show_all()
			
		elif self.SelectedItem == "options":
			# Place container for this screen
			widget = wTree.get_widget("OptionsContainer")
			widget.reparent(self.window)
			container.pack_end(widget)
			# Configure events on options page
			widget = wTree.get_widget("applyonstartup")
			widget.set_active(self.ConfigureOnLogin)
			widget.connect("toggled",self.CheckBoxClick,1)
		else:
			# Place container for this screen
			widget = wTree.get_widget("PressureContainer")
			widget.reparent(self.window)
			container.pack_end(widget)
			self.PressureMachine = GraphicsTabletApplet(self.window, wTree, self.SelectedItem)
			self.PressureMachine.Run()
			
	def ShowModWindow(self,widget,event, button):
		a = ModifyAction(self.Tablet,self.wTree,self.SelectedItem, button, self.xSetWacomObject)
		self.ChangeScreen()
		# Ensures no memory leaks
		del a
		gc.collect()

class ModifyAction:
	def __init__(self,Tablet, wTree, Device, Button, xSetWacomObject):
		self.Tablet = Tablet
		self.SelectedItem = Device
		self.wTree = wTree
		self.Button = Button
		self.xSetWacomObject = xSetWacomObject
		self.Events = []
		# Display Window
		self.window = self.wTree.get_widget("ModifyKey")
		ev = self.window.connect("delete-event",self.close)
		self.Events.append([self.window,ev])
		# Connect events
		widget = self.wTree.get_widget("modclose")
		ev = widget.connect("button-press-event", self.close)
		self.Events.append([widget, ev])
		widget = self.wTree.get_widget("addaction")
		ev = widget.connect("button-press-event", self.AddMod)
		self.Events.append([widget, ev])
		# Set up widgets
		widget = self.wTree.get_widget("modlbl")
		widget.set_markup("<b>Modifying Action for " + self.Button.Name + "</b>")
		# Set contents of text box
		widget = self.wTree.get_widget("ModifyAction")
		widget.set_text("")
		ev = widget.connect("changed",self.CheckValidity)
		self.Events.append([widget, ev])
		# Configure radio buttons
		widget0 = self.wTree.get_widget("rb1")
		ev = widget0.connect("toggled",self.ChangeState)
		self.Events.append([widget0, ev])
		widget1 = self.wTree.get_widget("rb2")
		ev = widget1.connect("toggled",self.ChangeState)
		self.Events.append([widget1, ev])
		widget2 = self.wTree.get_widget("rb3")
		ev = widget2.connect("toggled",self.ChangeState)
		self.Events.append([widget2, ev])
		widget0.set_active(False)
		widget1.set_active(False)
		widget2.set_active(False)
		
		if self.xSetWacomObject.GetTypeAndName(self.SelectedItem,self.Button.Callsign)[0] == 0:
			widget0.set_active(True)
			self.UpdateActiveRegion(0)
		elif self.xSetWacomObject.GetTypeAndName(self.SelectedItem,self.Button.Callsign)[0] == 1:
			widget1.set_active(True)
			self.UpdateActiveRegion(1)
			self.UpdateForm()
		else:
			widget2.set_active(True)
			self.UpdateActiveRegion(2)
			self.UpdateForm()

		# Show Window
		self.window.show_all()
		gtk.main()

	def ChangeState(self,widget):
		if widget == self.wTree.get_widget("rb1"):
			self.UpdateActiveRegion(0)
		elif widget == self.wTree.get_widget("rb2"):
			self.UpdateActiveRegion(1)
		else:
			self.UpdateActiveRegion(2)

	def AddMod(self,widget,event):
		widget = self.wTree.get_widget("availkeys")
		widget2 = self.wTree.get_widget("ModifyAction")
		widget2.set_text(widget.get_model()[widget.get_active()][0]+" "+widget2.get_text())
		self.CheckValidity(widget2)

	def CheckValidity(self,widget):
		notice = self.wTree.get_widget("isvalid")
		if self.xSetWacomObject.VerifyString(widget.get_text())==1:
			notice.hide()
		else:
			notice.show()

	def UpdateActiveRegion(self,index):
		#0 = Ign
		#1 = Mouse
		#2 = Kbd
		if index == 0:
			widget = self.wTree.get_widget("MouseConfig")
			widget.set_sensitive(False)
			widget = self.wTree.get_widget("KeyConfig")
			widget.set_sensitive(False)
		elif index == 1:
			widget = self.wTree.get_widget("MouseConfig")
			widget.set_sensitive(True)
			widget = self.wTree.get_widget("KeyConfig")
			widget.set_sensitive(False)
		else:
			widget = self.wTree.get_widget("MouseConfig")
			widget.set_sensitive(False)
			widget = self.wTree.get_widget("KeyConfig")
			widget.set_sensitive(True)
	
	def UpdateForm(self):
		if self.xSetWacomObject.GetTypeAndName(self.SelectedItem,self.Button.Callsign)[0] == 0:
			pass
		elif self.xSetWacomObject.GetTypeAndName(self.SelectedItem,self.Button.Callsign)[0] == 1:
			widget = self.wTree.get_widget("MouseConfig")
			i = 0
			for item in widget.get_model():
				if item[1] == self.xSetWacomObject.GetTypeAndName(self.SelectedItem,self.Button.Callsign)[1]:
					widget.set_active(i)
				i+=1
		else:
			widget = self.wTree.get_widget("ModifyAction")
			widget.set_text(self.xSetWacomObject.GetTypeAndName(self.SelectedItem,self.Button.Callsign)[1])	
	
	def CommitChanges(self):
		if self.wTree.get_widget("rb1").get_active() == True:
			self.xSetWacomObject.SetByTypeAndName(self.SelectedItem,0,self.Button.Callsign)
		elif self.wTree.get_widget("rb2").get_active() == True:
			widget = self.wTree.get_widget("MouseConfig")
			self.xSetWacomObject.SetByTypeAndName(self.SelectedItem,1,self.Button.Callsign,widget.get_model()[widget.get_active()][1])
		else:
			widget = self.wTree.get_widget("ModifyAction")
			if self.xSetWacomObject.VerifyString(widget.get_text())==1:
				self.xSetWacomObject.SetByTypeAndName(self.SelectedItem,2,self.Button.Callsign,widget.get_text())

	def close(self,widget, event):
		self.CommitChanges()
		# Unlink all gtk events or python will not allow this object
		# to be destroyed, as there are events linked into this object's
		# code
		for event in self.Events:
			event[0].disconnect(event[1])
		gtk.main_quit()
		self.window.hide()
		
		

if __name__=="__main__":
	Main()
