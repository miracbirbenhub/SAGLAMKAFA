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
import grp
import introLogin

coin = {50,100,150,200,250,300,350,400,450,500}

price = {
	1: 2,
	2: 5,
	3: 7,
	4: 10,
	5: 12,
	6: 15, 
	7: 17,
	8: 20,
	9: 22,
	10: 25,
	11: 27,
	12: 32,
	13: 35,
	14: 40,
	15: 45,
	16: 50,
	17: 62,
	18: 75,
	19: 80,
	20: 85,
	21: 90,
	22: 95,
	23: 100,
	24: 125
}

class DealWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE GAME OPTION DIALOG"

	def __Initialize(self):
		self.titleBar = None
		self.board = None
		self.questionDialog = None
		self.popUpTimer = None
		self.InputDialog = None
		self.tab = {}
		self.boxtab = {}
		self.boxtab2 = {}
		self.boxtab3 = {}
		self.boxtab4 = {}
		self.text = {}
		self.tab2 = {}
		self.text2 = {}
		self.boxtext = {}
		self.boxtext2 = {}
		self.boxtext3 = {}
		self.boxtext4 = {}
		self.first = 0
		self.offer_time = 0
		self.my_price = 0
		self.coin = 0
		self.price_type = "Ejderha Parasý"
		self.type = 1

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
			exception.Abort("DealWindow.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.board = self.GetChild("board")
			self.left_box = self.GetChild("left_box")
			self.offer_text = self.GetChild("offer_text")
			self.offer_accept = self.GetChild("offer_accept")
			self.offer_cancel = self.GetChild("offer_cancel")
			
			self.offer_accept.SetEvent(ui.__mem_func__(self.OfferAccept))
			self.offer_cancel.SetEvent(ui.__mem_func__(self.OfferCancel))

		except:
			import exception
			exception.Abort("DealWindow.__Load_BindObject")
	

	def __Load(self):
		self.__Load_LoadScript("uiscript/dealwindow.py")

		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		# self.CreateButtons()
		self.CreateBoxes()
		self.CreatePopupDialog()
		
	def CreatePopupDialog(self):
		self.popupWindow = PopupDialog()
		self.popupWindow.LoadDialog()
		self.popupWindow.SetCenterPosition()
		self.popupWindow.Hide()
		
	def SendPopUp(self):
		self.popupWindow.Close()
		self.popupWindow.Open("Baþlamak için bir kutu seçin.", 0, localeInfo.UI_OK) 
		
	def InputCoin(self, type):
		max = 5
		title = "Yatýrýlacak Ep Miktarý(Min.50 Ep)"
		event = ui.__mem_func__(self.AcceptCoin)
		
		if type == 2: #yang
			title = "Yatýrýlacak M Miktarý(Min.50 M)"
			event = ui.__mem_func__(self.AcceptYang)
			
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(title)
		inputDialog.SetMaxLength(max)
		inputDialog.SetNumberMode()
		inputDialog.SetAcceptEvent(event)
		inputDialog.SetCancelEvent(ui.__mem_func__(self.CloseInput))
		inputDialog.Open()
		self.inputDialog = inputDialog
		
	def AcceptCoin(self):
		if not self.inputDialog:
			return True
		
		if not len(self.inputDialog.GetText()):
			return True
		
		text = int(self.inputDialog.GetText())
		
		if not text in coin:
			chat.AppendChat(1,"Miktar min. 50, max 500 olmalý.")
			chat.AppendChat(1,"Ayný zamanda 50 ve 50'nin katlarý olmalý.")
			self.inputDialog = None
			self.Close()
			return True
		
		self.mycoin = text
		
		self.inputDialog = None
		self.SendPopUp()

	def AcceptYang(self):
		if not self.inputDialog:
			return True
		
		if not len(self.inputDialog.GetText()):
			return True
		
		text = int(self.inputDialog.GetText())
		
		if not text in coin:
			chat.AppendChat(1,"Miktar min. 50, max 500 olmalý.")
			chat.AppendChat(1,"Ayný zamanda 50 ve 50'nin katlarý olmalý.")
			self.inputDialog = None
			self.Close()
			return True
		
		self.mycoin = text
		
		self.inputDialog = None
		self.SendPopUp()

	def CloseInput(self):
		self.inputDialog = None
		self.Close()
		return True
		
	def SendPopUp2(self, offer):
		self.popupWindow.Close()
		if self.type == 2:
			yang = 1000000
			checkText = localeInfo.NumberToMoneyStringKTM(yang * int(offer))
			self.popupWindow.Open("%s Kazandýnýz." % checkText, 0, localeInfo.UI_OK) 
		else:
			self.popupWindow.Open("%d Ejderha Parasý kazandýnýz." % int(offer), 0, localeInfo.UI_OK) 
		self.Close()
		
	def CreateButtons(self):
		for i in range(12):
			self.MakeButton(
				i,\
				self.board,\
				13, 33 + (34 * i)
			)
			self.MakeButton2(
				i,\
				self.board,\
				487, 33 + (34 * i)
			)
			
	def CreateBoxes(self):
		for i in range(6):
			self.MakeBox(
				i,\
				self.board,\
				140 + (53 * i), 135
			)
			self.MakeBox2(
				i+6,\
				self.board,\
				140 + (53 * i), 135+53
			)
			self.MakeBox3(
				i+12,\
				self.board,\
				140 + (53 * i), 135+53*2
			)
			self.MakeBox4(
				i+18,\
				self.board,\
				140 + (53 * i), 135+53*3
			)
			
	def MakeButton(self, index, parent, x, y):
		self.tab[index] = ui.MakeButton(parent, x, y, False, "dealornodeal/", "empty_box.png", "empty_box.png", "down.png")

		yang = 1000000
		carpan = 1
		if self.coin > 1:
			carpan = self.coin
		
		self.text[index] = ui.TextLine()
		self.text[index].SetParent(self.tab[index])
		self.text[index].SetPosition(30, 7)
		self.text[index].SetWindowHorizontalAlignCenter()
		self.text[index].SetHorizontalAlignCenter()
		if self.price_type == "M Yang":
			self.text[index].SetText(localeInfo.NumberToMoneyStringKTM(yang * (carpan * price[(index+1)])))
		else:
			self.text[index].SetText("%d %s" % (carpan * price[(index+1)],self.price_type))
		self.text[index].SetPackedFontColor(self.GetColorIndex(index+1))
		self.text[index].Show()
		
	def MakeButton2(self, index, parent, x, y):
		self.tab2[index] = ui.MakeButton(parent, x, y, False, "dealornodeal/", "empty_box.png", "empty_box.png", "down.png")
		
		yang = 1000000
		carpan = 1
		if self.coin > 1:
			carpan = self.coin
			
		self.text2[index] = ui.TextLine()
		self.text2[index].SetParent(self.tab2[index])
		self.text2[index].SetPosition(30, 7)
		self.text2[index].SetWindowHorizontalAlignCenter()
		self.text2[index].SetHorizontalAlignCenter()
		if self.price_type == "M Yang":
			self.text2[index].SetText(localeInfo.NumberToMoneyStringKTM(yang * (carpan * price[(index+13)])))
		else:
			self.text2[index].SetText("%d %s" % (carpan * price[(index+13)],self.price_type))
		self.text2[index].SetPackedFontColor(self.GetColorIndex(index+13))
		self.text2[index].Show()
		
	def MakeBox(self, index, parent, x, y):
		self.boxtab[index] = ui.MakeButton(parent, x, y, False, "dealornodeal/", "box2.png", "box2.png", "box2.png")

		self.boxtext[index] = ui.TextLine()
		self.boxtext[index].SetParent(self.boxtab[index])
		self.boxtext[index].SetPosition(0, 27)
		self.boxtext[index].SetFontName("Tahoma:16")
		self.boxtext[index].SetWindowHorizontalAlignCenter()
		self.boxtext[index].SetHorizontalAlignCenter()
		self.boxtext[index].SetText("%d" % (index+1))
		self.boxtext[index].SetPackedFontColor(grp.GenerateColor(0, 0, 0, 1.0))
		self.boxtext[index].Show()
		
		self.boxtab[index].SetEvent(ui.__mem_func__(self.__OpenBoxDialog), (index), self.boxtab[index])

	def MakeBox2(self, index, parent, x, y):
		self.boxtab2[index] = ui.MakeButton(parent, x, y, False, "dealornodeal/", "box2.png", "box2.png", "box2.png")

		self.boxtext2[index] = ui.TextLine()
		self.boxtext2[index].SetParent(self.boxtab2[index])
		self.boxtext2[index].SetPosition(0, 27)
		self.boxtext2[index].SetFontName("Tahoma:16")
		self.boxtext2[index].SetWindowHorizontalAlignCenter()
		self.boxtext2[index].SetHorizontalAlignCenter()
		self.boxtext2[index].SetText("%d" % (index+1))
		self.boxtext2[index].SetPackedFontColor(grp.GenerateColor(0, 0, 0, 1.0))
		self.boxtext2[index].Show()
		
		self.boxtab2[index].SetEvent(ui.__mem_func__(self.__OpenBoxDialog), (index), self.boxtab2[index])

	def MakeBox3(self, index, parent, x, y):
		self.boxtab3[index] = ui.MakeButton(parent, x, y, False, "dealornodeal/", "box2.png", "box2.png", "box2.png")

		self.boxtext3[index] = ui.TextLine()
		self.boxtext3[index].SetParent(self.boxtab3[index])
		self.boxtext3[index].SetPosition(0, 27)
		self.boxtext3[index].SetFontName("Tahoma:16")
		self.boxtext3[index].SetWindowHorizontalAlignCenter()
		self.boxtext3[index].SetHorizontalAlignCenter()
		self.boxtext3[index].SetText("%d" % (index+1))
		self.boxtext3[index].SetPackedFontColor(grp.GenerateColor(0, 0, 0, 1.0))
		self.boxtext3[index].Show()

		self.boxtab3[index].SetEvent(ui.__mem_func__(self.__OpenBoxDialog), (index), self.boxtab3[index])

	def MakeBox4(self, index, parent, x, y):
		self.boxtab4[index] = ui.MakeButton(parent, x, y, False, "dealornodeal/", "box2.png", "box2.png", "box2.png")

		self.boxtext4[index] = ui.TextLine()
		self.boxtext4[index].SetParent(self.boxtab4[index])
		self.boxtext4[index].SetPosition(0, 27)
		self.boxtext4[index].SetFontName("Tahoma:16")
		self.boxtext4[index].SetWindowHorizontalAlignCenter()
		self.boxtext4[index].SetHorizontalAlignCenter()
		self.boxtext4[index].SetText("%d" % (index+1))
		self.boxtext4[index].SetPackedFontColor(grp.GenerateColor(0, 0, 0, 1.0))
		self.boxtext4[index].Show()
		
		self.boxtab4[index].SetEvent(ui.__mem_func__(self.__OpenBoxDialog), (index), self.boxtab4[index])
		
	def GetColorIndex(self, index):
		if index >= 1 and index <= 6:
			return 0xff00688B
		elif index >= 7 and index <= 12:
			return 0xffFFD39B
		elif index >= 13 and index <= 17:
			return 0xff3D9140
		elif index >= 18 and index <= 21:
			return 0xffFF3030
		elif index >= 22 and index <= 24:
			return 0xffCD0000
	
	def __OpenBoxDialog(self, numb, button):
		if self.offer_time == 1:
			chat.AppendChat(1,"Teklifi cevaplamadan kutu secemezsiniz.")
			return
		questionDialog = uiCommon.QuestionDialog()
		if self.first == 0:
			questionDialog.SetText("%d numaralý kutuyu seçmek istiyor musunuz?" % (numb+1))
		else:
			questionDialog.SetText("%d numaralý kutuyu açmak istiyor musunuz?" % (numb+1))
		questionDialog.SetAcceptEvent(lambda arg=True: self.__OpenBox(arg))
		questionDialog.SetCancelEvent(lambda arg=False: self.__OpenBox(arg))
		questionDialog.Open()
		questionDialog.numb = numb+1
		questionDialog.button = button
		self.questionDialog = questionDialog
	
	
	def OfferAccept(self):
		net.SendChatPacket("/dealornodeal 3 1 1 1")
		
	def OfferCancel(self):
		net.SendChatPacket("/dealornodeal 3 2 1 1")
		
	def OnUpdate(self):
		if self.inputDialog and len(self.inputDialog.GetText()) > 0:
			text = int(self.inputDialog.GetText())
			self.coin = text
			if self.coin >= 50:
				self.coin /= 50
				self.CreateButtons()
			
		if self.offer_time == 1:
			self.offer_accept.Show()
			self.offer_cancel.Show()
		else:
			self.offer_accept.Hide()
			self.offer_cancel.Hide()
	
	def __OpenBox(self, answer):
		if not self.questionDialog:
			return

		if answer:
			numb = self.questionDialog.numb
			button = self.questionDialog.button
			if self.first == 0:
				net.SendChatPacket("/dealornodeal 1 %d %d %d" % (numb,self.mycoin, self.type))
				button.SetDownVisual("dealornodeal/selected.png")
				self.first = 1
			else:
				net.SendChatPacket("/dealornodeal 2 %d 1 1" % numb)
				button.SetDownVisual("dealornodeal/removebox.png")
			
			button.Down()
			button.Disable()

		self.questionDialog.Close()
		self.questionDialog = None
		
	def RemoveBox(self, price):
		yang = 1000000
		carpan = 1
		if self.type == 2:
			checkText = localeInfo.NumberToMoneyStringKTM(yang * int(price))
		else:
			checkText = "%s Ejderha Parasý" % str(price)
		for i in xrange(12):
			if self.text[i].GetText() == checkText:
				self.text[i].SetText("")
				self.tab[i].Down()
				self.tab[i].Disable()
				break
			if self.text2[i].GetText() == checkText:
				self.text2[i].SetText("")
				self.tab2[i].Down()
				self.tab2[i].Disable()
				break
				
	def LeftBox(self, count):
		self.offer_text.SetText("Teklife Kalan")
		self.left_box.SetText("Son %d sandýk" % int(count))
		
	def OfferTime(self, offer):
		self.offer_text.SetText("Bankanýn Teklifi")
		if self.type == 2:
			yang = 1000000
			checkText = localeInfo.NumberToMoneyStringKTM(yang * int(offer))
			self.left_box.SetText(checkText)
		else:
			self.left_box.SetText("%d Ejderha Parasý" % int(offer))
		self.offer_time = 1

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Open(self, type):
		self.ClearDictionary()
		self.__Initialize()
		self.__Load()
		self.Show()
		# self.SendPopUp()
		self.InputCoin(type)
		self.type = type
		if type == 1:
			self.GetChild("titlename").SetText("Var Mýsýn? Yok Musun? (EP)")
		else:
			self.GetChild("titlename").SetText("Var Mýsýn? Yok Musun? (Yang)")
			self.price_type = "M Yang"
		
	def DealAccept(self, offer):
		self.offer_time = 0
		self.SendPopUp2(offer)
		
	def DealCancel(self,box):
		self.offer_time = 0
		self.LeftBox(box)
		
	def DealOpenMyBox(self,price):
		self.offer_time = 0
		wait = 10.0
		if self.type == 2:
			wait = 2.0;
		self.my_price = price
		self.popUpTimer = introLogin.ConnectingDialog()
		self.popUpTimer.Open(wait)
		self.popUpTimer.SetText("Kutu açýlýyor..")
		self.popUpTimer.SAFE_SetTimeOverEvent(self.OnEndCountDown)
		self.popUpTimer.SAFE_SetExitEvent(self.OnEndCountDown)
	
	def OnEndCountDown(self):
		self.SendPopUp2(self.my_price)

	def Close(self):
		self.Hide()
		
class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		print "NEW POPUP DIALOG ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		self.CloseEvent = 0

	def __del__(self):
		print "---------------------------------------------------------------------------- DELETE POPUP DIALOG "
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

	def Open(self, Message, event = 0, ButtonName = localeInfo.UI_CANCEL):

		if True == self.IsShow():
			self.Close()

		self.Lock()
		self.SetTop()
		self.CloseEvent = event

		AcceptButton = self.GetChild("accept")
		AcceptButton.SetText(ButtonName)
		AcceptButton.SetEvent(ui.__mem_func__(self.Close))

		self.GetChild("message").SetText(Message)
		self.Show()

	def Close(self):

		if False == self.IsShow():
			self.CloseEvent = 0
			return

		self.Unlock()
		self.Hide()

		if 0 != self.CloseEvent:
			self.CloseEvent()
			self.CloseEvent = 0

	def Destroy(self):
		self.popupWindow.Destroy()
		self.popupWindow = 0
		self.Close()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True
