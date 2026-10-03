import net, ui, uiToolTip, player, item, exception, chat, constInfo, uiScriptLocale, app

class ChangerWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.ChangerPosition = None # Changer Pos
		self.ItemPosition = None # Item Pos
		self.ChangersCount = 0
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/bonuschanger.py")
		except:
			exception.Abort("ChangerWindow.LoadDialog.LoadObject")

		try:
			self.board = self.GetChild('Board')
			self.titleBar = self.GetChild('TitleBar')
			self.ChangeBonusButton = self.GetChild("AcceptButton")
			self.GetChild('CancelButton').SetEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort("ChangerWindow.LoadDialog.BindObject")

		self.ChangeBonusButton.SetEvent(ui.__mem_func__(self.ChangeBonus))
		newToolTip = uiToolTip.ItemToolTip()
		newToolTip.SetParent(self)
		newToolTip.SetPosition(15, 38)
		newToolTip.SetFollow(False)
		newToolTip.Show()
		self.newToolTip = newToolTip
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def AddItems(self, itemPositon, changerPosition):
		self.ChangerPosition = changerPosition
		self.ItemPosition = itemPositon
		itemIndex = player.GetItemIndex(self.ItemPosition)
		self.newToolTip.ClearToolTip()
		self.ChangersCount = player.GetItemCount(self.ChangerPosition)
		item.SelectItem(itemIndex)
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(self.ItemPosition, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(self.ItemPosition, i))

		self.newToolTip.AddRefineItemData(itemIndex, metinSlot, attrSlot)
		self.UpdateDialog()
		self.SetCenterPosition()
		self.SetTop()
		
		self.Open()

	def ChangeBonus(self):
		if self.ChangerPosition == None or self.ItemPosition == None:
			return
			
		if self.ChangersCount > 0:
			self.ChangersCount = self.ChangersCount-1
			net.SendItemUseToItemPacket(self.ChangerPosition, self.ItemPosition)
			
				
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.BONUS_CHANGER_ERROR)

	def OnUpdate(self):
		itemIndex = player.GetItemIndex(self.ItemPosition)
		self.newToolTip.ClearToolTip()
		item.SelectItem(itemIndex)
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(self.ItemPosition, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(self.ItemPosition, i))

		self.newToolTip.AddRefineItemData(itemIndex, metinSlot, attrSlot)
		self.UpdateDialog()

	def UpdateDialog(self):
		newWidth = self.newToolTip.GetWidth() + 30
		newHeight = self.newToolTip.GetHeight() + 90
		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth - 15)
		self.SetSize(newWidth, newHeight)
		x, y = self.GetLocalPosition()
		self.SetPosition(x, y)

		
	def Destroy(self):
		self.board = 0
		self.titleBar = 0
		self.toolTip = 0
		self.Close()
	
	def OnPressEscapeKey(self):
		self.Close()
		return TRUE
		
	def Close(self):
		if self.IsShow():
			self.ChangerPosition = None
			self.ItemPosition = None
			constInfo.IS_BONUS_CHANGER = FALSE
			self.Hide()

	def Open(self):
		constInfo.IS_BONUS_CHANGER = TRUE
		self.Show()
