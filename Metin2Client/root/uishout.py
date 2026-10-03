import ui
import chat
# import random
import net
import constInfo
# import random
from _weakref import proxy
from itertools import islice

class ShoutManager(ui.ScriptWindow):

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
			pyScrLoader.LoadScriptFile(self, "uiscript/shout.py")
		except:
			import exception
			exception.Abort("DiceClass.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")
			self.baslat = GetObject("baslat")
			self.durdur = GetObject("durdur")
			self.temizle = GetObject("temizle")
			self.bilgi = GetObject("bilgi")
			self.yazi = GetObject("CommentValue")
			
			self.baslat.SetEvent(ui.__mem_func__(self.Baslat))
			self.durdur.SetEvent(ui.__mem_func__(self.Durdur))
			self.temizle.SetEvent(ui.__mem_func__(self.Temizle))
			
			self.board.SetCloseEvent(ui.__mem_func__(self.__OnCloseButtonClick))

		except:
			import exception
			exception.Abort("DiceClass.LoadDialog.BindObject")
			
		
	def Destroy(self):
		self.ClearDictionary()
		self.titleBar = None



	def Open(self):	
		if constInfo.auto_shout_status == 1:
			self.bilgi.SetText("Gönderilecek mesajý yazýn. (Mevcut Durum: Aktif)")
		else:
			self.bilgi.SetText("Gönderilecek mesajý yazýn. (Mevcut Durum: Pasif)")
		
		self.Show()
		self.SetCenterPosition()
		
	def OnUpdate(self):
		if constInfo.auto_shout_status == 1:
			self.bilgi.SetText("Gönderilecek mesajý yazýn. (Mevcut Durum: Aktif)")
		else:
			self.bilgi.SetText("Gönderilecek mesajý yazýn. (Mevcut Durum: Pasif)")

	
	def Temizle(self):
		self.yazi.SetText("")
		
	def Baslat(self):
		constInfo.auto_shout_text = self.yazi.GetText()
		constInfo.auto_shout_status = 1
		
	def Durdur(self):
		constInfo.auto_shout_text = ""
		constInfo.auto_shout_status = 0

	def Close(self):
		self.Hide()

			
	def __OnCloseButtonClick(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()

