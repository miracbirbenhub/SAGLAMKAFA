import dbg
import ui
import snd
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import chrmgr
import player
import background
import uiCommon
import grp
import colorInfo

class GMPaneL(ui.ScriptWindow):

	KIRMIZI = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE SYSTEM OPTION DIALOG"

	def __Initialize(self):
		self.tilingMode = 0
		self.titleBar = 0
		## MAVI RUH DEAKTIF BUTTONS ##
		#self.materialButton = 0
		#self.chestButton = 0
		#self.stoneButton = 0
		## MAVI RUH DEAKTIF BUTTONS ##
		self.infoButton = 0
		self.heromanButton = 0
		self.kickButton = 0
		self.cleaninventoryButton = 0
		self.levelmeButton = 0
		self.fullButton = 0
		self.skillperfectButton = 0
		self.skyboxButton = 0
		self.oxmapButton = 0
		self.noticeButton = 0
		self.eternalButton = 0
		self.leveluserButton = 0
		self.invisibleButton = 0
		self.npcButton = 0
		self.muteButton = 0
		
	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY SYSTEM OPTION DIALOG"

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("System.OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			## MAVI RUH DEAKTIF BUTTONS ##
			#self.materialButton = GetObject("material_button")
			#self.chestButton = GetObject("chest_button")
			#self.stoneButton = GetObject("stone_button")
			## MAVI RUH DEAKTIF BUTTONS ##
			self.infoButton = GetObject("info_button")
			self.heromanButton = GetObject("heroman_button")
			self.kickButton = GetObject("kick_button")
			self.cleaninventoryButton = GetObject("cleaninventory_button")
			self.levelmeButton = GetObject("levelme_button")
			self.fullButton = GetObject("full_button")
			self.skillperfectButton = GetObject("skillperfect_button")
			self.skyboxButton = GetObject("skybox_button")
			self.oxmapButton = GetObject("oxmap_button")
			self.noticeButton = GetObject("notice_button")
			self.eternalButton = GetObject("eternal_button")
			self.leveluserButton = GetObject("leveluser_button")
			self.invisibleButton = GetObject("invisible_button")
			self.npcButton = GetObject("npc_button")
			self.muteButton = GetObject("mute_button")

		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/gamemasterpanel.py")
		self.__Load_BindObject()

		self.SetCenterPosition()
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		## MAVI RUH DEAKTIF BUTTONS ##
		#self.materialButton.SAFE_SetEvent(self.__OnClickMaterialButton)
		#self.chestButton.SAFE_SetEvent(self.__OnClickChestButton)
		#self.stoneButton.SAFE_SetEvent(self.__OnClickStoneButton)
		## MAVI RUH DEAKTIF BUTTONS ##
		self.infoButton.SAFE_SetEvent(self.__OnClickInfoButton)
		self.heromanButton.SAFE_SetEvent(self.__OnClickHeroManButton)
		self.kickButton.SAFE_SetEvent(self.__OnClickKickButton)
		self.cleaninventoryButton.SAFE_SetEvent(self.__OnClickCleanInventoryButton)
		self.levelmeButton.SAFE_SetEvent(self.__OnClickLevelMeButton)
		self.fullButton.SAFE_SetEvent(self.__OnClickFullButton)
		self.skillperfectButton.SAFE_SetEvent(self.__OnClickPerfectSkillButton)
		self.skyboxButton.SAFE_SetEvent(self.__OnClickSkyboxButton)
		self.oxmapButton.SAFE_SetEvent(self.__OnClickOxMapButton)
		self.noticeButton.SAFE_SetEvent(self.__OnClickNoticeButton)
		self.eternalButton.SAFE_SetEvent(self.__OnClickEternalButton)
		self.leveluserButton.SAFE_SetEvent(self.__OnClickLevelUserButton)
		self.invisibleButton.SAFE_SetEvent(self.__OnClickInvisibleButton)
		self.npcButton.SAFE_SetEvent(self.__OnClickNpcButton)
		self.muteButton.SAFE_SetEvent(self.__OnClickMuteButton)

########################################################################################################################
	def __OnClickInfoButton(self):
		InfoBoard = Info()
		InfoBoard.SetTitle(localeInfo.CHAT_INFORMATION)
		InfoBoard.Open()
		self.InfoBoard = InfoBoard
########################################################################################################################

	## MAVI RUH DEAKTIF BUTTONS ##
	#def __OnClickMaterialButton(self):
	#	net.SendChatPacket("/give_me_material")

	#def __OnClickChestButton(self):
	#	net.SendChatPacket("/give_me_chest")

	#def __OnClickStoneButton(self):
	#	net.SendChatPacket("/give_me_stone")
	## MAVI RUH DEAKTIF BUTTONS ##

########################################################################################################################
	def __OnClickHeroManButton(self):
		self.Close()
		friendNameBoard2 = HeroMan()
		friendNameBoard2.SetTitle(localeInfo.GAMEMASTER_PANEL_HEROMAN)
		friendNameBoard2.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend2))
		friendNameBoard2.SetCancelEvent(ui.__mem_func__(self.OnCancelAddFriend2))
		friendNameBoard2.Open()
		self.friendNameBoard2 = friendNameBoard2

	def OnAddFriend2(self):
		text = self.friendNameBoard2.GetText()
		net.SendChatPacket("/set " + text + " align 999999")
		self.friendNameBoard2.Hide()

	def OnCancelAddFriend2(self):
		self.friendNameBoard2.Hide()
