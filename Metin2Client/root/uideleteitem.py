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
import uiPickMoney
import localeInfo
import constInfo
import uiToolTip

from grid import Grid

BILGI_AL = [
	"Neslereri sürükleyerek ekleyebilirsiniz.",
	"Silmekten vazgeçtiðiniz nesnenin üstüne týklayarak kaldýrabilirsiniz.",
]

class DeleteItem(ui.ScriptWindow):
	def __init__(self):	
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.itemStock = {}
		self.money = 0
		constInfo.ITEM_DELETE_LIST = {}
		self.tooltipItem = None
		self.itemDropQuestionDialog = None
		self.bilgialbuton = None
		self.DeleteGrid = None
		self.interface = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/DeleteItem.py")
		except:
			import exception
			exception.Abort("OfflineShopBuilderWindow.LoadWindow.LoadObject")
			
		try:
			self.itemSlot = self.GetChild("ItemSlot")
			self.btnOk = self.GetChild("OkButton")
			self.btnSat = self.GetChild("SatButton")
			self.btnClose = self.GetChild("CloseButton")
			self.btnIptal = self.GetChild("VazgecButton")
			self.board = self.GetChild("Board")
			self.bilgialbuton = self.GetChild("bilgialkardes")
			self.toplamfiyat = self.GetChild("toplamfiyat")
		except:
			import exception
			exception.Abort("OfflineShopBuilderWindow.LoadWindow.BindObject")
			
		self.btnOk.SetEvent(ui.__mem_func__(self.OnOk))
		self.btnSat.SetEvent(ui.__mem_func__(self.OnSat))
		self.btnClose.SetEvent(ui.__mem_func__(self.Temizle))
		self.board.SetCloseEvent(ui.__mem_func__(self.OnClose))
		self.btnIptal.SetEvent(ui.__mem_func__(self.OnClose))
		
		self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		self.itemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		
		self.bilgialbuton.SetToolTipWindow2(self.__ToolTipOlustur("Bilgilendirme", BILGI_AL))
	
	def Destroy(self):
		self.ClearDictionary()
		
		self.itemSlot = None
		self.btnOk = None
		self.btnSat = None
		self.btnClose = None
		self.board = None
		self.itemDropQuestionDialog = None
		self.bilgialbuton = None
		self.DeleteGrid = None
		self.toplamfiyat = None

	def BindInterface(self, interface):
		self.interface = interface

	def Open(self):
		self.Temizle()
		self.SetCenterPosition()
		self.Refresh()
		self.DeleteGrid = Grid(width=6, height=10)
		self.Show()
		if constInfo.silme == 0:
			constInfo.silme = 1

	def Close(self):
		self.itemStock = {}
		self.money = 0
		constInfo.ITEM_DELETE_LIST = {}
		self.Hide()
		if constInfo.silme == 1:
			constInfo.silme = 0

	def Temizle(self):
		self.itemStock = {}
		self.money = 0
		self.DeleteGrid = Grid(width=6, height=10)
		constInfo.ITEM_DELETE_LIST = {}
		self.Refresh()

	def __ToolTipOlustur(self, title, descList):
		toolTip = uiToolTip.ToolTip()
		toolTip.SetTitle(title)

		for desc in descList:
			toolTip.AutoAppendTextLine(desc)

		toolTip.AlignHorizonalCenter()
		toolTip.SetTop()
		return toolTip

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Refresh(self):
		for i in xrange(60):
			if (not self.itemStock.has_key(i)):
				self.itemSlot.ClearSlot(i)
				continue

			pos = self.itemStock[i]
			itemCount = player.GetItemCount(*pos)
			if (itemCount <= 1):
				itemCount = 0
			self.itemSlot.SetItemSlot(i, player.GetItemIndex(*pos), itemCount)

		self.money = 0
		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
			self.money += long(player.GetISellItemPrice(itemWindowType, itemSlotIndex))

		self.itemSlot.RefreshSlot()

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
					player.SLOT_TYPE_CHEST_INVENTORY != attachedSlotType:
					return
			else:
				if (player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType):
					return

			if (selectedSlotPos in self.itemStock):
				return

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			attrSlot = [player.GetItemAttribute(attachedSlotPos, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			if player.IsEquipmentSlot(attachedSlotPos):
				self.uyari2 = uiCommon.PopupDialog()
				self.uyari2.SetText("Giyili itemleri silemezsin.")
				self.uyari2.Open()
				return

			(width, height) = item.GetItemSize()
			
			for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
				if itemWindowType == attachedInvenType and itemSlotIndex == attachedSlotPos:
					del self.itemStock[selectedSlotPos]
					del constInfo.ITEM_DELETE_LIST[selectedSlotPos]
					self.DeleteGrid.clear(selectedSlotPos, width, height)

			available_position = self.DeleteGrid.find_blank(width, height)
			if available_position != -1:
				self.DeleteGrid.put(selectedSlotPos, width, height)

			self.itemStock[selectedSlotPos] = (attachedInvenType, attachedSlotPos)
			constInfo.ITEM_DELETE_LIST[selectedSlotPos] = (attachedInvenType, attachedSlotPos)
			# self.CheckItem(attachedInvenType, attachedSlotPos)
			self.Refresh()

	def OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if (isAttached):
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()

		else:
			if (not selectedSlotPos in self.itemStock):
				return

			invenType, invenPos = self.itemStock[selectedSlotPos]
			del self.itemStock[selectedSlotPos]
			del constInfo.ITEM_DELETE_LIST[selectedSlotPos]
			
			itemVNum = player.GetItemIndex(invenType, invenPos)
			item.SelectItem(itemVNum)
			# self.money -= long(item.GetISellItemPrice() * player.GetItemCount(invenType, invenPos))
			# self.money -= long(player.GetISellItemPrice(invenType, invenPos))
			(width, height) = item.GetItemSize()

			self.DeleteGrid.clear(selectedSlotPos, width, height)
			
			self.Refresh()
	def AddItemWithoutMouse(self, inven_type, inven_pos):
		itemID = player.GetItemIndex(inven_type, inven_pos)
		item.SelectItem(itemID)
		if player.IsEquipmentSlot(inven_pos):
			self.uyari2 = uiCommon.PopupDialog()
			self.uyari2.SetText("Giyili itemleri silemezsin.")
			self.uyari2.Open()
			return
		(width, height) = item.GetItemSize()
		available_position = self.DeleteGrid.find_blank(width, height)
		
		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
			if itemWindowType == inven_type and itemSlotIndex == inven_pos:
				return

		if available_position != -1:
			self.DeleteGrid.put(available_position, width, height)
			self.itemStock[available_position] = (inven_type, inven_pos)
			constInfo.ITEM_DELETE_LIST[available_position] = (inven_type, inven_pos)
			# self.CheckItem(inven_type, inven_pos)
			# self.money += long(item.GetISellItemPrice() * player.GetItemCount(inven_type, inven_pos))
			# self.money += long(player.GetISellItemPrice(inven_type, inven_pos))
			self.Refresh()

	def OnOk(self):
		if (len(self.itemStock) == 0):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Silinecek nesne yok.")
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText("Seçilen (|cffFDD017|h%d Adet|h|r) nesneyi silmek istiyor musun?" % (len(self.itemStock)))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def OnSat(self):
		if (len(self.itemStock) == 0):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Satýlacak nesne yok.")
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText("Seçilen (|cffFDD017|h%d Adet|h|r) nesneyi satmak istiyor musun?" % (len(self.itemStock)))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestSellItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestSellItem(arg))
		itemDropQuestionDialog.Open()
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def Sil(self):
		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():

			net.SendItemDeletePacket(itemSlotIndex, itemWindowType)
			del self.itemStock[privatePos]
			del constInfo.ITEM_DELETE_LIST[privatePos]

			self.DeleteGrid = Grid(width=6, height=10)
			self.money = 0
			self.Refresh()

	def Sat(self):
		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():

			net.SendItemSellPacket(itemSlotIndex, itemWindowType)
			del self.itemStock[privatePos]
			del constInfo.ITEM_DELETE_LIST[privatePos]
			
			self.DeleteGrid = Grid(width=6, height=10)
			self.money = 0
			self.Refresh()

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			self.Sil()

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

	def RequestSellItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			self.Sat()

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None


	def OnClose(self):
		self.Close()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnOverInItem(self, slotIndex):
		if (self.tooltipItem):
			if (self.itemStock.has_key(slotIndex)):
				self.tooltipItem.SetDeleteItem(*self.itemStock[slotIndex] + (slotIndex,))

	def OnOverOutItem(self):
		if (self.tooltipItem):
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		self.toplamfiyat.SetText("(|cffFDD017|h%s|h|r)" % (localeInfo.NumberToMoneyString(self.money)))
