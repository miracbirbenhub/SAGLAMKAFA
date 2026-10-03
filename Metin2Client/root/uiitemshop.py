import ui
import uiToolTip
import uiCommon
import localeInfo
import wndMgr
import constInfo
import dbg
import os
import snd
import chat
import chr
import player
import item
import net
import app
import background
import chrmgr
import renderTarget


FAKE_CATEGORY_DATA = {
	0 : {
		"categoryName" : "Fýrsat",
		"subCategoryNameList" : ["Özel Eþyalar"],
	},
	1 : {
		"categoryName" : "Binek",
		"subCategoryNameList" : ["Mühür", "Parþomen", "Nesne"],
	},
	2 : {
		"categoryName" : "Boost",
		"subCategoryNameList" : ["Özel", "Yüzükler", "Rüya Ruhu"],
	},
	3 : {
		"categoryName" : "Ekipman",
		"subCategoryNameList" : ["Silah", "Zýrh", "Kask", "Kalkan", "Küpe", "Bilezik", "Kolye", "Ayakkabý", "Kemer", "Omuz Kuþaðý"],
	},
	4 : {
		"categoryName" : "Kostüm",
		"subCategoryNameList" : ["Erkek", "Bayan"],
	},
}


ITEM_FLAG_STACKABLE = (1 << 2)
BLEND_AFFECT_UNLIMITED_DURATION = 100 * 60 * 60
def toLower(string):
	alphabetList = {
		'Ý' : 'i',
		'I' : 'ý',
		'Ö' : 'ö',
		'Ü' : 'ü',
		'Þ' : 'þ',
		'Ç' : 'ç',
		'Ð' : 'ð',
	}

	for (key, item) in alphabetList.iteritems():
		string = string.replace(key, item)

	return string.lower()

###################################################################################################
# Load Shop Item Table


# def LoadItemShopTable():

	# try:
		# lines = pack_open("item_shop_table.txt", "28102461", "55221166", "99887733", "11223355","r").readlines()
	# except IOError:
		# dbg.LogBox("LoadLocaleError(%(srcFileName)s)" % locals())
		# app.Abort()


	# for line in lines:
		# tokens = line[:-1].split("\t")

		# if len(tokens) < 8:
			# continue

		# if tokens[0][0] == "#":
			# continue

		# categoryID = int(tokens[0])
		# subCategoryID = int(tokens[1])
		# itemID = int(tokens[2])
		# itemVnum = int(tokens[3])
		# itemPrice = int(tokens[4])
		# itemPriceOld = int(tokens[5])
		# itemCount = int(tokens[6])
		# itemSocketZero = int(tokens[7])
		
		# if not constInfo.ITEM_DATA.has_key(categoryID):
			# constInfo.ITEM_DATA[categoryID] = {}

		# if not constInfo.ITEM_DATA[categoryID].has_key(subCategoryID):
			# constInfo.ITEM_DATA[categoryID][subCategoryID] = []

		# item.SelectItem(itemVnum)
		# constInfo.ITEM_DATA[categoryID][subCategoryID].append((None, itemID, itemVnum,itemPriceOld, itemPrice, itemCount, itemSocketZero))
		# constInfo.ITEM_SEARCH_DATA.append((toLower(item.GetItemName()), itemID, itemVnum,itemPriceOld, itemPrice, itemCount, itemSocketZero))


# LoadItemShopTable()
# Load Shop Item Table
###################################################################################################

