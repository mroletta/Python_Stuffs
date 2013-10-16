import wx
import os

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(200,100))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar() # A status bar at the bottom of the MainWindow

		#setting up the menu
		filemenu= wx.Menu()

		#wx.ID_ABOUT and wx.IDE_EXIT are standard IDs provided by wxWidgets.
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About","Information about this program")
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit","Terminte the program")
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open a File")


		#Create the menu bar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		self.SetMenuBar(menuBar)
		
		# Set events
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)

		self.Show(True)

	def OnAbout(self,e):
		# A message dialog box with an OK button.  wx.OK is standard ID in wxWidgets
		dlg = wx.MessageDialog(self, "A small text editor", "About sample editor", wx.OK)
		dlg.ShowModal ()
		dlg.Destroy

	def OnExit(self,e):
		self.Close(True) # Close the frame

	def OnOpen(self,e):
		"""Open a file"""
		self.dirname = ''
		dlg = wx.FileDialog(self, "Chose a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'r')
			self.control.SetValue(f.read())
			f.close()
		dlg.Destroy()	



app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()