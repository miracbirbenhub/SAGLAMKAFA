import ui
import item
import net
import constInfo
import localeInfo
import uiCommon
import wndMgr
import app
import grp
import chat
import player
import skill
import shop
import chr
import math
from _weakref import proxy
from operator import truediv

import offlineshop
import uiToolTip
import ime
import dbg

PATH = "cream/"
PATH_ROOT = "cream/searchshop/"
TIME_WAIT = 5 # Seconds
MAX_ITEMS_APPEND = 25
SELECTED_ITEMS_BUY = {}

# Config Categories
def SetCategories(wnd):
	wnd.AppendItem("Ekipman", "2.dds", 89, -1, -1, False, True)
	wnd.AppendSubCategory("Silah", 89, item.ITEM_TYPE_WEAPON)
	wnd.AppendSubCategory("Zýrh", 89, item.ITEM_TYPE_ARMOR, item.ARMOR_BODY)
	wnd.AppendSubCategory("Kask", 89, item.ITEM_TYPE_ARMOR, item.ARMOR_HEAD)
	wnd.AppendSubCategory("Kalkan", 89, item.ITEM_TYPE_ARMOR, item.ARMOR_SHIELD)
	wnd.AppendSubCategory("Küpe", 89, item.ITEM_TYPE_ARMOR, item.ARMOR_EAR)
	wnd.AppendSubCategory("Kolye", 89, item.ITEM_TYPE_ARMOR, item.ARMOR_NECK)
	wnd.AppendSubCategory("Bilezik", 89, item.ITEM_TYPE_ARMOR, item.ARMOR_WRIST)
	wnd.AppendSubCategory("Ayakkabý", 89, item.ITEM_TYPE_ARMOR, item.ARMOR_FOOTS)

	wnd.AppendItem("Kostüm", "4.dds", 88, -1, -1, False, True)
	wnd.AppendSubCategory("Saç", 88, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_HAIR)
	wnd.AppendSubCategory("Zýrh", 88, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_BODY)
	# wnd.AppendSubCategory("Sash", 88, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_SASH)
	# wnd.AppendSubCategory("Weapon", 88, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_WEAPON)

	# wnd.AppendItem("Chest", "8.dds", item.ITEM_TYPE_GIFTBOX)
	wnd.AppendItem("Beceri Kitabý", "6.dds", item.ITEM_TYPE_SKILLBOOK)
	wnd.AppendItem("Taþ", "3.dds", item.ITEM_TYPE_METIN)
	wnd.AppendItem("+Basma", "9.dds", item.ITEM_TYPE_MATERIAL)
	# wnd.AppendItem("Blend", "6.dds", item.ITEM_TYPE_BLEND)