###################################################################################################
# Category Board
class CategoryButton(ui.Window):
	ARROWIMAGE_FILE_NAME = {
		"SELECT" : "d:/ymir work/ui/privatesearch/private_next_btn_02.sub",
		"UNSELECT" : "d:/ymir work/ui/privatesearch/private_next_btn_01.sub",
	}

	def __init__(self, parent, x, y, isSubItem = False):
		ui.Window.__init__(self)
		self.getParent = parent
		self.key = None
		self.isSubItem = isSubItem

		self.SetParent(parent)
		self.AddFlag("float")
		self.SetSize(96, 26)
		self.SetPosition(x, y)
		
		categoryButton = ui.RadioButton()
		categoryButton.SetParent(self)
		categoryButton.AddFlag("not_pick")
		
		
		
		if (isSubItem):
			categoryButton.SetUpVisual("d:/ymir work/ui/itemshop/subbutton.png")
			categoryButton.SetOverVisual("d:/ymir work/ui/itemshop/subbutton.png")
			categoryButton.SetDownVisual("d:/ymir work/ui/itemshop/subbuttonbasili.png")
		else:
			categoryButton.SetUpVisual("d:/ymir work/ui/itemshop/norm.png")
			categoryButton.SetOverVisual("d:/ymir work/ui/itemshop/norm1.png")
			categoryButton.SetDownVisual("d:/ymir work/ui/itemshop/norm1.png")

		categoryButton.SetPosition(0, 0)
		categoryButton.SetEvent(ui.__mem_func__(self.OnMouseLeftButtonDown))
		categoryButton.Show()
		self.categoryButton = categoryButton

		image = ui.ImageBox()
		image.SetParent(self)
		image.AddFlag("not_pick")
		image.LoadImage(self.ARROWIMAGE_FILE_NAME["UNSELECT"])
		image.SetPosition(6, 5)
		image.Hide()
		self.image = image

		name = ui.TextLine()
		name.SetParent(self)
		name.SetPosition(25, 5)
		name.Show()
		self.name = name

	def IsSubItem(self):
		return self.isSubItem
		
	def SetName(self, name):
		if self.isSubItem:
			self.name.SetPosition(22, 5)
			#self.name.SetFontColor(0.63,0.91,1.00)
		else:
			self.name.SetPosition(22, 5)
			#self.name.SetFontColor(1.00,0.69,0.29)

		self.name.SetText(name)

	def SetKey(self, key):
		self.key = key
		
	def GetKey(self):
		return self.key

	def IsSameKey(self, key):
		return self.key == key

	def Select(self):
		self.categoryButton.Down()
		self.image.LoadImage(self.ARROWIMAGE_FILE_NAME["SELECT"])

	def UnSelect(self):
		self.categoryButton.SetUp()
		self.image.LoadImage(self.ARROWIMAGE_FILE_NAME["UNSELECT"])

	def OnMouseLeftButtonDown(self):
		if not self.isSubItem:
			self.getParent.OnSelectItem(self)
		else:
			self.getParent.OnSubSelectItem(self)

class CategoryListItem(CategoryButton):
	IMAGE_FILE_NAME = {
		"OPEN" : "d:/ymir work/ui/privatesearch/btn_plus_dis.tga",
		"CLOSE" : "d:/ymir work/ui/privatesearch/btn_minus_dis.tga",
	}

	def __init__(self, parent, x, y):
		self.getParent = parent
		self.isOpen = False
		self.subCategoryList = []

		CategoryButton.__init__(self, parent, x, y)

	def AppendSubCategory(self, key, name):
		(x, y) = self.GetLocalPosition()
		yPos = len(self.subCategoryList) * 30 + y + 30
		categoryButton = CategoryButton(self.getParent, 30, yPos, True)
		categoryButton.SetKey(key)
		categoryButton.SetName(name)
		self.subCategoryList.append(categoryButton)
		return categoryButton

	def GetCategoryList(self):
		return self.subCategoryList

	def FindCategory(self, key):
		list = filter(lambda argCategory, argKey=key: argCategory.IsSameKey(argKey), self.subCategoryList)
		if list:
			return list[0]

		return None

	def IsOpen(self):
		return self.isOpen

	def Open(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["OPEN"])
		self.categoryButton.Down()
		self.categoryButton.Disable()
		self.isOpen = True

	def Close(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["CLOSE"])
		self.image.SetPosition(6, 5)
		self.categoryButton.SetUp()
		self.categoryButton.Enable()
		self.isOpen = False
		
		map(ui.Window.Hide, self.subCategoryList)

	def Select(self):
		self.Open()
		self.getParent.OnRefreshList()

	def UnSelect(self):
		self.Close()
		self.getParent.OnRefreshList()

