import ui
import net


class AdminWhisperManager(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.board = None

		self.LoadWindow()
		



	def __del__(self):
		self.Destroy()
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/adminwhisper.py")
		except:
			import exception
			exception.Abort("LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")
			self.gonder = GetObject("gonder")
			self.duyuruylagonder = GetObject("duyuruylagonder")
			self.temizle = GetObject("temizle")
			self.yazi = GetObject("CommentValue")
			
			self.gonder.SetEvent(ui.__mem_func__(self.Gonder))
			self.duyuruylagonder.SetEvent(ui.__mem_func__(self.DGonder))
			self.temizle.SetEvent(ui.__mem_func__(self.Temizle))
			
			self.board.SetCloseEvent(ui.__mem_func__(self.__OnCloseButtonClick))

		except:
			import exception
			exception.Abort("LoadDialog.BindObject")
			
		
	def Destroy(self):
		self.ClearDictionary()
		self.titleBar = None



	def Open(self):	
		self.Show()
		self.SetCenterPosition()

	
	def Temizle(self):
		self.yazi.SetText("")
		
	def Gonder(self):
		text = self.yazi.GetText()
		# text = text.replace(" ", "$")
		net.SendBulkWhisperPacket(str(text))
		
	def DGonder(self):
		text = self.yazi.GetText()
		# text = text.replace(" ", "$")
		net.SendChatPacket("/b " + str(self.yazi.GetText()))
		net.SendBulkWhisperPacket(str(text))
			
	
		

	def Close(self):
		self.Hide()

			
	def __OnCloseButtonClick(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()