########################################################################################################################

########################################################################################################################
	def __OnClickKickButton(self):
		self.Close()
		friendNameBoard3 = HeroMan()
		friendNameBoard3.SetTitle(localeInfo.GAMEMASTER_PANEL_KICK)
		friendNameBoard3.SetAcceptEvent(ui.__mem_func__(self.__ClickKickAskButton))
		friendNameBoard3.SetCancelEvent(ui.__mem_func__(self.OnCancelAddFriend3))
		friendNameBoard3.Open()
		self.friendNameBoard3 = friendNameBoard3

	def __ClickKickAskButton(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Bu kararýný onaylýyor musun ?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend3))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.Hayir))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def OnAddFriend3(self):
		self.questionDialog.Close()
		text = self.friendNameBoard3.GetText()
		net.SendChatPacket("/dc " + text)
		self.friendNameBoard3.Hide()

	def OnCancelAddFriend3(self):
		self.friendNameBoard3.Hide()
########################################################################################################################

########################################################################################################################
	def __OnClickCleanInventoryButton(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.GAMEMASTER_PANEL_CLEAN_INVENTORY)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend4))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.Hayir))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def OnAddFriend4(self):
		net.SendChatPacket("/ip inventory")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Envanter baþarýyla temizlendi.")
		self.questionDialog.Close()
########################################################################################################################

########################################################################################################################
	def __OnClickFullButton(self):
		self.Close()
		net.SendChatPacket("/item_full_set")
		net.SendChatPacket("/attr_full_set")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Efsunlu itemler üstüne giyildi.")
########################################################################################################################

########################################################################################################################
	def __OnClickPerfectSkillButton(self):
		net.SendChatPacket("/all_skill_master")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Tüm becerilerin perfect oldu. (binicilik,skiller,dönüþüm,balýk...)")
########################################################################################################################

########################################################################################################################
	def __OnClickLevelMeButton(self):
		self.Close()
		friendNameBoard = LevelciMaviRuh()
		friendNameBoard.SetTitle(localeInfo.GAMEMASTER_PANEL_LEVEL_ME)
		friendNameBoard.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend))
		friendNameBoard.SetCancelEvent(ui.__mem_func__(self.OnCancelAddFriend))
		friendNameBoard.Open()
		self.friendNameBoard = friendNameBoard

	def OnAddFriend(self):
		text = self.friendNameBoard.GetText()
		net.SendChatPacket("/level " + text)
		chat.AppendChat(chat.CHAT_TYPE_INFO, text + " seviye oldun.")
		self.friendNameBoard.Hide()

	def OnCancelAddFriend(self):
		self.friendNameBoard.Hide()