class CategoryBoard(ui.Window):
	def __init__(self, parentFirst, parentSecond, scrollBar):
		ui.Window.__init__(self)
		
		self.SetParent(parentSecond)
		self.getParent = parentFirst

		self.scrollBar = scrollBar
		self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.selectCategory = None
		self.selectSubCategory = None
		self.categoryListItems = []
		self.showingItemList = []
		self.startLine = 0

	def OnScroll(self):
		scrollLineCount = len(self.showingItemList) - 13
		startLine = int(scrollLineCount * self.scrollBar.GetPos())

		if startLine != self.startLine:
			self.startLine = startLine
			self.__LocateMember()

	def OnSelectItem(self, item):
		if self.selectCategory:
			self.selectCategory.UnSelect()
			self.getParent.ClearItemBoard()

			if item == self.selectCategory:
				item = None

		self.selectCategory = item

		if self.selectCategory:
			self.selectCategory.Select()
			
			self.OnSubSelectItem(self.selectCategory.GetCategoryList()[0])

		self.scrollBar.SetPos(0.0)

		buttonList = filter(lambda argSelf: argSelf.IsOpen(), self.categoryListItems)
		if buttonList:
			(x, y) = buttonList[0].GetLocalPosition()

			if y >= 385:
				y += 24

			startPos = 1.0 / (385.0 / float(y - 24))
			self.scrollBar.SetPos(startPos)
	
	def OnSubSelectItem(self, item):
		if self.selectSubCategory:
			if item != self.selectSubCategory:
				self.selectSubCategory.UnSelect()
				
		self.selectSubCategory = item
		
		if self.selectSubCategory:
			self.selectSubCategory.Select()

			self.getParent.ChangeCategory(self.selectCategory.GetKey(), self.selectSubCategory.GetKey())

	def __LocateMember(self):

		if self.showingItemList:
			stepSize = 1.0 / (len(self.showingItemList) - 12)
			self.scrollBar.SetScrollStep(stepSize)

			if stepSize <= 0.8:
				stepSize += 0.2

			self.scrollBar.SetMiddleBarSize(stepSize)

		self.scrollBar.Show()

		#####

		yPos = 25
		heightLimit = self.GetHeight() - 30

		map(ui.Window.Hide, self.showingItemList)

		for item in self.showingItemList[self.startLine:]:
			xPos = 10
			if item.IsSubItem():
				xPos = 30
			item.SetPosition(xPos, yPos)
			item.SetTop()
			item.Show()

			yPos += 30
			if yPos > heightLimit:
				break
				
		
	
	def OnRefreshList(self):
		self.showingItemList = []
		
		for items in self.categoryListItems:
			self.showingItemList.append(items)
			subItems = items.GetCategoryList()

			if items.IsOpen() and subItems:
				for item in subItems:
					self.showingItemList.append(item)

		self.__LocateMember()
	
	def firstOpenBoard(self):
		self.OnSelectItem(self.categoryListItems[0])
		self.OnSubSelectItem(self.categoryListItems[0].GetCategoryList()[0])

	def RefreshProcess(self):
		self.categoryListItems = []
		for i in xrange(len(FAKE_CATEGORY_DATA)):
			categoryData = FAKE_CATEGORY_DATA[i]
			category = CategoryListItem(self, 10, 25 + i * 30)
			category.SetKey(i)
			category.SetName(categoryData["categoryName"])
			category.Close()
			category.Show()

			for j in xrange(len(categoryData["subCategoryNameList"])):
				category.AppendSubCategory(j, categoryData["subCategoryNameList"][j])

			self.categoryListItems.append(category)
		
		self.OnRefreshList()


	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()
			
			
# Category Board
###################################################################################################

