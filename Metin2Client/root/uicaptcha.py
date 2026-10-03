import ui
import net
import app
import chat
import constInfo
import localeInfo
import uiCommon
import chrmgr
import uiToolTip
import player
import wndMgr
import playerSettingModule
import chr

class CaptchaWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE GAME OPTION DIALOG"

	def __Initialize(self):
		self.titleBar = 0
		self.item = 0
		self.item2 = 0
		self.item3 = 0
		self.item4 = 0
		self.item5 = 0
		self.time = 0
		self.sendinfo = 0
		self.sendinfotime = app.GetTime()

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY GAME OPTION DIALOG"
	
	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("CaptchaDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.board = self.GetChild("board")
			self.ItemSlot = self.GetChild("ItemSlot")
			self.item_name = self.GetChild("item_name")
			self.left_count = self.GetChild("left_count")
			self.time_text = self.GetChild("time_text")
			
			self.ItemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItem))

		except:
			import exception
			exception.Abort("CaptchaDialog.__Load_BindObject")

	def OnUpdate(self):	
		if self.sendinfo > 0:
			end_left_time = self.time - app.GetGlobalTimeStamp()
			end_real_time = localeInfo.SecondToDHM(end_left_time)
			self.time_text.SetText(str(end_real_time))


	def __Load(self):
		self.__Load_LoadScript("uiscript/captchadialog.py")

		self.__Load_BindObject()

		self.SetCenterPosition()
		
		
	def SelectItem(self, slotIndex):
		if slotIndex == 0:
			net.SendChatPacket("/answer_captcha " + str(self.item))
		elif slotIndex == 1:
			net.SendChatPacket("/answer_captcha " + str(self.item2))
		elif slotIndex == 2:
			net.SendChatPacket("/answer_captcha " + str(self.item3))
		elif slotIndex == 3:
			net.SendChatPacket("/answer_captcha " + str(self.item4))
		elif slotIndex == 4:
			net.SendChatPacket("/answer_captcha " + str(self.item5))
		
	def Destroy(self):
		self.ClearDictionary()
		self.board = None
		
	def Open(self, item, item2, item3, item4, item5, left, name, time):
		ui.ScriptWindow.Show(self)
		self.ItemSlot.SetItemSlot(0,item,0)
		self.ItemSlot.SetItemSlot(1,item2,0)
		self.ItemSlot.SetItemSlot(2,item3,0)
		self.ItemSlot.SetItemSlot(3,item4,0)
		self.ItemSlot.SetItemSlot(4,item5,0)
		self.item = item
		self.item2 = item2
		self.item3 = item3
		self.item4 = item4
		self.item5 = item5
		self.time = time
		self.sendinfo = 1
		
		self.left_count.SetText("Kalan hakkýnýz: %d " % left)
		self.item_name.SetText(name[:(len(name)/8)]+"-"+name[(len(name)/8):(len(name)/4)]+"-"+name[(len(name)/4):(len(name)/2)]+"-"+name[(len(name)/2):len(name)-2])
		
	def Close(self):
		self.Hide()
		return True