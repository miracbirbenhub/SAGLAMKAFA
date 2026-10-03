import app
import ui
import uiToolTip
import localeInfo
from _weakref import proxy
from itertools import islice
import calendar

class EventTakvim(ui.ScriptWindow):
	class SearchResultItem(ui.Window):

		def __init__(self, parent, index):
			ui.Window.__init__(self)
			
			self.parent = parent
			
			self.isLoad = True
			self.isSelected = False
			
			self.index = index

			self.SetParent(parent)
			self.InitItem()

		def InitItem(self):
			startX = 0
			yPos = 0

			self.eventScreen = ui.MakeImageBox(self, "d:/ymir work/ui/EventPublic/normal.tga", 0, 3)
			self.eventScreen.SAFE_SetStringEvent("MOUSE_LEFT_UP",self.__OnSelect)
			self.eventScreen.SetTop()
			self.eventScreen.Show()
			
			self.text = ui.TextLine()
			self.text.SetParent(self)
			self.text.SetPosition(35, 6)
			self.text.Show()

			self.text1 = ui.TextLine()
			self.text1.SetParent(self)
			self.text1.SetPosition(145, 6)
			self.text1.Show()

			self.text2 = ui.TextLine()
			self.text2.SetParent(self)
			self.text2.SetPosition(155+100, 6)
			self.text2.Show()

			self.text3 = ui.TextLine()
			self.text3.SetParent(self)
			self.text3.SetPosition(205+110, 6)
			self.text3.Show()
			self.SetSize(self.eventScreen.GetWidth(), self.eventScreen.GetHeight())

			
		def SetEvents(self, name):
			self.text.SetText(name)

		def SetDaysName(self, name):
			self.text1.SetText(name)

		def SetBasla(self, name):
			self.text2.SetText(name)

		def SetBitir(self, name):
			self.text3.SetText(name)

		def __OnSelect(self):
			self.parent.OnSearchResultItemSelect(self.index)

		def Select(self):

			self.isSelected = True
			self.isLoad = True

		def UnSelect(self):
			self.isSelected = False
			self.isLoad = True

		def OnRender(self):
			if self.isLoad:
				if self.isSelected:
					self.eventScreen.LoadImage("d:/ymir work/ui/EventPublic/active.tga")
				else:
					self.eventScreen.LoadImage("d:/ymir work/ui/EventPublic/normal.tga")
				self.isLoad = False

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		

		
		
		self.selectedItemIndex = -1
		self.board = None
		self.secilen = None

		self.searchResultItems = []

		self.itemDataList = []
		
		self.currentPage = 1
		self.pageCount = 1
		self.perPage = 10
		self.itemCount = 0
		
		self.LoadWindow()

	def __del__(self):
		self.Destroy()
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/eventtakvim.py")
		except:
			import exception
			exception.Abort("EventTakvim.LoadDialog.LoadScript")
		try:
			GetObject						=self.GetChild
			self.board						= GetObject("board")
			self.eventno					= GetObject("eventno")
			self.eventdrop					= GetObject("eventdrop")
			self.eventlevel					= GetObject("eventlevel")
			self.sunucusaat					= GetObject("sunucusaat")
			self.eventname					= GetObject("eventname")
			self.girisslot					= GetObject("girisslot")
			self.questScrollBar				= self.GetChild("info_ScrollBar")
			self.girisitemtext				= self.GetChild("girisitemtext")
			self.questShowingStartIndex		= 0
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
			
			self.board.SetCloseEvent(ui.__mem_func__(self.__OnCloseButtonClick))

		except:
			import exception
			exception.Abort("EventTakvim.LoadDialog.BindObject")

		self.girisslot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
		self.girisslot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.searchResultItems[:]				= [] 
		self.titleBar							= None
		self.questScrollBar						= None
		self.questShowingStartIndex				= None

	def OnQuestScroll(self):
		questCount = len(calendar.EventCalendar)
		scrollLineCount = max(0, questCount - 11)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshInfo()

	def RefreshInfo(self):
		questCount = len(calendar.EventCalendar)
		questRange = range(1)
		self.searchResultItems[:] = []
		
		if questCount > 11:
			self.questScrollBar.Show()
		else:
			self.questScrollBar.Hide()

		basePos = 60
		for i in range(0+self.questShowingStartIndex, 11+self.questShowingStartIndex):
			resultItem = EventTakvim.SearchResultItem(self, i)
			resultItem.SetPosition(136-112, basePos+((i-self.questShowingStartIndex)*24))
			resultItem.SetEvents(calendar.EventCalendar[i][0])
			resultItem.SetDaysName(calendar.EventCalendar[i][5])
			resultItem.SetBasla(calendar.EventCalendar[i][6])
			resultItem.SetBitir(calendar.EventCalendar[i][7])
			resultItem.Show()
			self.searchResultItems.append(resultItem)
		self.Children.append(self.searchResultItems)

	def Open(self):	
		self.selectedItemIndex = -1
		self.Show()
		self.SetCenterPosition()
		basePos = 60
		for i in range(0, 11):
			resultItem = EventTakvim.SearchResultItem(self, i)
			resultItem.SetPosition(136-112, basePos+(i*36))
			resultItem.SetEvents(calendar.EventCalendar[i][0])
			resultItem.SetDaysName(calendar.EventCalendar[i][5])
			resultItem.SetBasla(calendar.EventCalendar[i][6])
			resultItem.SetBitir(calendar.EventCalendar[i][7])
			resultItem.Show()
			self.searchResultItems.append(resultItem)
		self.Children.append(self.searchResultItems)
		self.OnSearchResultItemSelect(0+self.questShowingStartIndex)
		if len(calendar.EventCalendar) > 11:
			self.questScrollBar.Show()
		else:
			self.questScrollBar.Hide()
		self.questScrollBar.SetPos(0)
		self.RefreshInfo()
		self.OnSearchResultItemSelect(0+self.questShowingStartIndex)

	def OnUpdate(self):
		import time
		# FurkoSaat = time.strftime("|cffffcc00%H:%M:%S")
		# self.sunucusaat.SetText(FurkoSaat)

	def OnSearchResultItemSelect(self, index):
		if self.questShowingStartIndex > 0:
			self.selectedItemIndex = index - self.questShowingStartIndex
		else:
			self.selectedItemIndex = index
		self.secilen = index

		self.girisslot.Show()
		self.girisitemtext.Show()
		map(EventTakvim.SearchResultItem.UnSelect,  self.searchResultItems)
		self.searchResultItems[self.selectedItemIndex].Select()
		# self.eventno.SetText(localeInfo.EVENTS_NAME1+str(calendar.EventCalendar[index][1]))
		# self.eventdrop.SetText(localeInfo.EVENTS_NAME2+str(calendar.EventCalendar[index][2]))
		# self.eventlevel.SetText(localeInfo.EVENTS_NAME3+str(calendar.EventCalendar[index][3]) + " - " + str(calendar.EventCalendar[index][4]))

		self.eventname.SetText(str(calendar.EventCalendar[index][5]))
		if int(calendar.EventCalendar[index][8]) == 0:
			self.girisslot.SetItemSlot(0, 0)
		else:
			self.girisslot.SetItemSlot(0, int(calendar.EventCalendar[index][8]),int(calendar.EventCalendar[index][9]))
		self.girisslot.RefreshSlot()

	def __OnOverInItem(self, index):
		import uiToolTip
		self.tooltipItem.SetItemToolTip(calendar.EventCalendar[index][8])

	def __OnOverOutItem(self):
		self.tooltipItem.HideToolTip()		

	def Close(self):
		map(EventTakvim.SearchResultItem.Hide, self.searchResultItems)
		self.Hide()


	def Clear(self):
		self.Refresh()

	def Refresh(self):
		pass

	def __OnCloseButtonClick(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()