###################################################################################################
# Item Stackable Buy Dialog
class ItemStackableBuyDialog(ui.BoardWithTitleBar):

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		
		self.getParent = None
		self.itemID = 0
		self.itemVnum = 0
		self.itemPrice = -1
		self.maxCount = 0
		self.coins = 0
		self.mark = 0
		
		self.__LoadDialog()
	
	def __LoadDialog(self):
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetSize(200, 160)
		self.SetCloseEvent(self.Close)

		countTextFirst = ui.TextLine()
		countTextFirst.SetParent(self)
		countTextFirst.SetFontName("Tahoma:14")
		countTextFirst.SetText("Alýnacak toplam miktar: 1")
		countTextFirst.SetPosition(self.GetWidth() / 2, 40)
		countTextFirst.SetHorizontalAlignCenter()
		countTextFirst.Show()
		self.countTextFirst = countTextFirst
		
		countArrowUp = ui.Button()
		countArrowUp.SetParent(self)
		countArrowUp.SetPosition(self.GetWidth() / 2 - 44, self.GetHeight() / 2 - 9)
		countArrowUp.SetUpVisual("d:/ymir work/ui/itemshop/arrow_up_default.sub")
		countArrowUp.SetOverVisual("d:/ymir work/ui/itemshop/arrow_up_over.sub")
		countArrowUp.SetDownVisual("d:/ymir work/ui/itemshop/arrow_up_down.sub")
		countArrowUp.SetEvent(self.__ArrowButton, 0)
		countArrowUp.Show()
		self.countArrowUp = countArrowUp

		countArrowDown = ui.Button()
		countArrowDown.SetParent(self)
		countArrowDown.SetPosition(self.GetWidth() / 2 - 44, self.GetHeight() / 2 + 3)
		countArrowDown.SetUpVisual("d:/ymir work/ui/itemshop/arrow_down_default.sub")
		countArrowDown.SetOverVisual("d:/ymir work/ui/itemshop/arrow_down_over.sub")
		countArrowDown.SetDownVisual("d:/ymir work/ui/itemshop/arrow_down_down.sub")
		countArrowDown.SetEvent(self.__ArrowButton, 1)
		countArrowDown.Show()
		self.countArrowDown = countArrowDown

		countSlotBar = ui.SlotBar()
		countSlotBar.SetParent(self)
		countSlotBar.SetSize(50, 18)
		countSlotBar.SetPosition(self.GetWidth() / 2 - 30, self.GetHeight() / 2 - 10)
		countSlotBar.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickValueEditLine)
		countSlotBar.Show()
		self.countSlotBar = countSlotBar

		countEditline = ui.EditLine()
		countEditline.SetParent(countSlotBar)
		countEditline.SetSize(24, 18)
		countEditline.SetMax(3)
		countEditline.SetPosition(3, 2)
		countEditline.SetNumberMode()
		countEditline.SetText("1")
		countEditline.SetFocus()
		countEditline.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		countEditline.OnIMEReturn = ui.__mem_func__(self.__OnValueReturn)
		countEditline.Show()
		self.countEditline = countEditline
		
		countTextSecond = ui.TextLine()
		countTextSecond.SetParent(countSlotBar)
		countTextSecond.SetFontName("Tahoma:14")
		countTextSecond.SetText("/0")
		countTextSecond.SetPosition(55, 0)
		countTextSecond.Show()
		self.countTextSecond = countTextSecond
		
		ammoutText = ui.TextLine()
		ammoutText.SetParent(self)
		ammoutText.SetFontName("Tahoma:14")
		ammoutText.SetText("Tutar : 0 Ep")
		ammoutText.SetPosition(self.GetWidth() / 2, self.GetHeight() / 2 + 15)
		ammoutText.SetHorizontalAlignCenter()
		ammoutText.Show()
		self.ammoutText = ammoutText
		
		acceptButton = ui.Button()
		acceptButton.SetParent(self)
		acceptButton.SetPosition(self.GetWidth() / 2 - 70, self.GetHeight() - 35)
		acceptButton.SetUpVisual("d:/ymir work/ui/Public/acceptbutton00.sub")
		acceptButton.SetOverVisual("d:/ymir work/ui/Public/acceptbutton01.sub")
		acceptButton.SetDownVisual("d:/ymir work/ui/Public/acceptbutton02.sub")
		acceptButton.SetToolTipText("Satýn Al")
		acceptButton.SetEvent(ui.__mem_func__(self.acceptButtonEvent))
		acceptButton.Show()
		self.acceptButton = acceptButton
		
		cancelButton = ui.Button()
		cancelButton.SetParent(self)
		cancelButton.SetPosition(self.GetWidth() / 2 + 8, self.GetHeight() - 35)
		cancelButton.SetUpVisual("d:/ymir work/ui/Public/canclebutton00.sub")
		cancelButton.SetOverVisual("d:/ymir work/ui/Public/canclebutton01.sub")
		cancelButton.SetDownVisual("d:/ymir work/ui/Public/canclebutton02.sub")
		cancelButton.SetToolTipText("Ýptal")
		cancelButton.SetEvent(ui.__mem_func__(self.Close))
		cancelButton.Show()
		self.cancelButton = cancelButton
	
	def SetParent2(self, parent):
		self.getParent = parent
	
	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.BoardWithTitleBar.Show(self)

	def Close(self):
		self.itemPrice = -1
		self.maxCount = 0
		self.countEditline.SetText("1")
		self.countTextFirst.SetText("Alýnacak toplam miktar: 1")
		self.Hide()

	def acceptButtonEvent(self):
		itemName = self.titleName.GetText()
		itemCount = self.countEditline.GetText()
		price = self.itemPrice * int(itemCount)

		if self.getParent:
			self.getParent.buyQuestionDialog(self.itemID, self.itemVnum, itemName, int(itemCount), price)
		
		self.Close()

	def __ClickValueEditLine(self):
		self.countEditline.SetFocus()
	
	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.countEditline)

		text = self.countEditline.GetText()

		count = 1
		if text and text.isdigit():
			try:
				count = int(text)
				
				if count <= 0:
					count = 1

				if count > self.maxCount:
					count = self.maxCount
					self.countEditline.SetText("%d" % count)

			except ValueError:
				pass

		self.countTextFirst.SetText("Alýnacak toplam miktar: %d" % count)

		price = self.itemPrice * count
		self.SetItemPrice(price)

	def __OnValueReturn(self):
		self.countEditline.KillFocus()

		text = self.countEditline.GetText()

		count = 1
		if text and text.isdigit():
			try:
				count = int(text)

				if count <= 0:
					count = 1

			except ValueError:
				count = 1

		self.countEditline.SetText("%d" % count)
		self.countTextFirst.SetText("Alýnacak toplam miktar: %d" % count)
		price = self.itemPrice * count
		self.SetItemPrice(price)

	def __ArrowButton(self, type):
		self.countEditline.KillFocus()

		text = self.countEditline.GetText()

		count = 0

		if not text or not text.isdigit():
			count = 1
		else:
			count = int(text)

		if type == 0:
			count += 1
		else:
			count -= 1

		if count <= 0:
			count = 1
		elif count >= self.maxCount:
			count = self.maxCount

		self.countEditline.SetText("%d" % count)
		self.countTextFirst.SetText("Alýnacak toplam miktar: %d" % count)
		price = self.itemPrice * count
		self.SetItemPrice(price)

	def SetItemPrice(self, price):
		text = ("Tutar : %d EP" % (price))
		self.ammoutText.SetText(text)

	def SetCountText(self, price, playerTotalCoin):
		self.itemPrice = price
		self.maxCount = playerTotalCoin / price
		self.countTextSecond.SetText("/%d" % self.maxCount)

		if self.maxCount > 200:
			self.maxCount = 200

		self.SetItemPrice(price)

	def SetItem(self, itemID, itemVnum):
		self.itemID = itemID
		self.itemVnum = itemVnum

