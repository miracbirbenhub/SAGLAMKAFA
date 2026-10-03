import ui
import net
import app
import constInfo
import uiCommon
import chrmgr


class NPCEkran(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE GAME OPTION DIALOG"

	def __Initialize(self):
		self.titleBar = 0

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
			exception.Abort("OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			
			self.genel = GetObject("genel")
			self.silah = GetObject("silah")
			self.zirh = GetObject("zirh")
			#self.depocu = GetObject("depocu")
			self.olay = GetObject("olay")
			self.market = GetObject("market")
			#self.metingaya = GetObject("metingaya")
			
			self.genel.SAFE_SetEvent(self.butonlar,9010)
			self.silah.SAFE_SetEvent(self.butonlar,9001)
			self.zirh.SAFE_SetEvent(self.butonlar,9002)
			#self.depocu.SAFE_SetEvent(self.butonlar,9005)
			self.olay.SAFE_SetEvent(self.butonlar,9004)
			self.market.SAFE_SetEvent(self.butonlar,9003)
			#self.metingaya.SAFE_SetEvent(self.butonlar,20505)

		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/npcekran.py")

		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		
	def butonlar(self, npc):
		net.SendChatPacket("/npcisopen " + str(npc))


	def OnPressEscapeKey(self):
		self.Close()
		return True


	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
