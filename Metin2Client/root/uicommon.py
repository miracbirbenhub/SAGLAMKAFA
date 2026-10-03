import ui
import localeInfo
import app
import ime
import uiScriptLocale
import dbg

import constInfo
import item
import net
import mouseModule
import player

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())	
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		if localeInfo.IsARABIC() :
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "inputdialogwithdescription.py")
		else:
			pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True

class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)

class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(13)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(13, length)
		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))		


	def GetText(self):
		return self.inputValue.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)

		text = self.inputValue.GetText()

		money = 0

		if text and text.isdigit():
			try:
				money = long(text)
			except ValueError:
				money = 199999999

		self.moneyText.SetText(localeInfo.NumberToMoneyString2(money) + " Yang")

class QuestionGuildWar(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/guildwarquestion.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.textLine3 = self.GetChild("message3")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)

	def SetText3(self, text):
		self.textLine3.SetText(text)

class AddYangDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.SetMaxLength(13)
		self.SetMaxLengthCoin(9)


	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/addyangdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")
		self.InputValue_Coin = getObject("InputValue_Coin")
		self.InputValue_Coin.SetNumberMode()
		self.InputValue_Coin.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdateCoin)
		self.coinText = getObject("CoinValue")

	def Open(self):
		self.inputValue.SetText("0")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.InputValue_Coin.SetText("0")
		self.inputValue.SetFocus()
		self.__OnValueUpdateCoin()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.InputValue_Coin = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()
		self.InputValue_Coin.SetFocus()

	def SetMaxLength(self, length):
		length = min(13, length)
		self.inputValue.SetMax(length)

	def SetMaxLengthCoin(self, length):
		length = min(9, length)
		self.InputValue_Coin.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text
		self.coinHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event
		self.InputValue_Coin.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event
		self.InputValue_Coin.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))		

	def GetText(self):
		return self.inputValue.GetText()
		return self.InputValue_Coin.GetText()
			
	def GetCoinText(self):
		return self.InputValue_Coin.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)

		text = self.inputValue.GetText()
		text2 = self.InputValue_Coin.GetText()

		money = 0

		if text and text.isdigit():
			try:
				money = int(text)
			except ValueError:
				money = 1999999999999

		self.moneyText.SetText(localeInfo.NumberToMoneyStringNEW(money) + " Yang")

	def __OnValueUpdateCoin(self):
		ui.EditLine.OnIMEUpdate(self.InputValue_Coin)

		text = self.InputValue_Coin.GetText()

		coin = 0
		if text and text.isdigit():
			try:
				coin = int(text)
			except ValueError:
				coin = 999999999

		self.coinText.SetText(localeInfo.NumberToMoneyStringNEW(coin) + " TL")

class MoneyInputDialogYangShop(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.SetMaxLength(13)


	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/addyangdialog2.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")
		self.InputValue_Coin = getObject("InputValue_Coin")

	def Open(self, bank):
		self.inputValue.SetText("0")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.InputValue_Coin.SetText(str(bank))
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.InputValue_Coin = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(13, length)
		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text
		self.coinHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))		

	def GetText(self):
		return self.inputValue.GetText()
		return self.InputValue_Coin.GetText()
			
	def GetCoinText(self):
		return self.InputValue_Coin.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)

		text = self.inputValue.GetText()

		money = 0

		if text and text.isdigit():
			try:
				money = int(text)
			except ValueError:
				money = 1999999999999

		self.moneyText.SetText(localeInfo.NumberToMoneyStringNEW(money) + " TL")

class AddItemDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.attachedInvenType = None
		self.attachedSlotPos = None

		self.__CreateDialog()
		self.SetMaxLengthCoin(9)


	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/additemdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.itemSlot = self.GetChild("ItemSlot")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.InputValue_Coin = getObject("InputValue_Coin")
		self.InputValue_Coin.SetNumberMode()
		self.InputValue_Coin.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdateCoin)
		self.coinText = getObject("CoinValue")
		
		self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		#self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		#self.itemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		
	def OnSelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if (isAttached):
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY != attachedSlotType and \
					player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType and \
					player.SLOT_TYPE_UPGRADE_INVENTORY != attachedSlotType and \
					player.SLOT_TYPE_BOOK_INVENTORY != attachedSlotType and \
					player.SLOT_TYPE_STONE_INVENTORY != attachedSlotType and \
					player.SLOT_TYPE_ATTR_INVENTORY != attachedSlotType and \
					player.SLOT_TYPE_CHEST_INVENTORY != attachedSlotType:
					return

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)
			
			self.attachedInvenType = attachedInvenType
			self.attachedSlotPos = attachedSlotPos
		
			self.AddItem(itemVNum,1)

	def AddItem(self, vnum, count):
		self.itemSlot.SetItemSlot(0, vnum, 1)
		
	def GetInvenType(self):
		return self.attachedInvenType
		
	def GetSlotPos(self):
		return self.attachedSlotPos

	def Open(self):
		self.InputValue_Coin.SetText("0")
		self.__OnValueUpdateCoin()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		
	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.InputValue_Coin = None
		self.attachedInvenType = None
		self.attachedSlotPos = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.InputValue_Coin.SetFocus()

	def SetMaxLengthCoin(self, length):
		length = min(9, length)
		self.InputValue_Coin.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.coinHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.InputValue_Coin.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.InputValue_Coin.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))		

	def GetText(self):
		return self.InputValue_Coin.GetText()
			
	def GetCoinText(self):
		return self.InputValue_Coin.GetText()

	def __OnValueUpdateCoin(self):
		ui.EditLine.OnIMEUpdate(self.InputValue_Coin)

		text = self.InputValue_Coin.GetText()

		coin = 0
		if text and text.isdigit():
			try:
				coin = int(text)
			except ValueError:
				coin = 999999999

		self.coinText.SetText(localeInfo.NumberToMoneyStringNEW(coin) + " TL")
        
if app.WJ_NEW_DROP_DIALOG:
	class ItemQuestionDialog2(ui.ScriptWindow):

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/itemquestiondialog.py")
			self.board = self.GetChild('board')
			self.textLine = self.GetChild('message')
			self.textLine2 = self.GetChild('message2')
			self.textLine3 = self.GetChild('message3')
			self.deleteButton = self.GetChild('deletebutton')
			self.sellButton = self.GetChild('sellbutton')
			self.cancelButton = self.GetChild('cancelbutton')
			self.icon = self.GetChild("icon")

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.Hide()

		def SetWidth(self, width):
			height = self.GetHeight()
			self.SetSize(width, height)
			self.board.SetSize(width, height)
			self.SetCenterPosition()
			self.UpdateRect()

		def SetDeleteAcceptEvent(self, event):
			self.deleteButton.SetEvent(event)

		def SetSellAcceptEvent(self, event):
			self.sellButton.SetEvent(event)

		def SetCancelEvent(self, event):
			self.cancelButton.SetEvent(event)

		def SetText(self, text):
			self.textLine.SetText(text)

		def SetText2(self, text):
			self.textLine2.SetText(text)
			
		def SetText3(self, text):
			self.textLine3.SetText(text)
		
		def SetIcon(self,icon):
			self.icon.SetItemSlot(0,icon,0)

		def OnPressEscapeKey(self):
			self.Close()
			return True
		