class ListBoxCategory(ui.Window):
	class NewItem(ui.Window):
		def __init__(self, parent, icon, name, type, ForType, Subtype, IsSubCategory, ArrowShow):
			ui.Window.__init__(self)

			self.ImageSubCat = None
			self.background = None
			self.Arrow = None
			self.IconCategory = None			
			self.OnInit()

			self.Type = type
			self.ForType = ForType
			self.Subtype = Subtype
			self.IsSubCategory = IsSubCategory
			self.IsExpanded = False
			self.IsVisible = False

			if IsSubCategory == False:
				self.AppendCategory(parent.hWnd, icon, name, type, ArrowShow)
			else:
				self.AppendSubCategory(parent.hWnd, name, ForType)
				

		def OnRender(self):
			xList, yList = self.parent.GetGlobalPosition()
			widthList, heightList = self.parent.GetWidth(), self.parent.GetHeight()	
		
			images = [self.background, self.IconCategory, self.Arrow]
			for img in images:
				if img:
					img.SetClipRect(xList, yList, xList + widthList, yList + heightList)
		
			textList = [self.NameCategory]
			for text in textList:
				if text:
					xText, yText = text.GetGlobalPosition()
		
					if yText < yList or yText + text.GetTextSize()[1] > yList + heightList:
						text.Hide()
					else:
						text.Show()
		
		def AppendCategory(self, parent, icon, name, type, ArrowShow):
			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.background.LoadImage(PATH_ROOT + "category_norm.dds")
			self.background.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn2)
			self.background.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOut2)
			self.background.OnMouseLeftButtonDown = ui.__mem_func__(self.OnSelectImageBox)
			self.background.Show()
			
			self.SetSize(self.background.GetWidth(), self.background.GetHeight())

			self.IconCategory = ui.ExpandedImageBox()
			self.IconCategory.SetParent(self)
			self.IconCategory.LoadImage(PATH_ROOT + icon)
			self.IconCategory.SetPosition(4, 3)
			self.IconCategory.Show()
		
			if ArrowShow:
				self.Arrow = ui.ExpandedImageBox()
				self.Arrow.SetParent(self.background)
				self.Arrow.LoadImage(PATH_ROOT + "arrow_down.dds")
				self.Arrow.SetPosition(144, 10)
				self.Arrow.Show()

			self.NameCategory = ui.TextLine()
			self.NameCategory.SetParent(self.background)
			self.NameCategory.SetVerticalAlignCenter()	
			self.NameCategory.SetWindowVerticalAlignCenter()
			self.NameCategory.SetText(name)
			self.NameCategory.SetPosition(40, -1)
			self.NameCategory.Show()
			
			self.SubTypes = {}

		def AppendSubCategory(self, parent, name, ForType):
			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.background.LoadImage(PATH_ROOT + "sub_category_norm.dds")
			self.background.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn2)
			self.background.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOut2)
			self.background.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftButtonDown)
			self.background.SetPosition(0, 0)
			self.background.Show()
			
			self.SetSize(self.background.GetWidth() + 2, self.background.GetHeight())
		
			self.NameCategory = ui.TextLine()
			self.NameCategory.SetParent(self)
			self.NameCategory.SetText(name)
			self.NameCategory.SetPosition(0, 3)
			self.NameCategory.SetHorizontalAlignCenter()	
			self.NameCategory.SetWindowHorizontalAlignCenter()
			self.NameCategory.Show()

		def SetVisible(self, flag):
			self.IsVisible = flag

		def GetItemType(self):
			return self.ForType
		
		def CanRender(self):
			if self.NameCategory.IsShow():
				return True
				
			return False
		
		def IsHide(self):
			return self.IsVisible

		def IsExpanded(self):
			return self.IsExpanded
		
		def SetSelectReset(self):
			self.selected = False
		
			if self.IsSubCategory:
				self.background.LoadImage(PATH_ROOT + "sub_category_norm.dds")
			else:
				self.background.LoadImage(PATH_ROOT + "category_norm.dds")
		
		def OnMouseOverIn2(self):
			if self.selected:
				return
		
			if self.IsSubCategory == False:
				if self.Arrow == None:
					self.background.LoadImage(PATH_ROOT + "category_hover.dds")
				return
				
			self.background.LoadImage(PATH_ROOT + "sub_category_hover.dds")
			
		def OnMouseOverOut2(self):
			if self.IsSubCategory == False:
				if self.Arrow == None:
					if self.selected:
						self.background.LoadImage(PATH_ROOT + "category_down.dds")
						return
				
					self.background.LoadImage(PATH_ROOT + "category_norm.dds")
				return
				
			if self.selected:
				self.background.LoadImage(PATH_ROOT + "sub_category_down.dds")
			else:
				self.background.LoadImage(PATH_ROOT + "sub_category_norm.dds")
		
		def OnMouseLeftButtonDown(self):
			if self.IsSubCategory == False:
				return
			
			if self.clickEvent:
				self.clickEvent(self.ForType, self.Type, self.Subtype, False)
	
			self.selected = True
			self.background.LoadImage(PATH_ROOT + "sub_category_down.dds")

		def OnSelectImageBox(self):
			if self.IsSubCategory:
				return

			if self.IsExpanded:
				self.IsExpanded = False
				if self.Arrow:
					self.Arrow.LoadImage(PATH_ROOT + "arrow_down.dds")
			else:
				self.IsExpanded = True
				if self.Arrow:
					self.Arrow.LoadImage(PATH_ROOT + "arrow_up.dds")

			if self.clickEvent:
				self.clickEvent(99, self.Type, 0, self.IsExpanded)
				
				if self.Arrow == None:
					self.selected = True
					self.background.LoadImage(PATH_ROOT + "category_down.dds")

		def __del__(self):
			ui.Window.__del__(self)
			self.OnInit()

		def OnInit(self):
			self.selected = False
			self.vnum = 0
			self.xBase = 0
			self.yBase = 0

			self.overInEvent = None
			self.overOutEvent = None
			self.clickEvent = None
			self.NameCategory = None
			if self.background != None:
				self.background.Hide()
			self.background = None
			self.Arrow = None
			self.ImageSubCat = None
			self.IconCategory = None

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEvent = event
			
		def SetOverOutEvent(self, event):
			self.overOutEvent = event
			
		def SetClickEvent(self, event):
			self.clickEvent = event
			
		def OnMouseOverIn(self):
			self.RefreshSelectState(True)
				
			if self.overInEvent:
				self.overInEvent(self.ItemVnum)
			
		def OnMouseOverOut(self):
			self.RefreshSelectState(False)
			
			if self.overOutEvent:
				self.overOutEvent()
				
		def IsSelected(self):
			return self.selected
				
		def RefreshSelectState(self, isIn):
			if not self.background:
				return
		
		def SetAnimWidth(self, width):
			self.widthAnim = width

	def __init__(self):
		ui.Window.__init__(self)
		self.OnInit()

	def __del__(self):
		ui.Window.__del__(self)
		self.OnInit()
		
	def Destroy(self):
		self.OnInit()

	def OnInit(self):
		self.SetFuncDown = None
		self.itemList = []
		self.scrollBar = None

		self.selectEvent = None
		self.selectedItemVnum = 0

	def SetEventDown(self, event):
		self.SetFuncDown = event

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)
		
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scrollBar.SetScrollStep(0.2)
		self.scrollBar=scrollBar

	def SetSelectEvent(self, event):
		self.selectEvent = event
		
	def __OnScroll(self):
		self.AdjustItemPositions(True)
			
	def GetTotalItemHeight(self):
		totalHeight = 0
		
		if self.itemList:
			for itemH in self.itemList:
				totalHeight += itemH.GetHeight() + 6
			
		return totalHeight + 2

	def GetItemCount(self):
		return len(self.itemList)
			
	def AppendItem(self, Name, IconImage, Type, ForType = -1, Subtype = -1, IsSubCategory = False, ShowArrow = False):
		item = self.NewItem(self, IconImage, Name, Type, ForType, Subtype, IsSubCategory, ShowArrow)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetClickEvent(ui.__mem_func__(self.SelectItem))
			
		item.Show()
		self.itemList.append(item)

		self.AdjustScrollBar()
		self.AdjustItemPositions()

	def SelectItem(self, ForType, Type, SubType, flag):
		for itemH in self.itemList:
			if ForType == 99:
				if itemH.GetItemType() == Type:
					itemH.SetVisible(flag)

			itemH.SetSelectReset()

		self.AdjustItemPositions(True)

		if Type == 0:
			self.SetFuncDown(-1, -1)
			return
		
		PassTypes = {item.ITEM_TYPE_GIFTBOX, item.ITEM_TYPE_SKILLBOOK, item.ITEM_TYPE_METIN, item.ITEM_TYPE_MATERIAL, item.ITEM_TYPE_BLEND}
		if ForType == 99 and (Type in PassTypes): 
			self.SetFuncDown(Type, -1)
			return

		if ForType != 99:
			self.SetFuncDown(Type, SubType)
		elif ForType == 99 and Type == -1:
			self.SetFuncDown(-1, -1)

	def AppendSubCategory(self, name, ForType, Type, Subtype = -1):
		self.AppendItem(name, None, Type, ForType, Subtype, 1)
	
	def AdjustScrollBar(self):
		totalHeight = float(self.GetTotalItemHeight())
		if totalHeight:
			scrollBarHeight = min(float(self.GetHeight() - 10) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
			
		self.scrollBar.SetMiddleBarSize(scrollBarHeight)
		
	def ResetScrollbar(self):
		self.scrollBar.SetPos(0)
				
	def AdjustItemPositions(self, scrolling = False, startIndex = -1):		
		scrollPos = self.scrollBar.GetPos()
		totalHeight = self.GetTotalItemHeight() - self.GetHeight()

		idx = 0
		if startIndex >= 0:
			idx = startIndex
		
		CurIdx, yAccumulate, FirstTab = 0, 0, False
		for item in self.itemList[idx:]:
			if startIndex >= 0:
				yAccumulate -= 20 + 2

			if item.IsHide():
				item.Hide()
				continue
			else:
				item.Show()
				
			if item.IsSubCategory == False and CurIdx > 0:
				yAccumulate += 7
				FirstTab = True
			else:
				yAccumulate += 1
				
				if FirstTab:
					yAccumulate += 5
					FirstTab = False
	
			if scrolling:
				setPos = yAccumulate - int(scrollPos * totalHeight)
				item.SetPosition(0, setPos)
			else:
				item.SetPosition(0, yAccumulate)
				
			item.SetBasePosition(0, yAccumulate)
			
			CurIdx += 1
			yAccumulate += 20

	def Clear(self):
		range = len(self.itemList)
		if range:
			for item in self.itemList:
				item.OnInit()
				item.Hide()
				del item
		
		self.itemList = []
		
	def GetList(self):
		return self.itemList


class ListBoxItem(ui.Window):
	class NewItem(ui.Window):
		def __init__(self, parent, index, info):
			ui.Window.__init__(self)
			self.background = None
			self.OnClear()
			self.Index = index
			self.InfoData = info

			Vnum = info["vnum"]
			count = info["count"]
		
			item.SelectItem(Vnum)
			_, self.itemSize = item.GetItemSize()
	
			price = info["price"]
			textYang = str(localeInfo.NumberToMoneyString(price))
			
			pid = 0

			name 	= info["owner_name"]
			seller	= name[:name.find('@')] if '@' in name else "NONAME"		
			name	= name[name.find('@')+1:] if '@' in name else name

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.OnMouseOverOut2()
			
			self.background.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn2)
			self.background.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOut2)
			self.background.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftButtonDown)
			self.background.Show()
			
			self.SetSize(self.background.GetWidth(), self.background.GetHeight())

			if count > 1:
				countText = str(count) + "x "
			else:
				countText = ""
				
			ItemName = item.GetItemName()
			
			if len(ItemName) >= 25:
				ItemName = ItemName[:25] + ".."

			self.ItemSlotBase = ui.ExpandedImageBox()
			self.ItemSlotBase.SetParent(self)
			self.ItemSlotBase.SetPosition(26, 0)
			self.ItemSlotBase.LoadImage(PATH + "slot_32x%d.tga" % (self.itemSize * 32))
			self.ItemSlotBase.SetWindowVerticalAlignCenter()
			self.ItemSlotBase.SAFE_SetStringEvent("MOUSE_OVER_IN", self.IconOnMouseOverIn)
			self.ItemSlotBase.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.IconOnMouseOverOut)
			self.ItemSlotBase.Show()

			self.ItemIcon = ui.ExpandedImageBox()
			self.ItemIcon.SetParent(self.ItemSlotBase)
			self.ItemIcon.AddFlag("not_pick")
			self.ItemIcon.LoadImage(item.GetIconImageFileName())
			self.ItemIcon.SetWindowVerticalAlignCenter()
			self.ItemIcon.SetWindowHorizontalAlignCenter()
			self.ItemIcon.Show()

			self.wndItemName = ui.TextLine()
			self.wndItemName.SetParent(self)
			self.wndItemName.AddFlag("not_pick")
			self.wndItemName.SetPosition(60, 0)
			self.wndItemName.SetText(str(countText) + ItemName)
			self.wndItemName.SetWindowVerticalAlignCenter()
			self.wndItemName.SetVerticalAlignCenter()
			self.wndItemName.Show()

			self.wndItemPrice = ui.TextLine()
			self.wndItemPrice.SetParent(self)
			self.wndItemPrice.AddFlag("not_pick")
			self.wndItemPrice.SetPosition(30, 0)
			self.wndItemPrice.SetText("|Eemoji/yang|e " + textYang)
			self.wndItemPrice.SetWindowHorizontalAlignCenter()
			self.wndItemPrice.SetHorizontalAlignCenter()
			self.wndItemPrice.SetWindowVerticalAlignCenter()
			self.wndItemPrice.SetVerticalAlignCenter()
			self.wndItemPrice.Show()

			self.CheckBox = ui.ExpandedImageBox()
			self.CheckBox.SetParent(self)
			self.CheckBox.SetPosition(6, 0)
			self.CheckBox.LoadImage(PATH_ROOT + "box_uncheck.dds")
			self.CheckBox.SetWindowVerticalAlignCenter()
			self.CheckBox.OnMouseLeftButtonDown = ui.__mem_func__(self.OnCheckBox)
			self.CheckBox.Show()
	
			self.wndSellerName = ui.TextLine()
			self.wndSellerName.SetParent(self)
			self.wndSellerName.AddFlag("not_pick")
			self.wndSellerName.SetPosition(13, 0)
			self.wndSellerName.SetText(str(seller))
			self.wndSellerName.SetWindowHorizontalAlignRight()
			self.wndSellerName.SetHorizontalAlignRight()
			self.wndSellerName.SetWindowVerticalAlignCenter()
			self.wndSellerName.SetVerticalAlignCenter()
			self.wndSellerName.Show()

			self.IconWhisperSeller = ui.ExpandedImageBox()
			self.IconWhisperSeller.SetParent(self)
			self.IconWhisperSeller.SetPosition(self.wndSellerName.GetTextSize()[0] + 30, 2)
			self.IconWhisperSeller.LoadImage(PATH_ROOT + "messenger.dds")
			self.IconWhisperSeller.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftWhisperSeller)
			self.IconWhisperSeller.SetWindowHorizontalAlignRight()
			self.IconWhisperSeller.SetWindowVerticalAlignCenter()
			self.IconWhisperSeller.Show()
			
			if self.InfoData["id"] in SELECTED_ITEMS_BUY:
				self.IsSelected = True
				self.CheckBox.LoadImage(PATH_ROOT + "box_checked.dds")
				
			self.OnMouseOverOut2()

		def OnRender(self):
			xList, yList = self.parent.GetGlobalPosition()
			widthList, heightList = self.parent.GetWidth(), self.parent.GetHeight()	
		
			images = [self.background, self.CheckBox, self.ItemSlotBase, self.ItemIcon, self.IconWhisperSeller]
			for img in images:
				if img:
					img.SetClipRect(xList, yList, xList + widthList, yList + heightList)
		
			textList = [self.wndItemName, self.wndItemPrice, self.wndSellerName]
			for text in textList:
				if text:
					xText, yText = text.GetGlobalPosition()
		
					if yText < yList or yText + text.GetTextSize()[1] > yList + heightList:
						text.Hide()
					else:
						text.Show()

		def OnMouseOverIn2(self):
			self.background.LoadImage(PATH_ROOT + "field_%d_selected.dds" % (self.itemSize))

		def OnMouseOverOut2(self):
			if self.IsSelected:
				self.background.LoadImage(PATH_ROOT + "field_%d_selected.dds" % (self.itemSize))
				return
		
			colorField = "black"
			if self.Index % 2 == 0:
				colorField = "white"
		
			self.background.LoadImage(PATH_ROOT + "field_%d_%s.dds" % (self.itemSize, colorField))

		def SetBlock(self):
			self.bIsBlocked = True
		
		def OnCheckBox(self):
			if self.IsSelected:
				self.IsSelected = False
				self.CheckBox.LoadImage(PATH_ROOT + "box_uncheck.dds")
				
				if self.InfoData["id"] in SELECTED_ITEMS_BUY:
					del SELECTED_ITEMS_BUY[self.InfoData["id"]]
			else:
				self.IsSelected = True
				self.CheckBox.LoadImage(PATH_ROOT + "box_checked.dds")

				SELECTED_ITEMS_BUY[self.InfoData["id"]] = self.InfoData["owner"]
				
			self.OnMouseOverOut2()
		
		def OnMouseLeftWhisperSeller(self):
			if self.WhisperEvent:
				self.WhisperEvent(self.wndSellerName.GetText())

		def OnMouseLeftButtonDown(self):
			if self.clickEvent:
				self.clickEvent(self.InfoData["owner"], self.InfoData["id"], self.wndItemName.GetText(), self.InfoData["price"])

		def __del__(self):
			ui.Window.__del__(self)
			self.OnClear()

		def OnClear(self):
			self.IsSelected = False
			self.bIsBlocked = False
			self.vnum = 0
			self.xBase = 0
			self.yBase = 0

			self.overInEventIconImage = None
			self.overOutEventIconImage = None
			self.clickEvent = None
			self.WhisperEvent = None
			if self.background != None:
				self.background.Hide()
			self.background = None
			self.CheckBox = None
			self.ItemSlotBase = None

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEventIconImage = event
			
		def SetOverOutEvent(self, event):
			self.overOutEventIconImage = event
			
		def SetClickEvent(self, event):
			self.clickEvent = event

		def SetWhisperEvent(self, event):
			self.WhisperEvent = event
			
		def IconOnMouseOverIn(self):
			if self.overInEventIconImage:
				self.overInEventIconImage(self.InfoData)
			
		def IconOnMouseOverOut(self):
			if self.overOutEventIconImage:
				self.overOutEventIconImage()

	def __init__(self):
		ui.Window.__init__(self)
		self.OnClear()
		
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

	def __del__(self):
		ui.Window.__del__(self)
		self.OnClear()
		
		self.tooltipItem = None
		
	def Destroy(self):
		self.tooltipItem = None
		self.OnClear()
		
	def OnClear(self):
		self.SetFuncDown = None
		self.BuyAskEvent = None
		self.WhishperEventFunc = None
		self.itemList = []
		self.scrollBar = None

		self.selectEvent = None
		self.selectedItemVnum = 0

	def SetEventBuy(self, event):
		self.BuyAskEvent = event

	def SetEventWhisper(self, event):
		self.WhishperEventFunc = event

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)
		
		self.SetPosition(5, 5)
		self.SetSize(parent.GetWidth() - 10, parent.GetHeight() - 10)
		
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scrollBar.SetScrollStep(0.2)
		self.scrollBar=scrollBar

	def SetSelectEvent(self, event):
		self.selectEvent = event
		
	def __OnScroll(self):
		self.AdjustItemPositions(True)
			
	def GetTotalItemHeight(self):
		totalHeight = 0
		
		if self.itemList:
			for itemH in self.itemList:
				if itemH.bIsBlocked:
					continue
				totalHeight += itemH.GetHeight() + 2
			
		return totalHeight

	def GetItemCount(self):
		return len(self.itemList)

	def AppendItem(self, index, infoData):
		item = self.NewItem(self, index, infoData)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetWhisperEvent(ui.__mem_func__(self.OnWhisperName))
		item.SetClickEvent(ui.__mem_func__(self.SelectItem))
		item.SetOverInEvent(ui.__mem_func__(self.OverInItem))
		item.SetOverOutEvent(ui.__mem_func__(self.OverOutItem))		
	
		item.Show()
		self.itemList.append(item)

		self.ResetScrollbar()
		self.AdjustScrollBar()	
		self.AdjustItemPositions()
	
	def OnWhisperName(self, name):
		if self.WhishperEventFunc:
			self.WhishperEventFunc(name)
	
	def OverInItem(self,info):

		if not self.tooltipItem.IsShow():
			# info = self.slotInfo
			sockets = [info["socket"][num] for num in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrs	= [(info["attr"][num]['type'], info["attr"][num]['value']) for num in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			evolution = info.get('evolution',1)#silah evrim

			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(info["vnum"], sockets, attrs, evolution)

			self.tooltipItem.AppendPrice(info["price"])

			self.tooltipItem.Show()
	
	# def OverInItem(self):
		# if self.tooltipItem:
			# self.tooltipItem.ClearToolTip()
			
			# sockets = []
			# for i in xrange(player.METIN_SOCKET_MAX_NUM):
				# sockets.append(0)

			# vnum = []
			# for i in xrange(player.METIN_SOCKET_MAX_NUM):
				# vnum.append(0)

			# attrs = []
			# for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				# attrs.append((0, 0))
			# self.tooltipItem.AddItemData(vnum, sockets, attrs)
			
			# self.tooltipItem.AddItemData(info["vnum"], metinSlot, attrSlot)	

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def SelectItem(self, pID, ItemPos, ItemName, itemPrice):
		if self.BuyAskEvent:
			self.BuyAskEvent(pID, ItemPos, ItemName, itemPrice)

	def AdjustScrollBar(self):
		totalHeight = float(self.GetTotalItemHeight())
		if totalHeight:
			scrollBarHeight = min(float(self.GetHeight() - 10) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
			
		self.scrollBar.SetMiddleBarSize(scrollBarHeight)
	
	def ResetScrollbar(self):
		self.scrollBar.SetPos(0)
				
	def AdjustItemPositions(self, scrolling = False):		
		scrollPos = self.scrollBar.GetPos()
		totalHeight = self.GetTotalItemHeight() - self.GetHeight()

		idx = 0

		CurIdx, yAccumulate = 0, 0
		for item in self.itemList[idx:]:
			if item.bIsBlocked:
				continue
			
			if scrolling:
				setPos = yAccumulate - int(scrollPos * totalHeight)
				item.SetPosition(0, setPos)
			else:
				item.SetPosition(0, yAccumulate)
				
			item.SetBasePosition(0, yAccumulate)

			CurIdx += 1
			yAccumulate += item.GetHeight() + 2

	def Clear(self):
		range = len(self.itemList)
		
		if range > 0:
			for item in self.itemList:
				item.OnClear()
				item.Hide()
				del item
		
		self.itemList = []
		
	def RemoveItemBought(self, bOwner, bId):
		range = len(self.itemList)
		
		if range > 0:
			for i in xrange(range):
				owner = self.itemList[i].InfoData["owner"]
				id = self.itemList[i].InfoData["id"]
				if owner == bOwner and id == bId:
					self.itemList[i].IsSelected = False
					self.itemList[i].Hide()
					self.itemList[i].SetBlock()
					break
				
			self.ReloadSymmetryBackground()
			self.ResetScrollbar()
			self.AdjustScrollBar()
			self.AdjustItemPositions(True)
	
	def ReloadSymmetryBackground(self):
		range = len(self.itemList)
		
		if range > 0:
			CntIndex = 0
			for i in xrange(range):
				if self.itemList[i].bIsBlocked:
					continue

				colorField = "black"
				if CntIndex % 2 == 0:
					colorField = "white"
				
				self.itemList[i].background.LoadImage(PATH_ROOT + "field_%d_%s.dds" % (self.itemList[i].itemSize, colorField))
				
				self.itemList[i].OnMouseOverOut2()
				
				CntIndex += 1

	def GetItemPrice(self, owner, itemID):
		for itemH in self.itemList:
			ownerItem = itemH.InfoData["owner"]
			idItem = itemH.InfoData["id"]
			if ownerItem == owner and itemID == idItem:
				return itemH.InfoData["price"]
		
		return 0

	def BuySelectedItems(self):
		global SELECTED_ITEMS_BUY
		range = len(SELECTED_ITEMS_BUY)
		
		if range > 0:
			for id_key in SELECTED_ITEMS_BUY:
				owner = SELECTED_ITEMS_BUY[id_key]
				offlineshop.SendBuyItemFromSearch(owner, id_key, self.GetItemPrice(owner, id_key))

class ShopSearch(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.loaded = 0
		self.iCountEnd = 0
		self.currentPage = 1
		self.interface = None
		self.dlgBuyQuestion = None
		self.ListBox = None
		self.CategoryList = None
		self.waitTime = 0
		self.SearchFilterShopItemResult = []
		
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		if self.ListBox:
			self.ListBox.Destroy()
			self.ListBox.Clear()
			del self.ListBox
			
		if self.CategoryList:
			self.CategoryList.Clear()
			del self.CategoryList
	
	def Show(self):
		self.LoadWindow()
		self.SetCenterPosition()
		self.Clear()
		ui.ScriptWindow.Show(self)
		
		self.OnSearch()

	def Clear(self):
		self.sLastItemName = None
		self.sCategory = -1
		self.sSubCategory = -1
		self.iPage = 1
		self.iCountEnd = 0
		self.ItemList.Clear()
		self.bCantChangePage = False
		self.FloodPage = 0

	def LoadWindow(self):
		if self.loaded == 1:
			return

		self.loaded = 1		
		self.AddFlag("movable")
		
		self.Board = ui.MakeBoardWithTitleBar(self, "not_pick", "Ticaret Camý", ui.__mem_func__(self.CloseGame), 730, 537)

		self.BoardListBox = ui.MakeImageBox(self.Board, "cream/shopeditor/category_board.dds", 17, 35)
		self.BoardItemList = ui.MakeImageBox(self.Board, "cream/shopeditor/item_board.dds", 210, 35)

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
		self.btnBuySelectedItems = ui.MakeButton(self, 226, 503, False, PATH_ROOT, "btn_filter_norm.dds", "btn_filter_hover.dds", "btn_filter_down.dds")
		self.btnBuySelectedItems.SetText("Seçilen itemleri satýn al")

		self.LineSearch = ui.MakeImageBox(self.Board, "cream/shopeditor/field_time.dds", 27, 45)

		self.sItemName = ui.EditLine()
		self.sItemName.SetParent(self.LineSearch)
		self.sItemName.SetMax(45)
		self.sItemName.SetSize(111 - self.LineSearch.GetWidth() - 2, 15)
		self.sItemName.SetPosition(2, 4)
		#self.sItemName.SetOverlayText("Search name...")
		self.sItemName.SetLimitWidth(self.LineSearch.GetWidth())
		self.sItemName.SetEscapeEvent(ui.__mem_func__(self.OnPressNameEscapeKey))
		self.sItemName.SetUpdateEvent(ui.__mem_func__(self.Search_RefreshTextHint))
		self.sItemName.SetTabEvent(ui.__mem_func__(self.Search_CompleteTextSearch))
		self.sItemName.SetReturnEvent(ui.__mem_func__(self.OnSearch))
		self.sItemName.SetOutline()
		self.sItemName.Show()

		self.searchEditHint = ui.TextLine()
		self.searchEditHint.SetParent(self.sItemName)
		self.searchEditHint.SetPackedFontColor(grp.GenerateColor(1.0, 1.0, 1.0, 0.5))
		self.searchEditHint.Show()

		self.btnSearch = ui.MakeButton(self.Board, 135, 45, False, PATH_ROOT, "btn_search_norm.dds", "btn_search_hover.dds", "btn_search_down.dds")
		self.btnSearch.SetEvent(ui.__mem_func__(self.OnSearch))

		self.btnEmptySearch = ui.MakeButton(self.Board, 165, 45, False, PATH_ROOT, "btn_reset_search_norm.dds", "btn_reset_search_hover.dds", "btn_reset_search_down.dds")
		self.btnBuySelectedItems.SetEvent(ui.__mem_func__(self.AskBuySelectedItems))

		self.ItemList = ListBoxItem()
		self.ItemList.SetParent(self.BoardItemList)
		self.ItemList.SetSize(502, 460)
		self.ItemList.SetPosition(2, 2)
		self.ItemList.SetEventBuy(ui.__mem_func__(self.AskBuySelectedItem))
		self.ItemList.SetEventWhisper(ui.__mem_func__(self.OnWhisper))
		self.ItemList.Show()
	
		self.ScrollBar = ui.ScrollBarNew()
		self.ScrollBar.SetParent(self)
		self.ScrollBar.SetScrollBarSize(464)
		self.ScrollBar.SetPosition(708, 35)
		self.ItemList.SetScrollBar(self.ScrollBar)
		self.ScrollBar.Show()
		
		self.MakeCategory()

		self.nextButton = ui.MakeButton(self, 50 + 453 + 130, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds")
		self.nextButton.SetText(">")
		
		self.lastButton = ui.MakeButton(self, 50 + 483 + 130, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds")
		self.lastButton.SetText(">>")
		
		self.prevButton = ui.MakeButton(self, 50 + 260-20 + 130, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds")
		self.prevButton.SetText("<")
		
		self.firstButton = ui.MakeButton(self, 50 + 230-20 + 130, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds")
		self.firstButton.SetText("<<")

		self.pageButtons = []
		self.pageButtons.append(ui.MakeButton(self, 50 + 275-10 + 130 + 5, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds"))
		self.pageButtons.append(ui.MakeButton(self, 50 + 310-10 + 130 + 5, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds"))
		self.pageButtons.append(ui.MakeButton(self, 50 + 345-10 + 130 + 5, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds"))
		self.pageButtons.append(ui.MakeButton(self, 50 + 380-10 + 130 + 5, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds"))
		self.pageButtons.append(ui.MakeButton(self, 50 + 415-10 + 130 + 5, 293 + 210, False, PATH_ROOT, "btn_page_norm.dds", "btn_page_hover.dds", "btn_page_down.dds"))

		for index, item in enumerate(self.pageButtons):
			item.SetText(str(index + 1))

		self.pageButtons[0].Show()
		self.pageButtons[1].Hide()
		self.pageButtons[2].Hide()
		self.pageButtons[3].Hide()
		self.pageButtons[4].Hide()
		self.pageButtons[0].Down()
		self.pageButtons[0].Disable()

		self.nextButton.SetEvent(ui.__mem_func__(self.NextPage))
		self.prevButton.SetEvent(ui.__mem_func__(self.PrevPage))
		self.firstButton.SetEvent(ui.__mem_func__(self.FirstPage))
		self.lastButton.SetEvent(ui.__mem_func__(self.LastPage))

		self.textInfoCheckBox = ui.TextLine()
		self.textInfoCheckBox.SetParent(self)
		self.textInfoCheckBox.SetPosition(38 + 21, 77 + 1)
		self.textInfoCheckBox.SetText("Oyuncu ismiyle ara")
		self.textInfoCheckBox.Show()

		self.CheckBox = ui.ExpandedImageBox()
		self.CheckBox.SetParent(self)
		self.CheckBox.SetPosition(38, 77)
		self.CheckBox.LoadImage(PATH_ROOT + "box_uncheck.dds")
		self.CheckBox.IsChecked = False
		self.CheckBox.OnMouseLeftButtonDown = ui.__mem_func__(self.OnCheckBox)
		self.CheckBox.Show()

		self.wndFilterWarrior = self.CreateFilterRadioButton("", 22 + 33 - 16, 94 + 5, "warrior_no_select.dds", "warrior_select.dds", "warrior_select.dds")
		self.wndFilterAssassin = self.CreateFilterRadioButton("", 22 + 68 - 16, 94 + 5, "assassin_no_select.dds", "assassin_select.dds", "assassin_select.dds")
		self.wndFilterSura = self.CreateFilterRadioButton("", 22 + 68 + 35 - 16, 94 + 5, "sura_no_select.dds", "sura_select.dds", "sura_select.dds")
		self.wndFilterShaman = self.CreateFilterRadioButton("", 22 + 68 + 35 + 35 - 16, 94 + 5, "shaman_no_select.dds", "shaman_select.dds", "shaman_select.dds")
	
	def OnCheckBox(self):
		if self.CheckBox.IsChecked:
			self.CheckBox.IsChecked = False
			self.CheckBox.LoadImage(PATH_ROOT + "box_uncheck.dds")
		else:
			self.CheckBox.IsChecked = True
			self.CheckBox.LoadImage(PATH_ROOT + "box_checked.dds")
			
		self.Search_RefreshTextHint()
	
	def CreateFilterRadioButton(self, text, x, y, up, over, down):
		button = ui.ToggleButton()
		button.SetParent(self)
		button.SetPosition(x, y)
		button.SetUpVisual(PATH + "filter/" + up)
		button.SetOverVisual(PATH + "filter/" + over)
		button.SetDownVisual(PATH + "filter/" + down)
		button.SetToolTipText(text)
		button.SetToggleUpEvent(ui.__mem_func__(self.OnFilterButtonDown), button)
		button.SetToggleDownEvent(ui.__mem_func__(self.OnFilterButtonSetUp), button)
		button.Show()
		
		button.Down()
		
		return button
	
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def BindInterface(self, interface):
		self.interface = interface
	def OnFilterButtonDown(self, wnd):
		wnd.SetUp()
		
	def OnFilterButtonSetUp(self, wnd):
		wnd.Down()

	def OnPressNameEscapeKey(self):
		if not self.sItemName:
			return
		
		if not self.sItemName.IsShowCursor() or self.sItemName.GetText() == "":
			self.OnPressEscapeKey()
		else:
			self.sItemName.SetText("")
			self.searchEditHint.SetText("")	

	def Search_CompleteTextSearch(self):
		if self.searchEditHint.GetText():
			oldText = self.sItemName.GetText()
			self.sItemName.SetText(oldText + self.searchEditHint.GetText()[len(oldText)+1:])
			self.sItemName.SetEndPosition()
			self.Search_RefreshTextHint()

	def Search_RefreshTextHint(self):
		EDIT_TEXT_BASE_COLOR = grp.GenerateColor(0.8549, 0.8549, 0.8549, 1.0)
		EDIT_TEXT_NOT_FOUND_COLOR = grp.GenerateColor(1.0, 0.2, 0.2, 1.0)
		
		self.searchEditHint.SetText("")
		self.sItemName.SetPackedFontColor(EDIT_TEXT_BASE_COLOR)
		
		search_text = self.sItemName.GetText()
		
		if len(search_text) and self.CheckBox.IsChecked == False:
			(hintName, vnum) = item.GetItemDataByNamePart(search_text)
			
			if vnum == -1:
				self.searchEditHint.SetText("")
				self.sItemName.SetPackedFontColor(EDIT_TEXT_NOT_FOUND_COLOR)
			else:
				self.searchEditHint.SetText(search_text + " " + hintName[len(search_text):])

	def OnRunMouseWheel(self, nLen):
		scroll = self.ScrollBar
		if self.BoardListBox.IsInPosition():
			scroll = self.ScrollBarCategory
		
		if nLen > 0:
			scroll.OnUp()
		else:
			scroll.OnDown()
			
		return True

	def MakeCategory(self):
		self.ScrollBarCategory = ui.ScrollBarNew()
		self.ScrollBarCategory.SetParent(self)
		self.ScrollBarCategory.SetScrollBarSize(380)
		self.ScrollBarCategory.SetPosition(193, 136)
		self.ScrollBarCategory.Show()

		self.CategoryList = ListBoxCategory()
		self.CategoryList.SetParent(self.BoardListBox)
		self.CategoryList.SetSize(self.BoardListBox.GetWidth(), self.BoardListBox.GetHeight() - 110)
		self.CategoryList.SetPosition(6, 100)
		self.CategoryList.SetScrollBar(self.ScrollBarCategory)
		self.CategoryList.SetEventDown(ui.__mem_func__(self.OnSearchByValue))
		self.CategoryList.Show()
		
		self.CategoryList.AppendItem("All", "0.dds", 0)
		
		SetCategories(self.CategoryList)

	def OnWhisper(self, name):
		if self.interface:
			self.interface.OpenWhisperDialog(name)

	def SetInterface(self, interface):
		self.interface = interface

	def SearchFilter_BuyFromSearch(self, ownerid, itemid):
		self.ItemList.RemoveItemBought(ownerid, itemid)
	
		for item in self.SearchFilterShopItemResult:
			if item['id'] == itemid and item['owner'] == ownerid:
				self.SearchFilterShopItemResult.remove(item)
				break
				
		global SELECTED_ITEMS_BUY
		SELECTED_ITEMS_BUY = {}

	def AskBuySelectedItems(self):
		global SELECTED_ITEMS_BUY
		count = len(SELECTED_ITEMS_BUY)
	
		self.BuyQuestionCancel()

		dlgBuyQuestion = uiCommon.QuestionDialog()
		dlgBuyQuestion.SetText("Do you want to buy x%d select items?" % (count))
		dlgBuyQuestion.SetAcceptEvent(ui.__mem_func__(self.BuySelectedItems))
		dlgBuyQuestion.SetCancelEvent(ui.__mem_func__(self.BuyQuestionCancel))
		dlgBuyQuestion.Open()
		self.dlgBuyQuestion = dlgBuyQuestion

	def BuySelectedItems(self):
		self.ItemList.BuySelectedItems()

		if self.dlgBuyQuestion:
			self.dlgBuyQuestion.Close()
			self.dlgBuyQuestion = None

	def AskBuySelectedItem(self, Pid, SlotPos, ItemName, ItemPrice):
		self.BuyQuestionCancel()

		self.sellOwner = Pid
		self.sellitemID = SlotPos
		self.sellItemPrice = ItemPrice
		
		dlgBuyQuestion = uiCommon.QuestionDialog()
		dlgBuyQuestion.SetText("Do you want to buy %s?" % (ItemName))
		dlgBuyQuestion.SetAcceptEvent(ui.__mem_func__(self.BuySelectedItem))
		dlgBuyQuestion.SetCancelEvent(ui.__mem_func__(self.BuyQuestionCancel))
		dlgBuyQuestion.Open()
		self.dlgBuyQuestion = dlgBuyQuestion
	
	def BuyQuestionCancel(self):
		if self.dlgBuyQuestion:
			self.dlgBuyQuestion.Close()
			self.dlgBuyQuestion = None		
	
	def BuySelectedItem(self):
		offlineshop.SendBuyItemFromSearch(self.sellOwner, self.sellitemID, self.sellItemPrice)
		
		if self.dlgBuyQuestion:
			self.dlgBuyQuestion.Close()
			self.dlgBuyQuestion = None

	def GetSearchFilterSettings(self, type = 0, subtype = 255):
		name = self.sItemName.GetText() if self.sItemName.GetText() else ""
		
		raceFlagDct = {
			0	: item.ITEM_ANTIFLAG_WARRIOR,
			1	: item.ITEM_ANTIFLAG_ASSASSIN,
			2	: item.ITEM_ANTIFLAG_SURA,
			3 	: item.ITEM_ANTIFLAG_SHAMAN,
		}
		
		raceflagbtn = [
			self.wndFilterWarrior,
			self.wndFilterAssassin,
			self.wndFilterSura,
			self.wndFilterShaman,
		]
		
		raceflag	= 0
		
		for k,v in raceFlagDct.items():
			if not raceflagbtn[k].IsDown():
				raceflag |= v
	
		type		= type
		subtype		= subtype
		bIsPlayerName = self.CheckBox.IsChecked
		
		levelmin	= 0
		levelmax	= 0
		
		yangmin		= 0
		yangmax		= 0
		
		if type == -1:
			type = 0
			subtype = 255
		
		if subtype == -1:	
			subtype = 255
		
		attributes	= tuple([(0,0) for x in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)])

		return (type, subtype, name, (yangmin,yangmax), (levelmin, levelmax, bIsPlayerName), raceflag, attributes)

	def OnSearchByValue(self, Type, SubType):
		if self.waitTime > app.GetGlobalTimeStamp(): # FIXME 01
			chat.AppendChat(1, "%d saniye beklemelisin" % (TIME_WAIT))
			return

		self.waitTime = app.GetGlobalTimeStamp() + TIME_WAIT
		self.sCategory = Type
		self.sSubCategory = SubType
		self.ItemList.Clear()

		self.SearchFilterLastUsedSetting = self.GetSearchFilterSettings(Type, SubType)
		
		offlineshop.SendFilterRequest(*self.SearchFilterLastUsedSetting)

		self.currentPaginationPage = 1

		global SELECTED_ITEMS_BUY
		SELECTED_ITEMS_BUY = {}

	def OnSearch(self):
		if self.waitTime > app.GetGlobalTimeStamp(): # FIXME 01
			chat.AppendChat(1, "%d saniye beklemelisin" % (TIME_WAIT))
			return
			
		self.waitTime = app.GetGlobalTimeStamp() + TIME_WAIT
		self.ItemList.Clear()

		self.SearchFilterLastUsedSetting = self.GetSearchFilterSettings(self.sCategory, self.sSubCategory)
		offlineshop.SendFilterRequest(*self.SearchFilterLastUsedSetting)

		self.currentPaginationPage = 1

		global SELECTED_ITEMS_BUY
		SELECTED_ITEMS_BUY = {}

	def RefreshPaginationButtons(self):
		self.currentPaginationPage = int(math.ceil(float(self.currentPage) / 5.0 ))
		self.shownPages = min(self.pageCount - (5 * (self.currentPaginationPage - 1)), 5)

		for x in xrange(5):
			currentPage = (x + ((self.currentPaginationPage-1) * 5) + 1)
			self.pageButtons[x].SetUp()
			self.pageButtons[x].SetText("%d" % currentPage)
			self.pageButtons[x].SetEvent(ui.__mem_func__(self.GotoPage), currentPage)
		
		map(ui.Button.Hide, self.pageButtons)
		map(ui.Button.Enable, self.pageButtons)
		
		for x in xrange(self.shownPages):
			self.pageButtons[x].Show()

		self.pageButtons[(self.currentPage - ((self.currentPaginationPage - 1) * 5)) - 1].Down()
		self.pageButtons[(self.currentPage - ((self.currentPaginationPage - 1) * 5)) - 1].Disable()

	def GotoPage(self, page):
		self.currentPage = page
		self.RefreshList()

	def FirstPage(self):
		self.currentPage = 1
		self.RefreshList()
		
	def LastPage(self):
		self.currentPage = self.pageCount
		self.RefreshList()

	def NextPage(self):
		if self.currentPage < self.pageCount:
			self.currentPage += 1

		self.RefreshList()
			
	def PrevPage(self):
		if self.currentPage > 1:
			self.currentPage -= 1
		
		self.RefreshList()
	
	def ShopFilterResult( self , size):
		self.SearchFilterShopItemResult = []
	
	def ShopFilterResultItem_Alloc(self):
		self.SearchFilterShopItemResult.append({})

	def ShopFilterResultItem_SetValue( self,  key, index, *args):
		if key in ( "id", "vnum", "count", "price", "owner", "owner_name", 'trans', 'evolution'):
			self.SearchFilterShopItemResult[index][key] = args[0]
		
		elif key == "attr":
			if not key in self.SearchFilterShopItemResult[index]:
				self.SearchFilterShopItemResult[index][key] = {}
			
			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]
			
			self.SearchFilterShopItemResult[index][key][attr_index] = {}
			self.SearchFilterShopItemResult[index][key][attr_index]["type"]  = attr_type
			self.SearchFilterShopItemResult[index][key][attr_index]["value"] = attr_value
		
		elif key == "socket":
			if not key in self.SearchFilterShopItemResult[index]:
				self.SearchFilterShopItemResult[index][key] = {}
			
			socket_index = args[0]
			socket_val	 = args[1]
			
			self.SearchFilterShopItemResult[index][key][socket_index] = socket_val

	def ShopFilterResult_Show(self):
		self.itemCount = len(self.SearchFilterShopItemResult)

		self.pageCount = int(math.ceil(float(self.itemCount) / float(MAX_ITEMS_APPEND)))
		self.currentPaginationPage = 1
		self.paginationPageCount = int(math.ceil(float(self.pageCount) / 5.0 ))

		self.RefreshPaginationButtons()

		self.currentPage = 1
		self.RefreshList()

	def RefreshList(self):
		self.ItemList.Clear()
		self.RefreshPaginationButtons()
		
		size = len(self.SearchFilterShopItemResult)
		start = (self.currentPage - 1) * MAX_ITEMS_APPEND
		end = ((self.currentPage - 1) * MAX_ITEMS_APPEND) + MAX_ITEMS_APPEND
		for x in xrange(size):
			if start + x >= end:
				break

			if start + x < len(self.SearchFilterShopItemResult):
				self.ItemList.AppendItem(start + x, self.SearchFilterShopItemResult[start + x])
	
	def Close(self, IsFromGame = False):
		self.ItemList.Clear()
		
		if self.dlgBuyQuestion:
			self.dlgBuyQuestion.Close()
			self.dlgBuyQuestion = None
		
		self.Hide()
	
	def CloseGame(self):
		self.Close(True)
	
	def OnPressEscapeKey(self):
		self.Close(True)
		return True	
