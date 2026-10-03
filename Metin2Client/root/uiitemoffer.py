import ui
import net
import app
import chat
import constInfo
import localeInfo
import uiCommon
import chrmgr
import uiToolTip
import player
import wndMgr
import playerSettingModule
import chr
import item

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}

class OfferWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE GAME OPTION DIALOG"

	def __Initialize(self):
		self.prevButton = None
		self.pageText = None
		self.nextButton = None
		self.item_category = None
		self.priceInputBoard = None
		self.priceInputBoard2 = None
		self.questionDialog = None
		self.itemToolTip = None
		self.titleBar = 0
		self.pageMaxNum = 0
		self.pageNum = 0
		self.timerdone = 0
		self.timer = 0
		self.mypage = 0
		self.wndItemList = {}
		self.itemList = []
		self.add_type = 0
		
	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY GAME OPTION DIALOG"
	
	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("OfferDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.board = self.GetChild("board")
			self.LoadingImage = self.GetChild("LoadingImage")
			self.board_first = self.GetChild("board_first")
			self.board_second = self.GetChild("board_second")
			
			self.item_category = self.GetChild("item_category")
			self.yang_category = self.GetChild("yang_category")
			self.my_items = self.GetChild("my_items")
			self.my_yangs = self.GetChild("my_yangs")
			self.add_item = self.GetChild("add_item")
			self.add_yang = self.GetChild("add_yang")
			self.bank = self.GetChild("bank")
			
			self.prevButton = self.GetChild("prev_button")
			self.pageText = self.GetChild("page_text")
			self.nextButton = self.GetChild("next_button")
			
			self.characterName = self.GetChild("character_name")
			self.dragoncoin = self.GetChild("dragon_coin_text")
			
			for i in xrange(1, 10):
				number = "0%d" % i 

				if i >= 10:
					number = "%d" % i
					
				wndItemSlot = self.GetChild("itemSlot_%s" % number)
				#wndItemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.selectItemSlotEvent))
				#wndItemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.selectItemSlotEvent))
				wndItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				wndItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

				itemSlotImage = self.GetChild("itemslot_image_%s" % number)
				itemSlotImage.Hide()

				BuyButton = self.GetChild("itemBuyButton_%s" % number)
				BuyButton.Disable()
				BuyButton.ButtonText.SetFontColor(1.00,0.69,0.29)
				
				removeButton = self.GetChild("removeButton_%s" % number)
				removeButton.Disable()
				removeButton.ButtonText.SetFontColor(1.00,0.69,0.29)


				# yang #
				wndFaceSlot = self.GetChild("Face_Image_%s" % number)
				
				playerSlot = self.GetChild("Character_Name_Slot_%s" % number)
				priceSlot = self.GetChild("Money_Slot_%s" % number)
				Face_Slot = self.GetChild("Face_Slot_%s" % number)

				playerName = self.GetChild("Character_Name_%s" % number)
				playerName.SetLimitWidth(95)
				playerName.SetMultiLine()
				#playerName.SetFontName("Tahoma:13")
				playerName.SetPackedFontColor(0xFFFEE3AE)
				
				priceYang = self.GetChild("Money_%s" % number)
				priceYang.SetMax(15)
				priceYang.SetLimitWidth(95)
				priceYang.SetMultiLine()
				priceYang.SetPackedFontColor(0xFFFEE3AE)
				# yang #
				
				limitIcon = self.GetChild("limitIcon_%s" % number)
				limitIcon.Hide()
				
				
				itemSlot = self.GetChild("itemBoard_%s" % number)
				
				self.wndItemList[i] = (itemSlotImage, wndItemSlot, BuyButton, removeButton, itemSlot, wndFaceSlot, playerName, priceYang, playerSlot, priceSlot, Face_Slot)

		except:
			import exception
			exception.Abort("OfferDialog.__Load_BindObject")
			
		self.prevButton.SetEvent(ui.__mem_func__(self.prevButtonEvent))
		self.nextButton.SetEvent(ui.__mem_func__(self.nextButtonEvent))
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.item_category.SetEvent(ui.__mem_func__(self.ChangeCategory), 1)
		self.my_items.SetEvent(ui.__mem_func__(self.ChangeCategory), 2)
		self.yang_category.SetEvent(ui.__mem_func__(self.ChangeCategory), 3)
		self.my_yangs.SetEvent(ui.__mem_func__(self.ChangeCategory), 4)
		self.add_item.SetEvent(ui.__mem_func__(self.ClickAddGold), 1)
		self.add_yang.SetEvent(ui.__mem_func__(self.ClickAddGold), 2)
		self.bank.SetEvent(ui.__mem_func__(self.ClickBank))
		
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetAcceptEvent(lambda arg = True: self.QuestionDialogEvent(arg))
		self.questionDialog.SetCancelEvent(lambda arg = False: self.QuestionDialogEvent(arg))
		self.questionDialog.Hide()
		
		self.board_second.Hide()

	def __Load(self):
		self.__Load_LoadScript("uiscript/itemoffer.py")

		self.__Load_BindObject()

		self.SetCenterPosition()
		
	def OnUpdate(self):
		self.dragoncoin.SetText("%d TL" % int(player.GetTLPoint()))
		if self.timer <= app.GetTime() and self.timerdone == 0:
			net.SendChatPacket("/offer 1")
			net.SendChatPacket("/offer 2")
			net.SendChatPacket("/offer_yang 3")
			net.SendChatPacket("/offer_yang 4")
			self.timerdone = 1
			self.LoadingImage.Hide()
			self.board_second.Show()
			# self.ChangeCategory(1)
			# self.ClearDictionary()
			# self.__Initialize()
			# self.__Load()
			# self.Show()
			self.ChangeCategory(1)
			
	def SetItemToolTip(self, itemToolTip):
		self.itemToolTip = itemToolTip
			
	def ClickAddGold(self, type):
		self.add_type = type
		if type == 1:
			priceInputBoard = uiCommon.AddItemDialog()
		else:
			priceInputBoard = uiCommon.AddYangDialog()
		
		priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
		priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
		priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
		priceInputBoard.Open()
		
		self.priceInputBoard = priceInputBoard
		
	def AcceptInputPrice(self):
		if not self.priceInputBoard:
			return True
			
		type = self.add_type

		if type == 1:
			price = self.priceInputBoard.GetCoinText()
		else:
			price = self.priceInputBoard.GetText()

		if not price:
			return True

		if not price.isdigit():
			return True

		if long(price) <= 0:
			return True
			
		if type == 1:
			invenType = self.priceInputBoard.GetInvenType()
			slotPos = self.priceInputBoard.GetSlotPos()
			net.SendAddOfferItem(invenType, slotPos, int(price))
		else:
			yang = long(self.priceInputBoard.GetText())
			priceX = int(self.priceInputBoard.GetCoinText())
			net.SendChatPacket("/offer_add_gold %s %s" % (yang,priceX))
		
		self.ClearItem()
	
		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		self.priceInputBoard = None
		return True
		
	def ClearItem(self):
		net.SendChatPacket("/offer 1")
		net.SendChatPacket("/offer 2")
		net.SendChatPacket("/offer_yang 3")
		net.SendChatPacket("/offer_yang 4")
		self.timer = app.GetTime()+0.5
		self.timerdone = 0
		self.board_second.Hide()
		self.LoadingImage.Show()
		# constInfo.ITEM_OFFER_DATA = []
		# constInfo.ITEM_OFFER_DATA2 = []
		
	def ChangeCategory(self, page):
		self.ClearItemBoard()
		
		if int(page) == 1:
			count = len(constInfo.ITEM_OFFER_DATA)
			self.mypage = 2
		elif int(page) == 2:
			count = len(constInfo.ITEM_OFFER_DATA2)
			self.mypage = 1
		elif int(page) == 3:
			count = len(constInfo.EXCHANGE_YANG_DATA)
			self.mypage = 4
		else:
			count = len(constInfo.EXCHANGE_YANG_DATA2)
			self.mypage = 3

		self.pageMaxNum = count / 9
		
		if count % 9 > 0:
			self.pageMaxNum += 1
		
		self.pageNum = 0

		self.RefreshProcess()
		
	def ClearItemBoard(self):
		for i in xrange(1, 10):
			(itemSlotImage, wndItemSlot, BuyButton, removeButton, itemSlot, wndFaceSlot, playerName, priceYang, playerSlot, priceSlot, Face_Slot) = self.wndItemList[i]

			wndItemSlot.ClearSlot(i)
			wndItemSlot.RefreshSlot()
			
			wndFaceSlot.Hide()
			playerName.SetText("")
			priceYang.SetText("")
			itemSlotImage.Hide()
			
			playerSlot.Hide()
			priceSlot.Hide()
			Face_Slot.Hide()
			
			BuyButton.SetText("")
			BuyButton.Disable()
			removeButton.Hide()
			itemSlot.Hide()

		self.prevButton.Hide()
		self.nextButton.Hide()
		self.pageText.SetText("0/0")
		
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
			
			if int(self.mypage) == 1:
				if len(constInfo.ITEM_OFFER_DATA2) <= itemPos:
					return
			elif int (self.mypage) == 2:
				if len(constInfo.ITEM_OFFER_DATA) <= itemPos:
					return
			elif int (self.mypage) == 3:
				if len(constInfo.EXCHANGE_YANG_DATA2) <= itemPos:
					return
			elif int (self.mypage) == 4:
				if len(constInfo.EXCHANGE_YANG_DATA) <= itemPos:
					return

			(itemSlotImage, wndItemSlot, BuyButton, removeButton, itemSlot, wndFaceSlot, playerName, priceYang, playerSlot, priceSlot, Face_Slot) = self.wndItemList[i]
			
			itemSlotImage.Show()
			itemSlot.Show()
			
			if int(self.mypage) < 3:
				name = ""
				if int(self.mypage) == 2:
					(itemID, name, itemVnum, itemCount, price, socket0, socket1, socket2, type0, value0, type1, value1, type2, value2, type3, value3, type4, value4, type5, value5, type6, value6) = constInfo.ITEM_OFFER_DATA[itemPos]
				elif int(self.mypage) == 1:
					(itemID, itemVnum, itemCount, price, socket0, socket1, socket2, type0, value0, type1, value1, type2, value2, type3, value3, type4, value4, type5, value5, type6, value6) = constInfo.ITEM_OFFER_DATA2[itemPos]

				wndItemSlot.SetItemSlot(i, itemVnum, itemCount)
				wndItemSlot.RefreshSlot()
				wndFaceSlot.Hide()
				playerSlot.Show()
				playerName.SetText(name)
				priceSlot.Hide() 
				Face_Slot.Hide()
				
				item.SelectItem(itemVnum)
				
				if int(self.mypage) == 1:
					removeButton.Show()
					removeButton.SetText("Sil")
					removeButton.SetEvent(ui.__mem_func__(self.removeButtonEvent), itemID, 1)
					removeButton.Enable()
					BuyButton.Hide()
				else:
					BuyButton.Show()
					removeButton.Hide()
					BuyButton.SetText("%s TL" % localeInfo.NumberToMoneyStringNEW(price))
					BuyButton.SetEvent(ui.__mem_func__(self.buyButtonEvent), itemID, price, 1)
					BuyButton.Enable()
			else:
			
				if int(self.mypage) == 3:
					(itemID, name, yang, price, race) = constInfo.EXCHANGE_YANG_DATA2[itemPos]
				elif int(self.mypage) == 4:
					(itemID, name, yang, price, race) = constInfo.EXCHANGE_YANG_DATA[itemPos]
			
				faceImageName = FACE_IMAGE_DICT[race]
				wndFaceSlot.LoadImage(faceImageName)
				wndFaceSlot.Show()
				playerSlot.Show()
				priceSlot.Show() 
				Face_Slot.Show()

				priceYang.SetText("%s" % localeInfo.NumberToMoneyString(yang))
				playerName.SetText(name)
				
				if int(self.mypage) == 3:
					removeButton.Show()
					removeButton.SetText("Sil")
					removeButton.SetEvent(ui.__mem_func__(self.removeButtonEvent), itemID, 2)
					removeButton.Enable()
					BuyButton.Hide()
				else:
					BuyButton.Show()
					removeButton.Hide()
					BuyButton.SetText("%s TL" % localeInfo.NumberToMoneyStringNEW(price))
					BuyButton.SetEvent(ui.__mem_func__(self.buyButtonEvent), itemID, price, 2)
					BuyButton.Enable()

	def Open(self):
		# self.ClearDictionary()
		# self.__Initialize()
		# self.__Load()
		self.Show()
		net.SendChatPacket("/offer 1")
		net.SendChatPacket("/offer 2")
		net.SendChatPacket("/offer_yang 3")
		net.SendChatPacket("/offer_yang 4")
		self.timer = app.GetTime()+0.5
		self.timerdone = 0
		self.LoadingImage.Show()
		self.characterName.SetText(player.GetName())

	def buyButtonEvent(self, itemID, itemPrice, type):
		self.questionDialog.SetText("Satýn almak istiyor musun?")
		self.questionDialog.itemID = itemID
		self.questionDialog.type = type
		self.questionDialog.SetTop()
		self.questionDialog.Open()
		
		
	def QuestionDialogEvent(self, arg):
		if not self.questionDialog:
			return
		
		if arg:
			itemID = self.questionDialog.itemID
			type = self.questionDialog.type
			if type == 1:
				net.SendChatPacket("/buy_item %s" % itemID)
			else:
				net.SendChatPacket("/buy_offer_yang %s" % itemID)
			# net.SendChatPacket("/offer 1")
			# net.SendChatPacket("/offer 2")
			self.ClearItem()

		self.questionDialog.Close()
		
	def ClickBank(self):
		priceInputBoard2 = uiCommon.MoneyInputDialogYangShop()
		priceInputBoard2.SetTitle("Banka")
		priceInputBoard2.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice2))
		priceInputBoard2.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice2))
		priceInputBoard2.Open(player.GetExchangeCoin())
		
		self.priceInputBoard2 = priceInputBoard2
		
	def AcceptInputPrice2(self):

		if not self.priceInputBoard2:
			return True

		text = self.priceInputBoard2.GetText()

		if not text:
			return True

		if not text.isdigit():
			return True

		if long(text) <= 0:
			return True

		price = int(self.priceInputBoard2.GetText())

		net.SendChatPacket("/give_bank %s" % price)
		
		self.priceInputBoard2 = None
		return True

	def CancelInputPrice2(self):
		self.priceInputBoard2 = None
		return True
		
	def OverInItem(self, itemIndex):
		if not self.itemToolTip:
			return
		
		self.itemToolTip.ClearToolTip()
		itemPos = (self.pageNum * 9) + (itemIndex - 1)

		if len(constInfo.ITEM_OFFER_DATA) <= itemPos:
			return

		if self.mypage == 2:
			(itemID, name, itemVnum, itemCount, price, socket0, socket1, socket2, type0, value0, type1, value1, type2, value2, type3, value3, type4, value4, type5, value5, type6, value6) = constInfo.ITEM_OFFER_DATA[itemPos]
		else:
			(itemID, itemVnum, itemCount, price, socket0, socket1, socket2, type0, value0, type1, value1, type2, value2, type3, value3, type4, value4, type5, value5, type6, value6) = constInfo.ITEM_OFFER_DATA2[itemPos]


		if itemVnum == 0:
			return

		item.SelectItem(itemVnum)

		metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		
		if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
			attrSlot[0] = [type0, value0]
			attrSlot[1] = [type1, value1]
			attrSlot[2] = [type2, value2]
			attrSlot[3] = [type3, value3]
			attrSlot[4] = [type4, value4]
			attrSlot[5] = [type5, value5]
			attrSlot[6] = [type6, value6]
			
			metinSlot= [socket0,socket1,socket2,0,0,0]

		self.itemToolTip.AddItemData(itemVnum, metinSlot, attrSlot)
		self.itemToolTip.Show()

	def OnOverOutItem(self):
		if not self.itemToolTip:
			return

		self.itemToolTip.ClearToolTip()
		self.itemToolTip.HideToolTip()
		self.itemToolTip.Hide()
		
	def removeButtonEvent(self, itemID, type):
		if type == 1:
			net.SendChatPacket("/remove_item %s" % itemID)
		else:
			net.SendChatPacket("/remove_offer_yang %s" % itemID)
		self.timer = app.GetTime()+0.5
		self.timerdone = 0
		self.board_second.Hide()
		self.LoadingImage.Show()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.Hide()
		if self.questionDialog:
			self.questionDialog.Close()
		return True