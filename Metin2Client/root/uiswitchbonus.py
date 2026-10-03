import ui
import net
import chat
import app
import player
import game
import uiCommon
import debugInfo
import time
import shop
import uiTip
import uiBonusListe
import item

Switchbutton = 0
Bonus0 = 0
Bonus1 = 0
Bonus2 = 0
Bonus3 = 0
Bonus4 = 0
Presswish0 = 0
Presswish1 = 0
Presswish2 = 0
Presswish3 = 0
Presswish4 = 0
Overwrite0 = 0
Overwrite1 = 0
Overwrite2 = 0
Overwrite3 = 0
Overwrite4 = 0
Switchvalue = 71084

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()
		
		self.BoniListe = uiBonusListe.OptionDialog()
		self.bigBoard = uiTip.BigBoard()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.titleBar = 0

	def Destroy(self):
		self.ClearDictionary()
		self.__Initialize()
	
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
			self.Bvalue1		= GetObject("bonus_value_1")
			self.Bvalue2		= GetObject("bonus_value_2")
			self.Bvalue3		= GetObject("bonus_value_3")
			self.Bvalue4		= GetObject("bonus_value_4")
			self.Bvalue5		= GetObject("bonus_value_5")
			self.StartButton		= GetObject("start_switch_button")
			self.Wunschbonus01	= GetObject("choose_button_01")
			self.Wunschbonus02	= GetObject("choose_button_02")
			self.Wunschbonus03	= GetObject("choose_button_03")
			self.Wunschbonus04	= GetObject("choose_button_04")
			self.Wunschbonus05	= GetObject("choose_button_05")
			self.ResetbonusallButton			= GetObject("reset_bonusall")
			self.Switchtingabbruchbutton			= GetObject("break_bonusswitch")
			
		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):	
		self.__Load_LoadScript("UIscript/switchbonus.py")

		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Wunschbonus01.SetEvent(ui.__mem_func__(self.__Wish_1_Option))
		self.Wunschbonus02.SetEvent(ui.__mem_func__(self.__Wish_2_Option))
		self.Wunschbonus03.SetEvent(ui.__mem_func__(self.__Wish_3_Option))
		self.Wunschbonus04.SetEvent(ui.__mem_func__(self.__Wish_4_Option))
		self.Wunschbonus05.SetEvent(ui.__mem_func__(self.__Wish_5_Option))
		self.ResetbonusallButton.SetEvent(ui.__mem_func__(self.__Resetbonusall))
		self.StartButton.SetEvent(ui.__mem_func__(self.__Switchtingdialog))
		self.Switchtingabbruchbutton.SetEvent(ui.__mem_func__(self.__BreakSwitching))
		
	def __BreakSwitching(self):
		global Switchbutton
		if Switchbutton == 1:
			self.switcherDialog.Close()
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Efsun botu iptal edildi.")		
			self.Switchtingabbruchbutton.SetText("Kapat")
			Switchbutton = 0		
		else:
			self.Hide()
	
	def __Switchtingdialog(self):
		import item
		global Switchbutton
		global Bonus0
		global Bonus1
		global Bonus2
		global Bonus3
		global Bonus4
		global Switchvalue
		val0, bon0 = player.GetItemAttribute(0, 0) #(itemposition, atrribute)
		val1, bon1 = player.GetItemAttribute(0, 1) #(itemposition, atrribute)
		val2, bon2 = player.GetItemAttribute(0, 2) #(itemposition, atrribute)
		val3, bon3 = player.GetItemAttribute(0, 3) #(itemposition, atrribute)
		val4, bon4 = player.GetItemAttribute(0, 4) #(itemposition, atrribute)
		self.switcherDialog = SwitchingDialog()
		Search0 = self.Bvalue1.GetText()
		Search1 = self.Bvalue2.GetText()
		Search2 = self.Bvalue3.GetText()
		Search3 = self.Bvalue4.GetText()
		Search4 = self.Bvalue5.GetText()
		self.Switchtingabbruchbutton.SetText("Durdur")
		Switchbutton = 1		
		DELAY_SEC = 0.3

#1 Bonus switchen:		
		if (int(Bonus1) == 0) and (val0 == int(Bonus0) and bon0 >= int(Search0) or (val1 == int(Bonus0) and bon1 >= int(Search0)) or (val2 == int(Bonus0) and bon2 >= int(Search0)) or (val3 == int(Bonus0) and bon3 >= int(Search0)) or (val4 == int(Bonus0) and bon4 >= int(Search0))):
			self.bigBoard.SetTip("Ýstediðin bonuslar geldi.")
			self.bigBoard.SetTop()
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ýstediðin bonuslar geldi.")		
			self.Switchtingabbruchbutton.SetText("Kapat")
			Switchbutton = 0		