if app.__ENABLE_NEW_OFFLINESHOP__:
	import wndMgr

	class MoneyInputDialogNew(ui.ScriptWindow):
		PATH_ROOT = "cream/shopseller/"
		
		def __init__(self, ItemVnum):
			ui.ScriptWindow.__init__(self)

			self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
			self.__CreateDialog(ItemVnum)
			self.SetMaxLength(13)
			self.SetCenterPosition()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self, ItemVnum):

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

			getObject = self.GetChild
			self.board = self.GetChild("board")
			self.board.Hide()
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputValue = getObject("InputValue")
			self.inputValue.SetNumberMode()
			self.inputValue.SetText("0")

			self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
			self.inputValue.OnPressEscapeKey = ui.__mem_func__(self.OnPressEscapeKey)
			self.moneyText = getObject("MoneyValue")
			
			self.__OnValueUpdate()

			self.board = ui.ExpandedImageBox()
			self.board.SetParent(self)
			self.board.AddFlag("not_pick")
			self.board.LoadImage(self.PATH_ROOT + "bg.tga")
			self.board.Show()

			self.acceptButton = ui.MakeButton(self, 25, 280, False, self.PATH_ROOT, "btn_norm.dds", "btn_hover.dds", "btn_down.dds")
			self.acceptButton.SetText("OK")

			self.cancelButton = ui.MakeButton(self, 125, 280, False, self.PATH_ROOT, "btn_norm.dds", "btn_hover.dds", "btn_down.dds")
			self.cancelButton.SetText("Close")
			
			self.boardItem = ui.ExpandedImageBox()
			self.boardItem.SetParent(self)
			self.boardItem.SetPosition(0, 140)
			self.boardItem.AddFlag("not_pick")
			self.boardItem.LoadImage(self.PATH_ROOT + "bg_item.dds")
			self.boardItem.SetWindowHorizontalAlignCenter()
			self.boardItem.Show()
			
			import item

			item.SelectItem(ItemVnum)

			self.ItemIcon = ui.ExpandedImageBox()
			self.ItemIcon.SetParent(self.boardItem)
			self.ItemIcon.SetPosition(0, 0)
			self.ItemIcon.LoadImage(item.GetIconImageFileName())
			self.ItemIcon.SetWindowHorizontalAlignCenter()
			self.ItemIcon.SetWindowVerticalAlignCenter()
			self.ItemIcon.Show()

			self.boardYang = ui.ExpandedImageBox()
			self.boardYang.SetParent(self)
			self.boardYang.SetPosition(25, 80)
			self.boardYang.LoadImage(self.PATH_ROOT + "price.dds")
			self.boardYang.Show()
			
			self.inputValue.SetParent(self.boardYang)
			self.inputValue.SetPosition(29, 8)
		
			self.wndNameItem = ui.MakeTextLineNew(self, 0, 120, item.GetItemName())
			self.wndNameItem.SetWindowHorizontalAlignCenter()
			self.wndNameItem.SetHorizontalAlignCenter()
			
			self.wndNameLine1 = ui.MakeTextLineNew(self, 0, 23, "Bu itemi ne kadara")
			self.wndNameLine1.SetWindowHorizontalAlignCenter()
			self.wndNameLine1.SetHorizontalAlignCenter()

			self.wndNameLine2 = ui.MakeTextLineNew(self, 0, 40, "satmak istiyorsun?")
			self.wndNameLine2.SetWindowHorizontalAlignCenter()
			self.wndNameLine2.SetHorizontalAlignCenter()

			self.moneyText.SetParent(self)
			self.moneyText.SetPosition(0, 257)
			self.moneyText.SetWindowHorizontalAlignCenter()
			self.moneyText.SetHorizontalAlignCenter()

			self.SetSize(self.board.GetWidth(), self.board.GetHeight())

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def Open(self):
			self.inputValue.SetText("")
			self.inputValue.SetFocus()
			self.__OnValueUpdate()
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.ClearDictionary()
			self.board = None
			self.acceptButton = None
			self.cancelButton = None
			self.inputValue = None
			self.Hide()

		def SetTitle(self, name):
			pass
			# self.board.SetTitleName(name)

		def SetFocus(self):
			self.inputValue.SetFocus()

		def SetMaxLength(self, length):
			length = min(13, length)
			self.inputValue.SetMax(length)

		def SetMoneyHeaderText(self, text):
			self.moneyHeaderText = text

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)
			self.inputValue.OnIMEReturn = event

		def SetCancelEvent(self, event):
			# self.board.SetCloseEvent(event)
			self.cancelButton.SetEvent(event)
			self.inputValue.OnPressEscapeKey = event

		def SetValue(self, value):
			value=str(value)
			self.inputValue.SetText(value)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(value))


		def GetText(self):
			return self.inputValue.GetText()

		def __OnValueUpdate(self):
			ui.EditLine.OnIMEUpdate(self.inputValue)

			text = self.inputValue.GetText()
			countK = text.count('x')
			if countK <= 3:
				text = text.replace('k', '000')
			money = 0
			if text and text.isdigit():
				try:
					money = min(9999999999999, long(text))
				except ValueError:
					money = 199999999
			
			self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))

	
	class ShopOfflinePopup(ui.Board):
		def __init__(self):
			ui.Board.__init__(self)
			
			self.isActiveSlide = False
			self.isActiveSlideOut = False
			self.endTime = 0
			self.wndWidth = 0
			
			self.textInfo = ui.TextLine()
			self.textInfo.SetParent(self)
			self.textInfo.SetWindowHorizontalAlignCenter()
			self.textInfo.SetWindowVerticalAlignCenter()
			self.textInfo.SetHorizontalAlignCenter()
			self.textInfo.SetVerticalAlignCenter()
			self.textInfo.SetPosition(20, 0)
			self.textInfo.SetText("|cff90EE90Sattýn:|r")
			self.textInfo.Show()

			self.textLineItemName = ui.TextLine()
			self.textLineItemName.SetParent(self)
			self.textLineItemName.SetWindowHorizontalAlignCenter()
			self.textLineItemName.SetWindowVerticalAlignCenter()
			self.textLineItemName.SetHorizontalAlignCenter()
			self.textLineItemName.SetVerticalAlignCenter()
			self.textLineItemName.SetPosition(20, 10)
			self.textLineItemName.SetText("itemName")
			self.textLineItemName.Show()
			
			self.textLineItemPrice = ui.TextLine()
			self.textLineItemPrice.SetParent(self)
			self.textLineItemPrice.SetWindowHorizontalAlignCenter()
			self.textLineItemPrice.SetWindowVerticalAlignCenter()
			self.textLineItemPrice.SetHorizontalAlignCenter()
			self.textLineItemPrice.SetVerticalAlignCenter()
			self.textLineItemPrice.SetPosition(20, 20)
			self.textLineItemPrice.SetText("itemPrice")
			self.textLineItemPrice.Show()

			self.slotItem = ui.GridSlotWindow()
			self.slotItem.SetParent(self)
			self.slotItem.SetPosition(10, 10)
			self.slotItem.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.slotItem.ArrangeSlot(0, 1, 3, 32, 32, 0, 0)
			self.slotItem.RefreshSlot()
			self.slotItem.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
			self.slotItem.Show()

			self.listNotification = {}

		def AddNotification(self, dwItemID, itemName, itemPrice, dwItemCount):
			self.listNotification[dwItemID] = [itemName, itemPrice, dwItemCount]
			self.Close()

		def __del__(self):
			ui.Board.__del__(self)

		def SlideIn(self, dwItemID, itemName, itemPrice, dwItemCount):
			self.SetTop()
			self.Show()
			
			self.isActiveSlide = True
			self.endTime = app.GetGlobalTimeStamp() + 4
			
			self.textLineItemName.SetText("|cffFFD700"+str(itemName)+"|r")
			self.textLineItemPrice.SetText("|cffFFB96D"+localeInfo.NumberToMoneyString(itemPrice)+"|r")

			self.wndWidth = 220
			self.SetSize(self.wndWidth, 118)
			self.textInfo.SetPosition(21, -30)
			self.textLineItemName.SetPosition(21, 4)
			self.textLineItemPrice.SetPosition(21, 14)
			self.SetPosition(-self.wndWidth, wndMgr.GetScreenHeight() - 290 - 32*4)
			
			self.slotItem.ClearSlot(0)
			self.slotItem.SetItemSlot(0, dwItemID, dwItemCount)

		def Close(self):
			if self.isActiveSlide:
				return

			if len(self.listNotification) == 0:
				self.Hide()
			else:
				for itemf in self.listNotification:
					self.SlideIn(itemf, self.listNotification[itemf][0], self.listNotification[itemf][1], self.listNotification[itemf][2])
					del self.listNotification[itemf]
					break

		def Destroy(self):
			self.Hide()
			self.listNotification = {}

		def OnUpdate(self):
			if self.isActiveSlide and self.isActiveSlide == True:
				x, y = self.GetLocalPosition()
				if x < 0:
					self.SetPosition(x + 4, y)
					
			if self.endTime - app.GetGlobalTimeStamp() <= 0 and self.isActiveSlideOut == False and self.isActiveSlide == True:
				self.isActiveSlide = False
				self.isActiveSlideOut = True
					
			if self.isActiveSlideOut and self.isActiveSlideOut == True:
				x, y = self.GetLocalPosition()
				if x > -(self.wndWidth):
					self.SetPosition(x - 4, y)
					
				if x <= -(self.wndWidth):
					self.isActiveSlideOut = False
					self.Close()