# Item Stackable Buy Dialog
###################################################################################################

###################################################################################################
# Item Shop Window
class ItemShopWindow(ui.ScriptWindow):
	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)
		
		self.searchEditline = None
		self.searchButton = None
		self.boardFirst = None
		self.scrollBar = None
		self.prevButton = None
		self.pageText = None
		self.nextButton = None

		self.categoryGroupBoard = None
		self.wndItemList = {}
		self.itemList = []
		
		self.itemStackalbeBuyDialog = None
		
		self.pageMaxNum = 0
		self.pageNum = 0
		
		self.itemToolTip = None
		self.questionDialog = None
		self.interface = interface

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

	def LoadWindow(self):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/item_shop.py")
		except:
			import exception
			exception.Abort("ItemShopWindow.LoadDialog.LoadObject")
		try:
			self.GetChild("TitleBar").SetCloseEvent(self.Close)

			self.searchEditline = self.GetChild("search_editline")
			self.searchButton = self.GetChild("search_button")

			self.boardFirst = self.GetChild("board_first")
			self.scrollBar = self.GetChild("ScrollBar")

			self.prevButton = self.GetChild("prev_button")
			self.pageText = self.GetChild("page_text")
			self.nextButton = self.GetChild("next_button")

			self.dragoncoin = self.GetChild("dragon_coin_text")
			self.dragonmark = self.GetChild("dragon_mark_text")
			self.coinBuyButton = self.GetChild("coin_buy_button")

			for i in xrange(1, 10):
				number = "0%d" % i # number = "0%d" % i if i < 10 else "%d" % i (python 2.7 version)

				if i >= 10:
					number = "%d" % i

				wndItemSlot = self.GetChild("itemSlot_%s" % number)
				wndItemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.selectItemSlotEvent))
				wndItemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.selectItemSlotEvent))
				wndItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				wndItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

				itemName = self.GetChild("itemName_%s" % number)
				itemName.SetMax(15)
				itemName.SetLimitWidth(95)
				itemName.SetMultiLine()
				itemName.SetFontName("Tahoma:13")
				itemName.SetPackedFontColor(0xFFFEE3AE)
				itemOldPrice = self.GetChild("itemOldPrice_%s" % number)
				itemOldPrice.SetMax(15)
				itemOldPrice.SetLimitWidth(95)
				itemOldPrice.SetMultiLine()
				itemOldPrice.SetFontColor(1, 0, 0)
				itemOldPrice.SetFontName("Tahoma:11")
				itemPreviewButton = self.GetChild("itemPreviewButton_%s" % number)
				itemPreviewButton.Hide()
				itemBuyButton = self.GetChild("itemBuyButton_%s" % number)
				itemBuyButton.ButtonText.SetFontName("Tahoma:13")
				itemBuyButton.Disable()
				#itemBuyButton.ButtonText.SetFontColor(1.00,0.69,0.29)
				
				self.wndItemList[i] = (wndItemSlot, itemName, itemOldPrice, itemPreviewButton, itemBuyButton)
		except:
			import exception
			exception.Abort("ItemShopWindow.LoadDialog.BindObject")
		
		self.searchEditline.OnIMEReturn = ui.__mem_func__(self.searchButtonEvent)
		self.searchButton.SetEvent(ui.__mem_func__(self.searchButtonEvent))
		self.prevButton.SetEvent(ui.__mem_func__(self.prevButtonEvent))
		self.nextButton.SetEvent(ui.__mem_func__(self.nextButtonEvent))
		self.coinBuyButton.SetEvent(ui.__mem_func__(self.coinButtonEvent))

		categoryGroupBoard = CategoryBoard(self, self.boardFirst, self.scrollBar)
		categoryGroupBoard.SetSize(self.boardFirst.GetWidth() - 25, self.boardFirst.GetHeight())
		categoryGroupBoard.Show()
		self.categoryGroupBoard = categoryGroupBoard

		itemStackalbeBuyDialog = ItemStackableBuyDialog()
		itemStackalbeBuyDialog.SetParent2(self)
		itemStackalbeBuyDialog.SetCenterPosition()
		itemStackalbeBuyDialog.Hide()
		self.itemStackalbeBuyDialog = itemStackalbeBuyDialog
		
		self.questionDialog = uiCommon.QuestionDialog2()
		self.questionDialog.SetAcceptEvent(lambda arg = True: self.QuestionDialogEvent(arg))
		self.questionDialog.SetCancelEvent(lambda arg = False: self.QuestionDialogEvent(arg))
		self.questionDialog.Hide()
		
		
		self.coinBuyButton.ButtonText.SetPackedFontColor(0xFFFEE3AE)
				
	def OnScrollWheel(self, nLen):
		if self.scrollBar:
			if int(nLen) < 0:
				self.scrollBar.OnDown()
			else:
				self.scrollBar.OnUp()
		
	def SetItemToolTip(self, itemToolTip):
		self.itemToolTip = itemToolTip
		
	def OnUpdate(self):
		self.dragoncoin.SetText("%d EP" % int(player.GetDragonCoin()))
		self.coins = int(player.GetDragonCoin())
		self.dragonmark.SetText("%d EM" % int(player.GetDragonMark()))
		self.mark = int(player.GetDragonMark())

	def Open(self):
		self.max_pos_x = wndMgr.GetScreenWidth() - self.GetWidth()
		self.max_pos_y = wndMgr.GetScreenHeight() - self.GetHeight()
		self.SetCenterPosition()
		self.categoryGroupBoard.RefreshProcess()
		self.categoryGroupBoard.firstOpenBoard()
		self.RenderTargetBaoard()
		ui.ScriptWindow.Show(self)
		self.SetTop()

	def Close(self):
		ui.ScriptWindow.Hide(self)
		#renderTarget.SetVisibility(6, False)
		if self.itemStackalbeBuyDialog:
			self.itemStackalbeBuyDialog.Close()
		
		if self.questionDialog:
			self.questionDialog.Close()
		
		return True
		
		
	def RenderTargetBaoard(self):
		renderTarget.SelectModel(6, player.GetRace())
		renderTarget.SetBackground(6, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub", player.GetRace(), 0)
		renderTarget.SetVisibility(6, True)
		
	def ClearItemBoard(self):
		for i in xrange(1, 10):
			(wndItemSlot, itemName, itemOldPrice, itemPreviewButton, itemBuyButton) = self.wndItemList[i]
			wndItemSlot.ClearSlot(i)
			wndItemSlot.RefreshSlot()

			itemName.SetText("")
			itemOldPrice.SetText("")
			itemPreviewButton.Hide()
			itemBuyButton.SetText("")
			itemBuyButton.Disable()

		self.prevButton.Hide()
		self.nextButton.Hide()
		self.pageText.SetText("0/0")

	def ChangeCategory(self, categoryID, subCategoryID):
		self.ClearItemBoard()

		if not constInfo.ITEM_DATA.has_key(categoryID):
			return

		category = constInfo.ITEM_DATA[categoryID]

		if not category.has_key(subCategoryID):
			return

		category = category[subCategoryID]
		self.itemList = [item for item in category]
		self.pageMaxNum = len(self.itemList) / 9
		
		if len(self.itemList) % 9 > 0:
			self.pageMaxNum += 1
		
		self.pageNum = 0

		self.RefreshProcess()
	
	def prevButtonEvent(self):
		if self.pageNum - 1 < 0:
			return

		self.pageNum -= 1
		self.RefreshProcess()

	def nextButtonEvent(self):
		if self.pageNum + 1 >= self.pageMaxNum:
			return

		self.pageNum += 1
		self.RefreshProcess()

	def coinButtonEvent(self):
		if self.interface:
			self.interface.OpenWebWindow("https://sancak2.com.tr/ishop/")

	def RefreshProcess(self):
		self.ClearItemBoard()

		self.pageText.SetText("%d/%d" % (self.pageNum + 1, self.pageMaxNum))
		if self.pageNum == 0:
			self.prevButton.Hide()
		else:
			self.prevButton.Show()
			
		if self.pageNum + 1 == self.pageMaxNum:
			self.nextButton.Hide()
		else:
			self.nextButton.Show()

		for i in xrange(1, 10):
			itemPos = (self.pageNum * 9) + (i - 1)
			
			if len(self.itemList) <= itemPos:
				return
			
			(empty, itemID, itemVnum, itemPrice,itemPriceOld, itemCount, itemSocketZero, itemMark) = self.itemList[itemPos]
			(wndItemSlot, itemName, itemOldPrice, itemPreviewButton, itemBuyButton) = self.wndItemList[i]

			wndItemSlot.SetItemSlot(i, itemVnum, itemCount)
			wndItemSlot.RefreshSlot()
			
			item.SelectItem(itemVnum)
			
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			itemValue = item.GetValue(0)
			itemHair = item.GetValue(3)
			(affectTypem, affectValuem) = item.GetAffect(0)
			race = player.GetRace()
			job = chr.RaceToJob(race)
			sex = chr.RaceToSex(race)
			MALE = 1
			FEMALE = 0
			
			
			ANTI_FLAG_DICT = {
				0 : item.ITEM_ANTIFLAG_WARRIOR,
				1 : item.ITEM_ANTIFLAG_ASSASSIN,
				2 : item.ITEM_ANTIFLAG_SURA,
				3 : item.ITEM_ANTIFLAG_SHAMAN,
			}
			
			isItemPreview = False
			if itemType == item.ITEM_TYPE_WEAPON:
				isItemPreview = True
			if itemType == item.ITEM_TYPE_ARMOR and itemSubType == item.ARMOR_BODY:
				isItemPreview = True
			if itemType == item.ITEM_TYPE_COSTUME:
				isItemPreview = True
			#elif item.GetItemTypeVID(itemVnum) == item.ITEM_TYPE_USE and item.GetItemSubTypeVID(itemVnum) == item.USE_COSTUME_MOUNT_SKIN:	
				#isItemPreview = True
				
			if not ANTI_FLAG_DICT.has_key(job):
				isItemPreview = False
			if item.IsAntiFlag(ANTI_FLAG_DICT[job]):
				isItemPreview = False
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
				isItemPreview = False
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
				isItemPreview = False
				
			if itemPrice >= itemMark:
				priceType = "%d Ep" % itemPrice
			else:
				priceType = "%d EM" % itemMark
				
			#if constInfo.PetMuhurKontrol(itemVnum):
			#	isItemPreview = True
			#if constInfo.BinekMuhurKontrol(itemVnum):
			#	isItemPreview = True
		#	if constInfo.IS_FAKEBUFF_ITEM(itemVnum):
		#		isItemPreview = True

			if isItemPreview:
				itemPreviewButton.Show()

			itemName.SetText(item.GetItemName())
			itemOldPrice.SetText("Eski Fiyat:%d.EP" % itemPriceOld)
			itemPreviewButton.SetEvent(ui.__mem_func__(self.previewButtonEvent), itemVnum, itemType, itemSubType, itemValue, affectValuem, itemHair)
			itemBuyButton.SetText(priceType)
			itemBuyButton.SetEvent(ui.__mem_func__(self.buyButtonEvent), itemID, itemVnum, itemPrice, itemCount, itemMark)
			itemBuyButton.Enable()

	def searchButtonEvent(self):
		searchText = self.searchEditline.GetText()
		if len(searchText) < 3:
			chat.AppendChat(5, "Aranacak kelime çok kýsa")
			return True
		
		self.SearchItem(searchText)
		return True

	def SearchItem(self, itemName):
		searchItemList = filter(lambda item: item[0].find(toLower(itemName)) != -1, constInfo.ITEM_SEARCH_DATA)
		
		if not searchItemList:
			chat.AppendChat(1, "%s içeren nesne bulunamadý." % itemName)
			return

		self.itemList = [item for item in searchItemList]
		self.pageMaxNum = len(self.itemList) / 9

		if len(self.itemList) % 9 > 0:
			self.pageMaxNum += 1

		self.pageNum = 0

		self.RefreshProcess()
	
	def previewButtonEvent(self, itemVnum, itemType, itemSubType, itemValue, itemAffect, itemHair):
		if not itemVnum:
			return
		
		if itemType == item.ITEM_TYPE_WEAPON:
			renderTarget.SetWeapon(6, itemVnum, player.GetRace())
		if itemType == item.ITEM_TYPE_ARMOR or (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_BODY):
			renderTarget.SetArmor(6, itemVnum, player.GetRace())
		if itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_HAIR:
			renderTarget.SetHair(6, itemHair,  player.GetRace())

				
	#def ShowShamanModel(self):
		#renderTarget.SelectRenderModel(6, 3)
		#renderTarget.SetArmor(6, 20759)
		#renderTarget.SetHair(6, 0)
		#renderTarget.SetWeapon(6, 7199)
		#renderTarget.SetVisibility(6, True)
			

	def buyButtonEvent(self, itemID, itemVnum, itemPrice, itemCount, itemMark):
		if itemVnum == 0:
			return

		item.SelectItem(itemVnum)
		if item.IsFlag(ITEM_FLAG_STACKABLE) and itemCount <= 1:
			self.itemStackalbeBuyDialog.SetItem(itemID, itemVnum)
			self.itemStackalbeBuyDialog.SetCountText(itemPrice, self.coins)#player total coin
			self.itemStackalbeBuyDialog.SetTitleName(item.GetItemName())
			self.itemStackalbeBuyDialog.Open()
		else:
			if itemPrice >= itemMark:
				self.buyQuestionDialog(itemID, itemVnum, item.GetItemName(), 1, itemPrice)
			else:
				self.buyQuestionDialog2(itemID, itemVnum, item.GetItemName(), 1, itemMark)

	def buyQuestionDialog(self, itemID, itemVnum, itemName, itemCount, itemPrice):
		self.questionDialog.SetText1(localeInfo.ASK_BUY_ITEM_TEXT % itemName)
		self.questionDialog.SetText2(localeInfo.DO_YOU_BUY_ITEM_COINS(itemCount, itemPrice))
		self.questionDialog.itemID = itemID
		self.questionDialog.itemVnum = itemVnum
		self.questionDialog.itemCount = itemCount
		self.questionDialog.SetWidth(385)
		self.questionDialog.SetTop()
		self.questionDialog.Open()
		
	def buyQuestionDialog2(self, itemID, itemVnum, itemName, itemCount, itemMark):
		self.questionDialog.SetText1(localeInfo.ASK_BUY_ITEM_TEXT % itemName)
		self.questionDialog.SetText2(localeInfo.DO_YOU_BUY_ITEM_MARK(itemCount, itemMark))
		self.questionDialog.itemID = itemID
		self.questionDialog.itemVnum = itemVnum
		self.questionDialog.itemCount = itemCount
		self.questionDialog.SetWidth(385)
		self.questionDialog.SetTop()
		self.questionDialog.Open()

	def QuestionDialogEvent(self, arg):
		if not self.questionDialog:
			return
		
		if arg:
			itemID = self.questionDialog.itemID
			itemCount = self.questionDialog.itemCount
			net.SendChatPacket("/nesne_market %d %d" % (itemID, itemCount))

		self.questionDialog.Close()
	
	def selectItemSlotEvent(self, itemIndex):
		itemPos = (self.pageNum * 9) + (itemIndex - 1)

		if len(self.itemList) <= itemPos:
				return

		(empty, itemID, itemVnum, itemPrice,itemPriceOld, itemCount, itemSocketZero, itemMark) = self.itemList[itemPos]

		if itemVnum == 0:
			return

		self.buyButtonEvent(itemID, itemVnum, itemPrice, itemCount, itemMark)

	def OverInItem(self, itemIndex):
		if not self.itemToolTip:
			return

		self.itemToolTip.ClearToolTip()
		itemPos = (self.pageNum * 9) + (itemIndex - 1)

		if len(self.itemList) <= itemPos:
				return

		(empty, itemID, itemVnum, itemPrice,itemPriceOld, itemCount, itemSocketZero, itemMark) = self.itemList[itemPos]

		if itemVnum == 0:
			return

		item.SelectItem(itemVnum)

		metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_BELT):
			itemSocketZero = itemSocketZero+app.GetGlobalTimeStamp()
			metinSlot = [itemSocketZero,0,0,0]
			
		if item.GetItemType() == item.ITEM_TYPE_RING:
			itemSocketZero = 0
			metinSlot = [0,0,0,0]
			
		if 27996 == int(itemVnum):
			metinSlot = [0,0,0,0]

		#if item.ITEM_TYPE_COSTUME == item.GetItemType() and item.GetItemName().rfind('+') != -1:
			#attrSlot[0] = [255, 1]
			
		# if item.ITEM_TYPE_BLEND == item.GetItemType():
			# blenditem = remastered.blend_item[itemVnum]
			# metinSlot = [blenditem[0],blenditem[1],BLEND_AFFECT_UNLIMITED_DURATION,0]

		self.itemToolTip.AddItemData(itemVnum, metinSlot, attrSlot)
		self.itemToolTip.Show()

	def OnOverOutItem(self):
		if not self.itemToolTip:
			return

		self.itemToolTip.ClearToolTip()
		self.itemToolTip.Hide()


	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()
			
# Item Shop Window
###################################################################################################
