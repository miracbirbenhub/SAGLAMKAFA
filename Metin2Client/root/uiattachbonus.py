import dbg
import player
import item
import net
import snd
import ui
import chat
import uiToolTip
import uiAttachBonusList
import bonus_settings
import app

class AttachBonusDialog(ui.ScriptWindow):

	if app.WJ_ENABLE_TRADABLE_ICON:
		def __init__(self, wndInventory):
			ui.ScriptWindow.__init__(self)
			self.attrButtonList = []
			self.sourceItemPos = 0
			self.targetItemPos = 0
			self.bonusListDlg = 0
			self.curItemType = 0
			self.curItemSubType = 0
			self.bonusType0 = 0
			self.bonusType1 = 0
			self.bonusType2 = 0
			self.bonusType3 = 0
			self.wndInventory = wndInventory
			self.lockedItems = {i:(-1,-1) for i in range(2)}
			self.__LoadScript()
	else:
		def __init__(self, wndInventory):
			ui.ScriptWindow.__init__(self)
			self.attrButtonList = []
			self.sourceItemPos = 0
			self.targetItemPos = 0
			self.bonusListDlg = 0
			self.curItemType = 0
			self.curItemSubType = 0
			self.bonusType0 = 0
			self.bonusType1 = 0
			self.bonusType2 = 0
			self.bonusType3 = 0
			self.wndInventory = wndInventory
			self.__LoadScript()

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, 'UIScript/AttachBonusDialog.py')
		except:
			import exception
			exception.Abort('AttachBonusDialog.__LoadScript.LoadObject')

		try:
			self.board = self.GetChild('Board')
			self.titleBar = self.GetChild('TitleBar')
			self.GetChild('AcceptButton').SetEvent(ui.__mem_func__(self.Accept))
			self.GetChild('CancelButton').SetEvent(ui.__mem_func__(self.Close))
			self.attrButtonList.append(self.GetChild('SelectBonusButton0'))
			self.attrButtonList.append(self.GetChild('SelectBonusButton1'))
			self.attrButtonList.append(self.GetChild('SelectBonusButton2'))
			self.attrButtonList.append(self.GetChild('SelectBonusButton3'))
		except:
			import exception
			exception.Abort('AttachBonusDialog.__LoadScript.BindObject')

		self.attrButtonList[0].SetEvent(ui.__mem_func__(self.__OnClickChangeMusicButton), 0)
		self.attrButtonList[1].SetEvent(ui.__mem_func__(self.__OnClickChangeMusicButton), 1)
		self.attrButtonList[2].SetEvent(ui.__mem_func__(self.__OnClickChangeMusicButton), 2)
		self.attrButtonList[3].SetEvent(ui.__mem_func__(self.__OnClickChangeMusicButton), 3)
		self.attrButtonList[0].SetToolTipText('Efsun Se\xe7', -90, 0)
		self.attrButtonList[1].SetToolTipText('Efsun Se\xe7', -90, 0)
		self.attrButtonList[2].SetToolTipText('Efsun Se\xe7', -90, 0)
		self.attrButtonList[3].SetToolTipText('Efsun Se\xe7', -90, 0)
		newToolTip = uiToolTip.ItemToolTip()
		newToolTip.SetParent(self)
		newToolTip.SetPosition(15, 38)
		newToolTip.SetFollow(False)
		newToolTip.Show()
		self.newToolTip = newToolTip
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.titleBar = 0
		self.toolTip = 0
		self.wndInventory = 0
		if app.WJ_ENABLE_TRADABLE_ICON:  
			self.wndInventory = 0

	def Open(self, sourceItemPos, targetItemPos):
		self.hideSecond = False
		self.sourceItemPos = sourceItemPos
		self.targetItemPos = targetItemPos
		itemIndex = player.GetItemIndex(targetItemPos)
		self.newToolTip.ClearToolTip()
		item.SelectItem(itemIndex)
		self.CheckAddonType(itemIndex)
		if self.curItemSubType != item.GetItemSubType() or self.curItemType != item.GetItemType():
			self.ResetAllValues()
		self.curItemType = item.GetItemType()
		self.curItemSubType = item.GetItemSubType()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(targetItemPos, i))

		self.newToolTip.AddRefineItemData(itemIndex, metinSlot, attrSlot)
		self.UpdateDialog()
		self.SetCenterPosition()
		self.SetTop()
		if app.WJ_ENABLE_TRADABLE_ICON:  
			self.SetCantMouseEventSlot(0, self.sourceItemPos)
			self.SetCantMouseEventSlot(1, self.targetItemPos)
		self.Show()

	def Update(self):
		self.hideSecond = False
		itemIndex = player.GetItemIndex(self.targetItemPos)
		self.newToolTip.ClearToolTip()
		item.SelectItem(itemIndex)
		self.CheckAddonType(itemIndex)
		if self.curItemSubType != item.GetItemSubType() or self.curItemType != item.GetItemType():
			self.ResetAllValues()
		self.curItemType = item.GetItemType()
		self.curItemSubType = item.GetItemSubType()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(self.targetItemPos, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(self.targetItemPos, i))

		self.newToolTip.AddRefineItemData(itemIndex, metinSlot, attrSlot)
		self.UpdateDialog()

	def UpdateDialog(self):
		newWidth = self.newToolTip.GetWidth() + 30
		newHeight = self.newToolTip.GetHeight() + 175
		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth - 15)
		self.SetSize(newWidth, newHeight)
		x, y = self.GetLocalPosition()
		self.SetPosition(x, y)

	def __OnClickChangeMusicButton(self, curSlotID):
		if not self.bonusListDlg:
			self.bonusListDlg = uiAttachBonusList.AttachBonusList()
			self.bonusListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)
		self.bonusListDlg.Open(curSlotID, self.targetItemPos)

	def __OnChangeMusic(self, bonusID, bonusText, curSlotID):
		self.attrButtonList[curSlotID].SetText(bonusText)
		if curSlotID == 0:
			self.bonusType0 = bonusID
		elif curSlotID == 1:
			self.bonusType1 = bonusID
		elif curSlotID == 2:
			self.bonusType2 = bonusID
		elif curSlotID == 3:
			self.bonusType3 = bonusID

	def CheckAddonType(self, itemIndex):
		addonItemList = bonus_settings.addonItemList
		for x in addonItemList:
			for y in xrange(x, x + 10):
				if itemIndex == y:
					self.hideSecond = True
					break

		if self.hideSecond == True:
			self.attrButtonList[2].Hide()
			self.attrButtonList[3].Hide()
		else:
			self.attrButtonList[2].Show()
			self.attrButtonList[3].Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Accept(self):
		if self.hideSecond:
			if self.bonusType0 == 0 or self.bonusType1 == 0:
				chat.AppendChat(chat.CHAT_TYPE_INFO, 'Efsunlarýn tamamýný seçmedin.')
				return
		elif self.bonusType0 == 0 or self.bonusType1 == 0 or self.bonusType2 == 0 or self.bonusType3 == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, 'Efsunlarýn tamamýný seçmedin.')
			return
		net.SendChatPacket("/add_new_attribute %s %s %s %s %s %s" % (self.sourceItemPos, self.targetItemPos, self.bonusType0, self.bonusType1, self.bonusType2, self.bonusType3))
		snd.PlaySound('sound/ui/pickup_item_in_inventory.wav')

	def ResetAllValues(self):
		self.bonusType0 = 0
		self.bonusType1 = 0
		self.bonusType2 = 0
		self.bonusType3 = 0
		for i in xrange(4):
			self.attrButtonList[i - 1].SetText('Efsun Seçilmedi')

	def Close(self):
		if app.WJ_ENABLE_TRADABLE_ICON:  
			self.SetCanMouseEventSlot(0, self.sourceItemPos)
			self.SetCanMouseEventSlot(1, self.targetItemPos)
		self.Hide()
		
	if app.WJ_ENABLE_TRADABLE_ICON:  
		def SetCanMouseEventSlot(self, what, slotIndex):
			itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItems[what] = (-1, -1)

			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCanMouseEventSlot(localSlotPos)

		def SetCantMouseEventSlot(self, what, slotIndex):
			itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItems[what] = (itemInvenPage, localSlotPos)

			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				for what, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()
