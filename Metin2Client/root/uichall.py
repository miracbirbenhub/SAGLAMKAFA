import app
import net
import item

import ui_offline as ui2
import ui
import uiToolTip
import constInfo
import localeInfo
import wndMgr
import chat

class ChallWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.HideToolTip()
		self.itemStackalbeBuyDialog = None
		self.tab = {}
		self.price = {}
		self.price2 = {}
		self.sellButton = {}
		self.item = {}
		self.itemSlot = {}
		self.moneyicon = {}
		self.ilk = 0
		self.gosterdim = 0
		self.yuzdekac = 0
		constInfo.CHAL_DATA = []
		net.SendChatPacket("/chal_ver 0")

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Show2(self):	
		self.ScrollBar.SetMiddleBarSize(float(6) / float(len(constInfo.CHAL_DATA)))
		for i in range(6):
			self.MakeButton(
				i,\
				self.board,\
				13, 33 + (41 * i)
			)

		
	def Show(self):
		self.LoadWindow()
		self.SetCenterPosition()
		self.select = None
		ui.ScriptWindow.Show(self)
		
	def Open(self):
		self.Show()
		self.SetCenterPosition()
		self.SetTop()
		
	def LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/chall.py")
		except:
			import exception
			exception.Abort("chall.LoadWindow.LoadObject")
		try:
			self.titleBar = self.GetChild("TitleBar")
			self.board = self.GetChild("board")
			self.ScrollBar = self.GetChild("ScrollBar")
			self.refreshButton=self.GetChild("refresh")
			self.yuzde=self.GetChild("yuzdelik")
			self.yuzde.Hide()
	
			self.ScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
			self.refreshButton.SetEvent(ui.__mem_func__(self.__OnRefresh))

		except:
			import exception
			exception.Abort("chall.__LoadWindow.BindObject")
	
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))	
		
		self.yenile = app.GetTime()+5
		
		
	def Close(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		if self.itemStackalbeBuyDialog:
			self.itemStackalbeBuyDialog.Close()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OnScroll(self):
		board_count = 6
		pos = int(self.ScrollBar.GetPos() * (len(constInfo.CHAL_DATA) - board_count))
		
		for i in xrange(board_count):
			realPos = i + pos
			self.MakeButton(
				realPos,\
				self.board,\
				13, 33 + (41 * i)
			)

	def MakeButton(self, index, parent, x, y):
		self.tab[index] = ui.MakeButton(parent, x, y, False, "dungeontimer/", "hover.tga", "active.tga", "hover.tga")

		itemID = constInfo.CHAL_DATA[index][0]
		gorev = str(constInfo.CHAL_DATA[index][1]).replace("#", " ")
		yapan = constInfo.CHAL_DATA[index][2]

		self.price[index] = ui.TextLine()
		self.price[index].SetParent(self.tab[index])
		#self.price[index].SetPosition(80, 8)
		self.price[index].SetPosition(10, 8)
		self.price[index].SetText(gorev)
		self.price[index].Show()
		
		self.price2[index] = ui.TextLine()
		self.price2[index].SetParent(self.tab[index])
		#self.price[index].SetPosition(80, 8)
		self.price2[index].SetPosition(100, 8)
		self.price2[index].SetText(": " + str(yapan))
		self.price2[index].Show()
		
		self.sellButton[index] = ui.Button()
		self.sellButton[index].SetParent(self.tab[index])
		#self.sellButton[index].SetPosition(10, 8)
		self.sellButton[index].SetPosition(185, 8)
		self.sellButton[index].SetUpVisual("d:/ymir work/battle_pass/reward_normal.tga")
		self.sellButton[index].SetOverVisual("d:/ymir work/battle_pass/reward_over.tga")
		self.sellButton[index].SetDownVisual("d:/ymir work/battle_pass/reward_down.tga")
		self.sellButton[index].SetToolTipText("Ödülü Al")
		self.sellButton[index].SetEvent(ui.__mem_func__(self.acceptButtonEvent), itemID)
		self.sellButton[index].Show()	
		self.sellButton[index].SetTop()
	
	
	def acceptButtonEvent(self, gelen):
		net.SendChatPacket("/chal_ver " + str(gelen))
		
	def __OnRefresh(self):
		if self.yenile > app.GetTime():
			chat.AppendChat(chat.CHAT_TYPE_INFO, "5 saniyede bir listeyi güncelleyebilirsiniz. Kalan Süre : "+str(int(self.yenile)-int(app.GetTime())))
		else:
			constInfo.CHAL_DATA = []
			net.SendChatPacket("/chal_ver 0")
			self.yuzde = 0
			self.ilk = 0
			self.gosterdim = 0
			self.yenile = app.GetTime()+5
			self.Close()
			self.Open()
		
	def OnUpdate(self):
		if self.ilk == 1:
			if self.gosterdim == 0:
				self.Show2()
				self.OnScroll()
				self.gosterdim = 1
			else:
				return
		else:
			if self.yuzdekac < 102:
				self.GetChild("ScrollBar").Hide()
				self.GetChild("yuzdelik").Show()
				self.GetChild("yuzdelik").SetFontName("Tahoma:25")
				self.GetChild("yuzdelik").SetText("%"+str(self.yuzdekac))
				self.yuzdekac += 1
			else:
				self.GetChild("yuzdelik").Hide()
				self.GetChild("ScrollBar").Show()
				self.ilk = 1
				self.yuzdekac = 0

	def OverInItem(self, slotindex, index, itemVnum):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(itemVnum)

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def OnCancel(self):
		self.Hide()
		return True
	