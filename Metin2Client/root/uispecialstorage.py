import ui
import player
import mouseModule
import net
import app
import snd
import item
import chat
import uiScriptLocale
import uiCommon
import uiPrivateShopBuilder
import uiPickMoney
import localeInfo
import constInfo
import uiPickEtc
import ime
if app.__ENABLE_NEW_OFFLINESHOP__:
	import offlineshop
	import uiofflineshop

class SpecialStorageWindow(ui.ScriptWindow):
	UPGRADE_TYPE = 0
	BOOK_TYPE = 1
	STONE_TYPE = 2
	sonbasma = 0
	if app.ENABLE_CUBE_RENEWAL:
		wndCubeRenewal = None
	
	SLOT_WINDOW_TYPE = {
		UPGRADE_TYPE	:	{"window" : player.UPGRADE_INVENTORY, "slot" : player.SLOT_TYPE_UPGRADE_INVENTORY},
		BOOK_TYPE	:	{"window" : player.BOOK_INVENTORY, "slot" : player.SLOT_TYPE_BOOK_INVENTORY},
		STONE_TYPE	:	{"window" : player.STONE_INVENTORY, "slot" : player.SLOT_TYPE_STONE_INVENTORY}
	}
	
	WINDOW_NAMES = {
		UPGRADE_TYPE	:	uiScriptLocale.UPGRADE_STORAGE_UPGRADE1,
		BOOK_TYPE	:	uiScriptLocale.UPGRADE_STORAGE_BOOK1,
		STONE_TYPE	:	uiScriptLocale.UPGRADE_STORAGE_STONE1,
	}
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.questionDialog = None
		self.tooltipItem = None
		self.dlgSplitItems = None
		self.wndItemDelete = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.inventoryPageIndex = 0
		self.categoryPageIndex = 0
		self.SetWindowName("SpecialStorageWindow")
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
			
		self.isLoaded = 1
		
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/SpecialStorageWindow.py")
		except:
			import exception
			exception.Abort("SpecialStorageWindow.LoadWindow.LoadObject")
			
		try:
			wndItem = self.GetChild("ItemSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.titleName = self.GetChild("TitleName")
			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))
			
			self.categoryTab = []
			self.categoryTab.append(self.GetChild("Category_Tab_01"))
			self.categoryTab.append(self.GetChild("Category_Tab_02"))
			self.categoryTab.append(self.GetChild("Category_Tab_03"))
			self.acceptbutton = self.GetChild("acceptbutton")
			self.cancelbutton = self.GetChild("cancelbutton")
			self.envyenile = self.GetChild("SeparateButton")
		except:
			import exception
			exception.Abort("SpecialStorageWindow.LoadWindow.BindObject")
			
		## Item
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))

		self.acceptbutton.SAFE_SetEvent(self.__envacilsinmi)
		self.cancelbutton.SAFE_SetEvent(self.__envacilmasinmi)
		
		## Grade button
		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg=3: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		
		self.categoryTab[0].SetEvent(lambda arg=0: self.SetCategoryPage(arg))
		self.categoryTab[1].SetEvent(lambda arg=1: self.SetCategoryPage(arg))
		self.categoryTab[2].SetEvent(lambda arg=2: self.SetCategoryPage(arg))
		self.categoryTab[0].Down()
		
		if self.envyenile:
			self.envyenile.SetEvent(ui.__mem_func__(self.envanterduzenle))
		
		## Etc
		self.wndItem = wndItem

		self.wndPopupDialog = uiCommon.PopupDialog()
		
		self.dlgSplitItems = uiPickEtc.PickEtcDialog()
		self.dlgSplitItems.LoadDialog()
		self.dlgSplitItems.Hide()
		
		self.SetInventoryPage(0)
		self.SetCategoryPage(0)
		self.RefreshItemSlot()
		self.RefreshBagSlotWindow()
		self.RefreshInvButton()
		
	def envanterduzenle(self):
		if app.GetTime() > self.sonbasma:
			net.SendChatPacket("/k_yenile")  
			self.sonbasma = app.GetTime() + 5
		else:
			v = self.sonbasma - app.GetTime()
			chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.envanteryenileme % (v))

	def __envacilsinmi(self):
		constInfo.INV_WITH_SPLIT = 1
		self.RefreshInvButton()
			
	def __envacilmasinmi(self):
		constInfo.INV_WITH_SPLIT = 0
		self.RefreshInvButton()
		
		
	def RefreshInvButton(self):
		if constInfo.INV_WITH_SPLIT == 1:
			self.acceptbutton.Down()
			self.cancelbutton.SetUp()
		else:
			self.cancelbutton.Down()
			self.acceptbutton.SetUp()
			
	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.questionDialog = None
		self.dlgSplitItems.Destroy()
		self.dlgSplitItems = None
		self.inventoryTab = []
		self.stonesell = 0
		self.titleName = None

	def Close(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		if self.dlgSplitItems:
			self.dlgSplitItems.Close()	
		self.Hide()

	def SetInventoryPage(self, page):			
		self.inventoryTab[self.inventoryPageIndex].SetUp()
		self.inventoryPageIndex = page
		self.inventoryTab[self.inventoryPageIndex].Down()

		self.RefreshBagSlotWindow()
		
	def SetCategoryPage(self, page):			
		self.categoryTab[self.categoryPageIndex].SetUp()
		self.categoryPageIndex = page
		self.categoryTab[self.categoryPageIndex].Down()
		
		self.titleName.SetText(self.WINDOW_NAMES[self.categoryPageIndex])
		self.RefreshBagSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()

	def RefreshStatus(self):
		self.RefreshItemSlot()

	def __InventoryLocalSlotPosToGlobalSlotPos(self, localSlotPos):
		return self.inventoryPageIndex * player.SPECIAL_PAGE_SIZE + localSlotPos

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVnum=self.wndItem.SetItemSlot
		
		for i in xrange(player.SPECIAL_PAGE_SIZE):
			self.wndItem.EnableSlot(i)
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)
			itemVnum = getItemVNum(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)
			
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0
				
			setItemVnum(i, itemVnum, itemCount)

		self.wndItem.RefreshSlot()

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])
			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uiofflineshop.IsBuildingShop():
					self.__AddTooltipSaleMode(slotIndex)

	if app.__ENABLE_NEW_OFFLINESHOP__:
		def __AddTooltipSaleMode(self, slot):
			if player.IsEquipmentSlot( self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slot):
				return

			itemIndex = player.GetItemIndex( self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slot)
			if itemIndex !=0:
				item.SelectItem(itemIndex)
				if item.IsAntiFlag(item.ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ANTIFLAG_GIVE):
					return
				
				self.tooltipItem.AddRightClickForSale()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)

		self.wndItem.SetUsableItem(False)
		self.ShowToolTip(overSlotPos)
		
	def OnPickItem(self, count):
		itemSlotIndex = self.dlgSplitItems.itemGlobalSlotIndex
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop() and uiofflineshop.IsSaleSlot( self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		selectedItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"], itemSlotIndex, selectedItemVNum, count)
				
	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)
		selectedItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
		itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
		
		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemCount  = mouseModule.mouseController.GetAttachedItemCount()

			if self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"] == attachedSlotType:
				if attachedItemVID == selectedItemVNum:
					net.SendItemMovePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex, 0) #This modifi: last value: attachedItemCount
				else:
					net.SendItemUseToItemPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)

			mouseModule.mouseController.DeattachObject()
		else:
			curCursorNum = app.GetCursor()
			
			if app.ENABLE_SHOW_CHEST_DROP:
				item.SelectItem(selectedItemVNum)
					
				if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
					if app.IsPressed(app.DIK_LCONTROL):
						if self.interface:
							if self.interface.dlgChestDrop:
								if not self.interface.dlgChestDrop.IsShow():
									self.interface.dlgChestDrop.Open(itemSlotIndex)
									net.SendChestDropInfo(itemSlotIndex, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])
									return

			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],itemSlotIndex)
				ime.PasteString(link)
	
			elif app.IsPressed(app.DIK_LSHIFT):
				if itemCount > 1:
					self.dlgSplitItems.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgSplitItems.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgSplitItems.Open(itemCount)
					self.dlgSplitItems.itemGlobalSlotIndex = itemSlotIndex
			else:
				mouseModule.mouseController.AttachObject(self, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"], itemSlotIndex, selectedItemVNum, itemCount)
				self.wndItem.SetUseMode(False)
				snd.PlaySound("sound/ui/pick.wav")

	def __SellItem(self, itemSlotPos):
		self.sellingSlotNumber = itemSlotPos
		itemIndex = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotPos)
		itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotPos)

		item.SelectItem(itemIndex)

		if item.IsAntiFlag(item.ANTIFLAG_SELL):
			popup = uiCommon.PopupDialog()
			popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
			popup.SetAcceptEvent(self.__OnClosePopupDialog)
			popup.Open()
			self.popup = popup
			return

		itemPrice = item.GetISellItemPrice()

		if item.Is1GoldItem():
			itemPrice = itemCount / itemPrice
		else:
			itemPrice = itemPrice * itemCount

		item.GetItemName(itemIndex)
		itemName = item.GetItemName()

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.count = itemCount

	def SellItem(self):
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop() and uiofflineshop.IsSaleSlot( self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], self.sellingSlotNumber):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

	def __OnClosePopupDialog(self):
		self.pop = None

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)
		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uiofflineshop.IsBuildingShop() and uiofflineshop.IsSaleSlot(player.SlotTypeToInvenType(attachedSlotType),attachedSlotPos):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
					return
			
			if player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
				net.SendSafeboxCheckoutPacket(attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos)
			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos)
			elif player.RESERVED_WINDOW != attachedInvenType:
				itemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()

				self.__SendMoveItemPacket(attachedInvenType, attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos, attachedCount)

			mouseModule.mouseController.DeattachObject()

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return
		windowIndex = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop():
				globalSlot 	= self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
				itemIndex 	= player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], globalSlot)
				
				item.SelectItem(itemIndex)
				
				if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
					offlineshop.ShopBuilding_AddItem(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], globalSlot)
				
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				
				return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
		
		ItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)
		item.SelectItem(ItemVNum)
		bool = False;
		
		if self.isShowDeleteItemDlg():
			self.wndItemDelete.AddItemWithoutMouse(windowIndex, slotIndex)
			return

		if bool == True:
		# if item.GetFlags() == 256:
			self.questionDialog = uicommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex
		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		elif item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
			if app.IsPressed(app.DIK_LCONTROL):
				net.SendItemUseAllPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],slotIndex)
			else:
				net.SendItemUsePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)
		else:
			net.SendItemUsePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)

		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotWindow , srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	if app.ENABLE_CUBE_RENEWAL:
		def SetCubeRenewalDlg(self, wndCubeRenewal):
			self.wndCubeRenewal = wndCubeRenewal
		
		def isShowCubeRenewalDlg(self):
			if self.wndCubeRenewal:
				if self.wndCubeRenewal.IsShow():
					return 1
					
			return 0

	if app.ENABLE_ITEM_DELETE_SYSTEM:
		def SetDeleteItemDlg(self, wndItemDelete):
			self.wndItemDelete = wndItemDelete

		def isShowDeleteItemDlg(self):
			if self.wndItemDelete:
				if self.wndItemDelete.IsShow():
					return 1
			return 0