########################################################################################################################

########################################################################################################################
	def __OnClickSkyboxButton(self):
		self.Close()
		questionDialog25 = HeroMan()
		questionDialog25.SetTitle(localeInfo.GAMEMASTER_PANEL_BAN)
		questionDialog25.SetAcceptEvent(ui.__mem_func__(self.__ClickBanAskButton))
		questionDialog25.SetCancelEvent(ui.__mem_func__(self.OnCancelBanButton))
		questionDialog25.Open()
		self.questionDialog25 = questionDialog25

	def __ClickBanAskButton(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Bu kararýný onaylýyor musun ?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAccepBan))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.Hayir))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def OnAccepBan(self):
		self.questionDialog.Close()
		text = self.questionDialog25.GetText()
		net.SendChatPacket("/hwid_ban " + text + " ban")
		self.questionDialog25.Hide()

	def OnCancelBanButton(self):
		self.questionDialog25.Hide()
########################################################################################################################

########################################################################################################################
	def __OnClickOxMapButton(self):
		self.Close()
		MapName = str(background.GetCurrentMapName()) 
		if MapName == "season1/metin2_map_oxevent": 
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(localeInfo.GAMEMASTER_PANEL_OX_FLOWER)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend5544))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.Hayir))
			questionDialog.Open()
			self.questionDialog = questionDialog
		else:
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(localeInfo.GAMEMASTER_PANEL_OX)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend554))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.Hayir))
			questionDialog.Open()
			self.questionDialog = questionDialog

	def OnAddFriend554(self):
		net.SendChatPacket("/go ox")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Ox haritasýna ýþýnlanýlýyor...")
		self.Close()
		self.questionDialog.Close()

	def OnAddFriend5544(self):
		net.SendChatPacket("/mob 20358")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Ýsimsiz Çiçekler yanýna spawnlandý.")
		self.Close()
		self.questionDialog.Close()
########################################################################################################################

########################################################################################################################
	def __OnClickNoticeButton(self):
		self.Close()
		questionDialog = Notice_BigNotice()
		questionDialog.SetText(localeInfo.GAMEMASTER_PANEL_NOTICE)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__OnClickNoticeNormalButton))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnClickNoticeBigButton))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def __OnClickNoticeNormalButton(self):
		self.questionDialog.Close()
		friendNameBoard72 = Notice2()
		friendNameBoard72.SetTitle(localeInfo.GAMEMASTER_PANEL_NOTICE2)
		friendNameBoard72.SetAcceptEvent(ui.__mem_func__(self.Normal))
		friendNameBoard72.SetSendKirmiziEvent(ui.__mem_func__(self.Kirmizi))
		friendNameBoard72.SetSendSariEvent(ui.__mem_func__(self.Sari))
		friendNameBoard72.SetSendMaviEvent(ui.__mem_func__(self.Mavi))
		friendNameBoard72.SetSendPembeEvent(ui.__mem_func__(self.Pembe))
		friendNameBoard72.SetSendMorEvent(ui.__mem_func__(self.Mor))
		friendNameBoard72.SetSendYesilEvent(ui.__mem_func__(self.Yesil))
		friendNameBoard72.SetSendTuruncuEvent(ui.__mem_func__(self.Turuncu))
		friendNameBoard72.SetCancelEvent(ui.__mem_func__(self.NoticeHayir))
		friendNameBoard72.Open()
		self.friendNameBoard72 = friendNameBoard72

	def Normal(self):
		text = self.friendNameBoard72.GetText()
		net.SendChatPacket("/notice " + text)

	def Kirmizi(self):
		text = self.friendNameBoard72.GetText()
		net.SendChatPacket("/notice |cFFFF0000" + text + "|h|r")

	def Sari(self):
		text = self.friendNameBoard72.GetText()
		net.SendChatPacket("/notice |cffffff00" + text + "|h|r")

	def Mavi(self):
		text = self.friendNameBoard72.GetText()
		net.SendChatPacket("/notice |cFF00FFFF" + text + "|h|r")

	def Pembe(self):
		text = self.friendNameBoard72.GetText()
		net.SendChatPacket("/notice |cFFFF00FF" + text + "|h|r")

	def Yesil(self):
		text = self.friendNameBoard72.GetText()
		net.SendChatPacket("/notice |cFF00FF00" + text + "|h|r")

	def Turuncu(self):
		text = self.friendNameBoard72.GetText()
		net.SendChatPacket("/notice |cFFFF8040" + text + "|h|r")

	def Mor(self):
		text = self.friendNameBoard72.GetText()
		net.SendChatPacket("/notice |cFF8000FF" + text + "|h|r")

	def __OnClickNoticeBigButton(self):
		self.questionDialog.Close()
		friendNameBoard723 = Notice3()
		friendNameBoard723.SetTitle(localeInfo.GAMEMASTER_PANEL_NOTICE2)
		friendNameBoard723.SetAcceptEvent(ui.__mem_func__(self.OssnAddFriend55444))
		friendNameBoard723.SetCancelEvent(ui.__mem_func__(self.NoticeHayir2))
		friendNameBoard723.Open()
		self.friendNameBoard723 = friendNameBoard723

	def OssnAddFriend55444(self):
		text = self.friendNameBoard723.GetText()
		net.SendChatPacket("/big_notice " + text)

	def NoticeHayir(self):
		self.friendNameBoard72.Hide()

	def NoticeHayir2(self):
		self.friendNameBoard723.Hide()
