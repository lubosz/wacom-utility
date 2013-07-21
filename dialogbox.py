# Dialog Box Class

# Dialog Box
import gtk
import gtk.glade

class DialogBox:
	def __init__(self,parent,wTree):
		# Set the Glade file
		self.wTree = wTree
		# Load pointer for dialog box
		self.window = self.wTree.get_widget("dialogbox")
		self.window.set_title("Wacom Control Panel")
		self.window.set_transient_for(parent)
		self.window.set_destroy_with_parent(True)

	
		self.window.set_skip_taskbar_hint(1)
		self.window.set_skip_pager_hint(1)
		
		#self.window.present()
		self.label = self.wTree.get_widget("dialoglbl")
		#self.label.set_text(message)
		self.window.connect("destroy",self.callbackYes)
		self.window.connect("key-press-event", self.keydown)
		self.button2 = self.wTree.get_widget("dialogyes")
		self.button2.connect("button-press-event",self.callbackYes)
		#gtk.main()

	def callbackYes(self,widget=None,event=None):
		self.window.hide()
		try:
			gtk.main_quit()
		except:
			pass

		
	def keydown(self,widget=None,event=None):
		Key_Enter1 = 104
		Key_Enter2 = 36
		Key_Escape = 9
			
		key = event.hardware_keycode
		if key == Key_Enter1 or key==Key_Enter2:
			self.callbackYes()
		elif key ==  Key_Escape:
			pass
			#self.callbackNo()
	
	def NewMessage(self,message, title):
		self.window.set_title(title)
		self.label.set_markup(message)
		self.window.present()
		gtk.main()
		return

