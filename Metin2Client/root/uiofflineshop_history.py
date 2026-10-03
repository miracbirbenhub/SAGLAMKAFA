import app
import player
import net
import offlineshop
import ui
import item

import uiToolTip
import localeInfo
import ime
import uiPickMoney
import grp
import mouseModule

from _weakref import proxy

PATH_ROOT = "cream/shopeditor/"
PATH_ROOT_SEARCH = "cream/searchshop/"

class HistoryWindow(ui.Window):
	class NewItem(ui.Window):
		def __init__(self, index, data):
			ui.Window.__init__(self)
			self.background = None
			self.bSelected = False
			self.OnResetThings()
			self.Index = index
			self.Data = data

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			if self.Index != 0:
				self.background.LoadImage(PATH_ROOT + "bar_without_top.tga")
			else:
				self.background.LoadImage(PATH_ROOT + "bar_complete.tga")
				
			self.background.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverInImage)
			self.background.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOutImage)
			self.background.Show()

			self.SetSize(self.background.GetWidth(), 26)

			self.wndIcon = ui.ExpandedImageBox()
			self.wndIcon.SetParent(self)
			self.wndIcon.AddFlag("not_pick")
			self.wndIcon.LoadImage(PATH_ROOT_SEARCH + "yang.dds")
			self.wndIcon.SetPosition(26, 7)
			self.wndIcon.SetWindowHorizontalAlignRight()
			self.wndIcon.Show()

			item.SelectItem(data["vnum"])
			
			itemName = item.GetItemName()
			itemName = itemName if len(itemName) < 15 else itemName[:15] + "..."
			
			self.wndName = ui.MakeTextLineNew(self, 6, 6, self.HasAttrItem(data) + itemName)
			self.wndPrice = ui.MakeTextLineNew(self, 35, 6, localeInfo.NumberToMoneyString(data["price"]))
			self.wndPrice.SetWindowHorizontalAlignRight()
			self.wndPrice.SetHorizontalAlignRight()
			
			self.wndReason = ui.MakeTextLineNew(self, 0, 6, "Eþya Satýldý")
			self.wndReason.SetWindowHorizontalAlignCenter()
			self.wndReason.SetHorizontalAlignCenter()
			
			self.OnMouseOverOutImage()

		def HasAttrItem(self, Data):
			attrs	= [(Data["attr"][num]['type'], Data["attr"][num]['value']) for num in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			if attrs:
				for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					apply = attrs[i][0]
					if 0 > apply:
						return "|cFFFFC700"

			return "|cFFF1E6C0"

		def __del__(self):
			ui.Window.__del__(self)

		def OnMouseOverInImage(self):
			if self.tooltipItem:
				sockets = [self.Data["socket"][num] for num in xrange(player.METIN_SOCKET_MAX_NUM)]
				attrs	= [(self.Data["attr"][num]['type'], self.Data["attr"][num]['value']) for num in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
				self.tooltipItem.ClearToolTip()
				
				self.tooltipItem.AppendIcon(self.Data["vnum"], self.Data["count"])
				self.tooltipItem.AddItemData(self.Data["vnum"], sockets, attrs)
				
				self.tooltipItem.UpdateRect()
				
			self.background.SetAlpha(1.0)

		def OnMouseOverOutImage(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
				
			self.background.SetAlpha(0.8)

		def SetItemToolTip(self, tooltip):
			self.tooltipItem = tooltip

		def OnResetThings(self):
			self.IsSelected = False
			self.bIsBlocked = False
			self.vnum = 0
			self.xBase = 0
			self.yBase = 0

			self.clickEvent = None
			if self.background != None:
				self.background.Hide()
			self.background = None
			self.wndIcon = None
			self.tooltipItem = None
			self.Data = None

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetClickEvent(self, event):
			self.clickEvent = event
		
		def Destroy(self):
			self.OnResetThings()
		
		def OnRender(self):
			xList, yList = self.parent.GetGlobalPosition()
			widthList, heightList = self.parent.GetWidth(), self.parent.GetHeight()	

			images = [self.background, self.wndIcon]
			for img in images:
				if img:
					img.SetClipRect(xList, yList, xList + widthList, yList + heightList)

			textList = [self.wndName, self.wndPrice, self.wndReason]
			for text in textList:
				if text:
					xText, yText = text.GetGlobalPosition()

					if yText < yList or yText + text.GetTextSize()[1] > yList + heightList:
						text.Hide()
					else:
						text.Show()

	def __init__(self):
		ui.Window.__init__(self)
		self.OnResetThings()

	def __del__(self):
		ui.Window.__del__(self)
		self.OnResetThings()
		
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip
		
	def Destroy(self):
		self.OnResetThings()
		
	def OnResetThings(self):
		self.SetFuncDown = None
		self.SelectIndexFunc = None
		self.itemList = []
		self.scrollBar = None

		self.selectEvent = None
		self.tooltipItem = None
	
	def SetEventSelect(self, event):
		self.SelectIndexFunc = event

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scrollBar.SetScrollStep(0.2)
		self.scrollBar=scrollBar

	def SetSelectEvent(self, event):
		self.selectEvent = event
		
	def __OnScroll(self):
		self.RefreshItemPosition(True)
			
	def GetTotalHeightItems(self):
		totalHeight = 0
		
		if self.itemList:
			for itemH in self.itemList:
				totalHeight += itemH.GetHeight()
			
		return totalHeight

	def GetItemCount(self):
		return len(self.itemList)

	def AppendItem(self, index, data):
		item = self.NewItem(index, data)
		item.SetParent(self)
		item.SetItemToolTip(self.tooltipItem)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.Show()
		self.itemList.append(item)

		self.ResetPosScrollBar()
		self.ResizeScrollBar()	
		self.RefreshItemPosition()
		
		if len(self.itemList) <= 13:
			self.scrollBar.Hide()
		else:
			self.scrollBar.Show()

	def ResizeScrollBar(self):
		totalHeight = float(self.GetTotalHeightItems())
		if totalHeight:
			scrollBarHeight = min(float(self.GetHeight() - 10) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
			
		self.scrollBar.SetMiddleBarSize(scrollBarHeight)
	
	def ResetPosScrollBar(self):
		self.scrollBar.SetPos(0)

	def RefreshItemPosition(self, bScroll = False):		
		scrollPos = self.scrollBar.GetPos()
		totalHeight = self.GetTotalHeightItems() - self.GetHeight()

		idx, CurIdx, yAccumulate = 0, 0, 0
		for item in self.itemList[idx:]:
			if bScroll:
				setPos = yAccumulate - int(scrollPos * totalHeight)
				item.SetPosition(0, setPos)
			else:
				item.SetPosition(0, yAccumulate)
				
			item.SetBasePosition(0, yAccumulate)

			CurIdx += 1
			yAccumulate += item.GetHeight()

	def Clear(self):
		range = len(self.itemList)
		
		if range > 0:
			for item in self.itemList:
				item.OnResetThings()
				item.Hide()
				del item

		self.itemList = []