########################################################################################################################

########################################################################################################################
	def __OnClickEternalButton(self):
		self.Close()
		if constInfo.eternal == 0:
			constInfo.eternal = 1
			net.SendChatPacket("/cannot_dead")
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ölümsüzlük modu aktif.")
		else:
			constInfo.eternal = 0
			net.SendChatPacket("/can_dead")
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ölümsüzlük modu dezaktif.")
			self.questionDialog.Close()
########################################################################################################################

########################################################################################################################
	def __OnClickLevelUserButton(self):
		self.Close()
		LevelUserBoard = LevelUser()
		LevelUserBoard.SetTitle(localeInfo.GAMEMASTER_PANEL_LEVEL_USER)
		LevelUserBoard.SetAcceptEvent(ui.__mem_func__(self.OnAddLevelUser))
		LevelUserBoard.SetCancelEvent(ui.__mem_func__(self.OnCancelLevelUser))
		LevelUserBoard.Open()
		self.LevelUserBoard = LevelUserBoard

	def OnAddLevelUser(self):
		text = self.LevelUserBoard.GetText()
		net.SendChatPacket("/a " + text)
		chat.AppendChat(chat.CHAT_TYPE_INFO, text + " seviye oldu.")
		self.LevelUserBoard.Hide()

	def OnCancelLevelUser(self):
		self.LevelUserBoard.Hide()
########################################################################################################################

########################################################################################################################
	def __OnClickInvisibleButton(self):
		self.Close()
		net.SendChatPacket("/inv")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Görünmezlik modu aktif/deaktif.")
		self.questionDialog.Close()
########################################################################################################################

