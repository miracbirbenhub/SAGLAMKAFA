import dbg
import player
import item
import net
import snd
import ui
import chat
import uiToolTip
import app

class PvMBonusDialog(ui.ScriptWindow):


	def __init__(self, wndInventory):
		ui.ScriptWindow.__init__(self)
		self.attrButtonList = []
		self.sourceItemPos = 0
		self.targetItemPos = 0
		self.curItemType = 0
		self.curItemSubType = 0
		self.children = []
		self.wndInventory = wndInventory
		self.__LoadScript()

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, 'UIScript/pvmbonusdialog.py')
		except:
			import exception
			exception.Abort('PvMBonusDialog.__LoadScript.LoadObject')

		try:
			self.board = self.GetChild('Board')
			self.titleBar = self.GetChild('TitleBar')
			self.GetChild('AcceptButton').SetEvent(ui.__mem_func__(self.Accept))
			self.GetChild('CancelButton').SetEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort('PvMBonusDialog.__LoadScript.BindObject')

		newToolTip = uiToolTip.ItemToolTip()
		newToolTip.SetParent(self)
		newToolTip.SetPosition(15+30, 38)
		newToolTip.SetFollow(False)
		newToolTip.Show()
		self.newToolTip = newToolTip
		
		self.slotList = []
		for i in xrange(3):
			slot = self.__MakeSlot()
			slot.SetParent(newToolTip)
			slot.SetWindowVerticalAlignCenter()
			self.slotList.append(slot)

		itemImage = self.__MakeItemImage()
		itemImage.SetParent(newToolTip)
		itemImage.SetWindowVerticalAlignCenter()
		itemImage.SetPosition(-35, 0)
		self.itemImage = itemImage
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __MakeSlot(self):
		slot = ui.ImageBox()
		slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
		slot.Show()
		self.children.append(slot)
		return slot

	def __MakeItemImage(self):
		itemImage = ui.ImageBox()
		itemImage.Show()
		self.children.append(itemImage)
		return itemImage

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.titleBar = 0
		self.toolTip = 0
		self.wndInventory = 0
		self.children = []

	def Open(self, sourceItemPos, targetItemPos):
		self.sourceItemPos = sourceItemPos
		self.targetItemPos = targetItemPos
		itemIndex = player.GetItemIndex(targetItemPos)
		self.newToolTip.ClearToolTip()
		item.SelectItem(itemIndex)
		self.curItemType = item.GetItemType()
		self.curItemSubType = item.GetItemSubType()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(targetItemPos, i))
			
		item.SelectItem(itemIndex)
		self.itemImage.LoadImage(item.GetIconImageFileName())
		xSlotCount, ySlotCount = item.GetItemSize()
		for slot in self.slotList:
			slot.Hide()
		for i in xrange(min(3, ySlotCount)):
			self.slotList[i].SetPosition(-35, i*32 - (ySlotCount-1)*16)
			self.slotList[i].Show()

		self.newToolTip.AddRefineItemData(itemIndex, metinSlot, attrSlot)
		self.UpdateDialog()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Update(self):
		self.hideSecond = False
		itemIndex = player.GetItemIndex(self.targetItemPos)
		self.newToolTip.ClearToolTip()
		item.SelectItem(itemIndex)
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
		newWidth = self.newToolTip.GetWidth() + 30 + 30
		newHeight = self.newToolTip.GetHeight() + 175 - 80
		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth - 15)
		self.SetSize(newWidth, newHeight)
		x, y = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Accept(self):
		net.SendItemUseToItemPacket(self.sourceItemPos, self.targetItemPos)
	
	def Close(self):
		self.Hide()