#2 Bonis switchen:
		elif (int(Bonus2) == 0) and (val0 == int(Bonus0) and bon0 >= int(Search0) or (val1 == int(Bonus0) and bon1 >= int(Search0)) or (val2 == int(Bonus0) and bon2 >= int(Search0)) or (val3 == int(Bonus0) and bon3 >= int(Search0)) or (val4 == int(Bonus0) and bon4 >= int(Search0))) and ((val0 == int(Bonus1) and bon0 >= int(Search1)) or (val1 == int(Bonus1) and bon1 >= int(Search1)) or (val2 == int(Bonus1) and bon2 >= int(Search1)) or (val3 == int(Bonus1) and bon3 >= int(Search1)) or (val4 == int(Bonus1) and bon4 >= int(Search1))):
			self.bigBoard.SetTip("Ýstediðin bonuslar geldi.")
			self.bigBoard.SetTop()
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ýstediðin bonuslar geldi.")		
			self.Switchtingabbruchbutton.SetText("Kapat")
			Switchbutton = 0		
#3 Bonis switchen:
		elif (int(Bonus3) == 0) and (val0 == int(Bonus0) and bon0 >= int(Search0) or (val1 == int(Bonus0) and bon1 >= int(Search0)) or (val2 == int(Bonus0) and bon2 >= int(Search0)) or (val3 == int(Bonus0) and bon3 >= int(Search0)) or (val4 == int(Bonus0) and bon4 >= int(Search0))) and ((val0 == int(Bonus1) and bon0 >= int(Search1)) or (val1 == int(Bonus1) and bon1 >= int(Search1)) or (val2 == int(Bonus1) and bon2 >= int(Search1)) or (val3 == int(Bonus1) and bon3 >= int(Search1)) or (val4 == int(Bonus1) and bon4 >= int(Search1))) and ((val0 == int(Bonus2) and bon0 >= int(Search2)) or (val1 == int(Bonus2) and bon1 >= int(Search2)) or (val2 == int(Bonus2) and bon2 >= int(Search2)) or (val3 == int(Bonus2) and bon3 >= int(Search2)) or (val4 == int(Bonus2) and bon4 >= int(Search2))):
			self.bigBoard.SetTip("Ýstediðin bonuslar geldi.")
			self.bigBoard.SetTop()
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ýstediðin bonuslar geldi.")		
			self.Switchtingabbruchbutton.SetText("Kapat")
			Switchbutton = 0		
#4 Bonis switchen:
		elif (int(Bonus4) == 0) and (val0 == int(Bonus0) and bon0 >= int(Search0) or (val1 == int(Bonus0) and bon1 >= int(Search0)) or (val2 == int(Bonus0) and bon2 >= int(Search0)) or (val3 == int(Bonus0) and bon3 >= int(Search0)) or (val4 == int(Bonus0) and bon4 >= int(Search0))) and ((val0 == int(Bonus1) and bon0 >= int(Search1)) or (val1 == int(Bonus1) and bon1 >= int(Search1)) or (val2 == int(Bonus1) and bon2 >= int(Search1)) or (val3 == int(Bonus1) and bon3 >= int(Search1)) or (val4 == int(Bonus1) and bon4 >= int(Search1))) and ((val0 == int(Bonus2) and bon0 >= int(Search2)) or (val1 == int(Bonus2) and bon1 >= int(Search2)) or (val2 == int(Bonus2) and bon2 >= int(Search2)) or (val3 == int(Bonus2) and bon3 >= int(Search2)) or (val4 == int(Bonus2) and bon4 >= int(Search2))) and ((val0 == int(Bonus3) and bon0 >= int(Search3)) or (val1 == int(Bonus3) and bon1 >= int(Search3)) or (val2 == int(Bonus3) and bon2 >= int(Search3)) or (val3 == int(Bonus3) and bon3 >= int(Search3)) or (val4 == int(Bonus3) and bon4 >= int(Search3))):
			self.bigBoard.SetTip("Ýstediðin bonuslar geldi.")
			self.bigBoard.SetTop()
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ýstediðin bonuslar geldi.")		
			self.Switchtingabbruchbutton.SetText("Kapat")
			Switchbutton = 0		