########################################################################################################################
	def __OnClickNpcButton(self):
		self.Close()
		NpcBoard = Npc()
		NpcBoard.SetTitle(localeInfo.GAMEMASTER_PANEL_NPC)
		NpcBoard.SetCancelEvent(ui.__mem_func__(self.Close))
		NpcBoard.SetSendSilahciEvent(ui.__mem_func__(self.Silahci))
		NpcBoard.SetSendZirhciEvent(ui.__mem_func__(self.Zirhci))
		NpcBoard.SetSendMarketEvent(ui.__mem_func__(self.Market))
		NpcBoard.SetSendOlayYardimcisiEvent(ui.__mem_func__(self.OlayYardimcisi))
		NpcBoard.SetSendDepocuEvent(ui.__mem_func__(self.Depocu))
		NpcBoard.SetSendYasliKadinEvent(ui.__mem_func__(self.YasliKadin))
		NpcBoard.SetSendBalikciEvent(ui.__mem_func__(self.Balikci))
		NpcBoard.SetSendGenelDepocuHelenEvent(ui.__mem_func__(self.GenelDepocuHelen))
		NpcBoard.SetSendIsinlayiciEvent(ui.__mem_func__(self.Isinlayici))
		NpcBoard.SetSendDemirciEvent(ui.__mem_func__(self.Demirci))
		NpcBoard.SetSendEpicSuraEvent(ui.__mem_func__(self.EpicSura))
		NpcBoard.SetSendKoyGardiyaniEvent(ui.__mem_func__(self.KoyGardiyani))
		NpcBoard.SetSendSavasSorumlusuEvent(ui.__mem_func__(self.SavasSorumlusu))
		NpcBoard.SetSendOgretmenlerEvent(ui.__mem_func__(self.Ogretmenler))
		NpcBoard.SetSendSimyaciEvent(ui.__mem_func__(self.Simyaci))
		NpcBoard.SetSendSoonEvent(ui.__mem_func__(self.Soon))
		NpcBoard.SetSendBiyologEvent(ui.__mem_func__(self.Biyolog))
		NpcBoard.SetSendBaekGoEvent(ui.__mem_func__(self.BaekGo))
		NpcBoard.SetSendUrielEvent(ui.__mem_func__(self.Uriel))
		NpcBoard.SetSendClearEvent(ui.__mem_func__(self.Clear))
		NpcBoard.Open()
		self.NpcBoard = NpcBoard

	def Silahci(self):
		net.SendChatPacket("/mob 9001")

	def Zirhci(self):
		net.SendChatPacket("/mob 9002")

	def Market(self):
		net.SendChatPacket("/mob 9003")

	def OlayYardimcisi(self):
		net.SendChatPacket("/mob 9004")

	def Depocu(self):
		net.SendChatPacket("/mob 9005")

	def YasliKadin(self):
		net.SendChatPacket("/mob 9006")

	def Balikci(self):
		net.SendChatPacket("/mob 9009")

	def GenelDepocuHelen(self):
		net.SendChatPacket("/mob 9010")

	def Isinlayici(self):
		net.SendChatPacket("/mob 9012")

	def Demirci(self):
		net.SendChatPacket("/mob 20016")

	def EpicSura(self):
		net.SendChatPacket("/mob 20091")

	def KoyGardiyani(self):
		net.SendChatPacket("/mob 11000")
		net.SendChatPacket("/mob 11002")
		net.SendChatPacket("/mob 11004")

	def SavasSorumlusu(self):
		net.SendChatPacket("/mob 11001")
		net.SendChatPacket("/mob 11003")
		net.SendChatPacket("/mob 11005")

	def Ogretmenler(self):
		if net.GetEmpireID() == 1:
			net.SendChatPacket("/mob 20300")
			net.SendChatPacket("/mob 20301")
			net.SendChatPacket("/mob 20302")
			net.SendChatPacket("/mob 20303")
			net.SendChatPacket("/mob 20304")
			net.SendChatPacket("/mob 20305")
			net.SendChatPacket("/mob 20306")
			net.SendChatPacket("/mob 20307")
		elif net.GetEmpireID() == 2:
			net.SendChatPacket("/mob 20320")
			net.SendChatPacket("/mob 20321")
			net.SendChatPacket("/mob 20322")
			net.SendChatPacket("/mob 20323")
			net.SendChatPacket("/mob 20324")
			net.SendChatPacket("/mob 20325")
			net.SendChatPacket("/mob 20326")
			net.SendChatPacket("/mob 20327")
		elif net.GetEmpireID() == 3:
			net.SendChatPacket("/mob 20340")
			net.SendChatPacket("/mob 20341")
			net.SendChatPacket("/mob 20342")
			net.SendChatPacket("/mob 20343")
			net.SendChatPacket("/mob 20344")
			net.SendChatPacket("/mob 20345")
			net.SendChatPacket("/mob 20346")
			net.SendChatPacket("/mob 20347")

	def Simyaci(self):
		net.SendChatPacket("/mob 20001")

	def Soon(self):
		net.SendChatPacket("/mob 20023")

	def Biyolog(self):
		net.SendChatPacket("/mob 20084")

	def BaekGo(self):
		net.SendChatPacket("/mob 20018")

	def Uriel(self):
		net.SendChatPacket("/mob 20011")

	def Clear(self):
		net.SendChatPacket("/purge")
########################################################################################################################

########################################################################################################################
	def __OnClickMuteButton(self):
		self.Close()
		MuteBoard = Mute()
		MuteBoard.SetTitle(localeInfo.GAMEMASTER_PANEL_MUTE)
		MuteBoard.SetAcceptEvent(ui.__mem_func__(self.OnAddMute))
		MuteBoard.SetCancelEvent(ui.__mem_func__(self.OnCancelMute))
		MuteBoard.Open()
		self.MuteBoard = MuteBoard

	def OnAddMute(self):
		text = self.MuteBoard.GetText()
		net.SendChatPacket("/block_chat " + text)
		chat.AppendChat(chat.CHAT_TYPE_INFO, text + " saniye boyunca susturuldu.")
		self.MuteBoard.Hide()

	def OnCancelMute(self):
		self.MuteBoard.Hide()
########################################################################################################################

	def __ClickAskButton(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Bu kararýný onaylýyor musun ?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.Yes))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.Hayir))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def Yes(self):
		app.Exit()

	def Hayir(self):
		self.questionDialog.Close()

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)

class Info(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/infoboard.py")

		getObject = self.GetChild
		self.board = getObject("Board")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())	
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

class LevelciMaviRuh(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/maviruhpanel.py")

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

class HeroMan(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/heroman.py")

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

class LevelUser(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/levelveriyorum.py")

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

class Skybox(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/skybox_gm.py")

		self.board = self.GetChild("board")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")
		self.cancel2Button = self.GetChild("cancel2")
		self.cancel3Button = self.GetChild("cancel3")
		self.cancel4Button = self.GetChild("cancel4")

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

	def SAFE_SetCancel2Event(self, event):
		self.cancel2Button.SAFE_SetEvent(event)

	def SAFE_SetCancel3Event(self, event):
		self.cancel3Button.SAFE_SetEvent(event)

	def SAFE_SetCancel4Event(self, event):
		self.cancel4Button.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetCancel2Event(self, event):
		self.cancel2Button.SetEvent(event)

	def SetCancel3Event(self, event):
		self.cancel3Button.SetEvent(event)

	def SetCancel4Event(self, event):
		self.cancel4Button.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def SetCancel2Text(self, text):
		self.cancel2Button.SetText(text)

	def SetCancel3Text(self, text):
		self.cancel3Button.SetText(text)

	def SetCancel4Text(self, text):
		self.cancel4Button.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

class Notice_BigNotice(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/notice_bignotice.py")

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
		return TRUE

class Notice2(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/notice2.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.sendkirmiziButton = getObject("SendKirmiziButton")
		self.sendsariButton = getObject("SendSariButton")
		self.sendmaviButton = getObject("SendMaviButton")
		self.sendyesilButton = getObject("SendYesilButton")
		self.sendturuncuButton = getObject("SendTuruncuButton")
		self.sendmorButton = getObject("SendMorButton")
		self.sendpembeButton = getObject("SendPembeButton")
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
		self.sendkirmiziButton = None
		self.sendmaviButton = None
		self.sendyesilButton = None
		self.sendmorButton = None
		self.sendpembeButton = None
		self.sendturuncuButton = None
		self.sendsariButton = None
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

	def SetSendKirmiziEvent(self, event):
		self.sendkirmiziButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendMaviEvent(self, event):
		self.sendmaviButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendSariEvent(self, event):
		self.sendsariButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendYesilEvent(self, event):
		self.sendyesilButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendTuruncuEvent(self, event):
		self.sendturuncuButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendMorEvent(self, event):
		self.sendmorButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendPembeEvent(self, event):
		self.sendpembeButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class Notice3(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/notice3.py")

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

class Npc(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/npc.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.sendsilahciButton = getObject("SendSilahciButton")
		self.sendzirhciButton = getObject("SendZirhciButton")
		self.sendmarketButton = getObject("SendMarketButton")
		self.sendolayyardimcisiButton = getObject("SendOlayYardimcisiButton")
		self.senddepocuButton = getObject("SendDepocuButton")
		self.sendyaslikadinButton = getObject("SendYasliKadinButton")
		self.sendbalikciButton = getObject("SendBalikciButton")
		self.sendgeneldepocuhelenButton = getObject("SendGenelDepocuHelenButton")
		self.sendisinlayiciButton = getObject("SendIsinlayiciButton")
		self.senddemirciButton = getObject("SendDemirciButton")
		self.sendepicsuraButton = getObject("SendEpicSuraButton")
		self.sendkoygardiyaniButton = getObject("SendKoyGardiyaniButton")
		self.sendsavassorumlusuButton = getObject("SendSavasSorumlusuButton")
		self.sendogretmenlerButton = getObject("SendOgretmenlerButton")
		self.sendsimyaciButton = getObject("SendSimyaciButton")
		self.sendsoonButton = getObject("SendSoonButton")
		self.sendbiyologButton = getObject("SendBiyologButton")
		self.sendbaekgoButton = getObject("SendBaekGoButton")
		self.sendurielButton = getObject("SendUrielButton")
		self.sendclearButton = getObject("SendClearButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.inputSlot.Hide()
		self.inputValue.Hide()
		self.cancelButton.Hide()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.sendsilahciButton = None
		self.sendzirhciButton = None
		self.sendmarketButton = None
		self.sendolayyardimcisiButton = None
		self.senddepocuButton = None
		self.sendyaslikadinButton = None
		self.sendbalikciButton = None
		self.sendgeneldepocuhelenButton = None
		self.sendisinlayiciButton = None
		self.senddemirciButton = None
		self.sendepicsuraButton = None
		self.sendkoygardiyaniButton = None
		self.sendsavassorumlusuButton = None
		self.sendogretmenlerButton = None
		self.sendsimyaciButton = None
		self.sendsoonButton = None
		self.sendbiyologButton = None
		self.sendbaekgoButton = None
		self.sendurielButton = None
		self.sendclearButton = None
		self.inputSlot = None
		self.inputValue = None
		self.cancelButton = None
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

	def SetSendSilahciEvent(self, event):
		self.sendsilahciButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendZirhciEvent(self, event):
		self.sendzirhciButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendMarketEvent(self, event):
		self.sendmarketButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendOlayYardimcisiEvent(self, event):
		self.sendolayyardimcisiButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendDepocuEvent(self, event):
		self.senddepocuButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendYasliKadinEvent(self, event):
		self.sendyaslikadinButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendBalikciEvent(self, event):
		self.sendbalikciButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendGenelDepocuHelenEvent(self, event):
		self.sendgeneldepocuhelenButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendIsinlayiciEvent(self, event):
		self.sendisinlayiciButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendDemirciEvent(self, event):
		self.senddemirciButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendEpicSuraEvent(self, event):
		self.sendepicsuraButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendKoyGardiyaniEvent(self, event):
		self.sendkoygardiyaniButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendSavasSorumlusuEvent(self, event):
		self.sendsavassorumlusuButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendOgretmenlerEvent(self, event):
		self.sendogretmenlerButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendSimyaciEvent(self, event):
		self.sendsimyaciButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendSoonEvent(self, event):
		self.sendsoonButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendBiyologEvent(self, event):
		self.sendbiyologButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendBaekGoEvent(self, event):
		self.sendbaekgoButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendUrielEvent(self, event):
		self.sendurielButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetSendClearEvent(self, event):
		self.sendclearButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class Mute(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/mute.py")

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