#5 Bonis switchen:
		elif (int(Bonus4) != 0) and (val0 == int(Bonus0) and bon0 >= int(Search0) or (val1 == int(Bonus0) and bon1 >= int(Search0)) or (val2 == int(Bonus0) and bon2 >= int(Search0)) or (val3 == int(Bonus0) and bon3 >= int(Search0)) or (val4 == int(Bonus0) and bon4 >= int(Search0))) and ((val0 == int(Bonus1) and bon0 >= int(Search1)) or (val1 == int(Bonus1) and bon1 >= int(Search1)) or (val2 == int(Bonus1) and bon2 >= int(Search1)) or (val3 == int(Bonus1) and bon3 >= int(Search1)) or (val4 == int(Bonus1) and bon4 >= int(Search1))) and ((val0 == int(Bonus2) and bon0 >= int(Search2)) or (val1 == int(Bonus2) and bon1 >= int(Search2)) or (val2 == int(Bonus2) and bon2 >= int(Search2)) or (val3 == int(Bonus2) and bon3 >= int(Search2)) or (val4 == int(Bonus2) and bon4 >= int(Search2))) and ((val0 == int(Bonus3) and bon0 >= int(Search3)) or (val1 == int(Bonus3) and bon1 >= int(Search3)) or (val2 == int(Bonus3) and bon2 >= int(Search3)) or (val3 == int(Bonus3) and bon3 >= int(Search3)) or (val4 == int(Bonus3) and bon4 >= int(Search3))) and ((val0 == int(Bonus4) and bon0 >= int(Search4)) or (val1 == int(Bonus4) and bon1 >= int(Search4)) or (val2 == int(Bonus4) and bon2 >= int(Search4)) or (val3 == int(Bonus4) and bon3 >= int(Search4)) or (val4 == int(Bonus4) and bon4 >= int(Search4))):
			self.bigBoard.SetTip("Ýstediðin bonuslar geldi.")
			self.bigBoard.SetTop()
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ýstediðin bonuslar geldi.")		
			self.Switchtingabbruchbutton.SetText("Kapat")
			Switchbutton = 0		
		elif Bonus0 == 0:
			self.Switchtingabbruchbutton.SetText("Kapat")
			Switchbutton = 0		
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Yapmaniz gerekenler:")		
			chat.AppendChat(chat.CHAT_TYPE_INFO, "1. kutuya efsunlanacak koy. ")		
			chat.AppendChat(chat.CHAT_TYPE_INFO, "2.In cea de-a doua casuta din inventar pune-ti Vrajeste Obiectul")		
		else:
			self.switcherDialog.Open(DELAY_SEC)
			self.switcherDialog.SAFE_SetTimeOverEvent(self.__Switchtingdialog)
			self.switcherDialog.SetText("Switching")
			for eachSlot in xrange(player.INVENTORY_PAGE_SIZE*2):
				getShopItemID = shop.GetItemID(eachSlot)
				itemVNum = player.GetItemIndex(eachSlot)
				if getShopItemID == int(Switchvalue) and not itemVNum == int(Switchvalue):
					net.SendShopBuyPacket(eachSlot)
				if itemVNum == int(Switchvalue):
					net.SendItemUseToItemPacket(eachSlot, 0)
					break
					
	def __Resetbonusall(self):
		global Bonus0
		global Bonus1
		global Bonus2
		global Bonus3
		global Bonus4
		Bonus0 = 0
		Bonus1 = 0
		Bonus2 = 0
		Bonus3 = 0
		Bonus4 = 0
		self.Bvalue1.SetText("0")
		self.Bvalue2.SetText("0")
		self.Bvalue3.SetText("0")
		self.Bvalue4.SetText("0")
		self.Bvalue5.SetText("0")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Bonuslar silindi.")
	
	def __Wish_1_Option(self):
		global Bonus0
		global Overwrite0
		global Presswish0
		if Bonus0 != 0:
			Overwrite0 = 1
		Presswish0 = 1
		self.BoniListe.Show()
		self.BoniListe.SetTop()
		
	def __Wish_2_Option(self):
		global Bonus1
		global Overwrite1
		global Presswish1
		if Bonus1 != 0:
			Overwrite1 = 1
		Presswish1 = 1
		self.BoniListe.Show()
		self.BoniListe.SetTop()
		
	def __Wish_3_Option(self):
		global Bonus2
		global Overwrite2
		global Presswish2
		if Bonus2 != 0:
			Overwrite2 = 1
		Presswish2 = 1
		self.BoniListe.Show()
		self.BoniListe.SetTop()
		
	def __Wish_4_Option(self):
		global Bonus3
		global Overwrite3
		global Presswish3
		if Bonus3 != 0:
			Overwrite3 = 1
		Presswish3 = 1
		self.BoniListe.Show()
		self.BoniListe.SetTop()
		
	def __Wish_5_Option(self):
		global Bonus4
		global Overwrite4
		global Presswish4
		if Bonus4 != 0:
			Overwrite4 = 1
		Presswish4 = 1
		self.BoniListe.Show()
		self.BoniListe.SetTop()

	def OnPressEscapeKey(self):
		self.Hide()
		return TRUE

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		
class SwitchingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/SwitchingDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.countdownMessage = self.GetChild("countdown_message")

		except:
			import exception
			exception.Abort("ConnectingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.SetCenterPosition()
		self.SetTop()
		self.Show()		

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.message.SetText(text)

	def SetCountDownMessage(self, waitTime):
		self.countdownMessage.SetText("Efsun Bot")

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)

	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			self.Close()
			self.eventTimeOver()
		else:
			self.SetCountDownMessage(self.endTime - time.clock())

	def OnPressExitKey(self):
		#self.eventExit()
		return TRUE
