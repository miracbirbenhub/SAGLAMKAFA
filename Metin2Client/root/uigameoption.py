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
import uiPrivateShopBuilder # ±Ë¡ÿ»£
import interfaceModule # ±Ë¡ÿ»£
import background

blockMode = 0
viewChatMode = 0

MOBILE = False

if localeInfo.IsYMIR():
	MOBILE = True


class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()
		self.RefreshViewChat()
		self.RefreshAlwaysShowName()
		self.RefreshShowDamage()
		self.RefreshShowSalesText()
		self.RefreshPremium()
		
		self.RefreshPickitem()
		#self.RefreshPickYang()
		self.RefreshShowLevel()
		self.RefreshTextures()
		self.RefreshRender()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE GAME OPTION DIALOG"

	def __Initialize(self):
		self.titleBar = 0
		self.nameColorModeButtonList = []
		self.viewTargetBoardButtonList = []
		self.pvpModeButtonDict = {}
		self.blockButtonList = []
		self.viewChatButtonList = []
		self.alwaysShowNameButtonList = []
		self.showDamageButtonList = []
		self.YangdropButtonList = []
		self.showsalesTextButtonList = []
		self.MadaraModelShow = []
		self.premium = []
		
		self.autopickitem = []
		#self.autopickyang = []
		self.showLevelButtonList = []
		self.texturesOptionButtonList = []
		self.renderButtonList = []

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
			exception.Abort("OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.nameColorModeButtonList.append(GetObject("name_color_normal"))
			self.nameColorModeButtonList.append(GetObject("name_color_empire"))
			self.viewTargetBoardButtonList.append(GetObject("target_board_no_view"))
			self.viewTargetBoardButtonList.append(GetObject("target_board_view"))
			self.pvpModeButtonDict[player.PK_MODE_PEACE] = GetObject("pvp_peace")
			self.pvpModeButtonDict[player.PK_MODE_REVENGE] = GetObject("pvp_revenge")
			self.pvpModeButtonDict[player.PK_MODE_GUILD] = GetObject("pvp_guild")
			self.pvpModeButtonDict[player.PK_MODE_FREE] = GetObject("pvp_free")
			self.blockButtonList.append(GetObject("block_exchange_button"))
			self.blockButtonList.append(GetObject("block_party_button"))
			self.blockButtonList.append(GetObject("block_guild_button"))
			self.blockButtonList.append(GetObject("block_whisper_button"))
			self.blockButtonList.append(GetObject("block_friend_button"))
			self.blockButtonList.append(GetObject("block_party_request_button"))
			self.viewChatButtonList.append(GetObject("view_chat_on_button"))
			self.viewChatButtonList.append(GetObject("view_chat_off_button"))
			self.alwaysShowNameButtonList.append(GetObject("always_show_name_on_button"))
			self.alwaysShowNameButtonList.append(GetObject("always_show_name_off_button"))
			self.showDamageButtonList.append(GetObject("show_damage_on_button"))
			self.showDamageButtonList.append(GetObject("show_damage_off_button"))
			self.showsalesTextButtonList.append(GetObject("salestext_on_button"))
			self.showsalesTextButtonList.append(GetObject("salestext_off_button"))
			self.MadaraModelShow.append(GetObject("ShowMadaraPetButton"))
			self.MadaraModelShow.append(GetObject("ShowMadaraMountButton"))	
			#yangdrop
			self.YangdropButtonList.append(GetObject("yangdrop_on_button"))
			self.YangdropButtonList.append(GetObject("yangdrop_off_button"))
			#yangdrop
			self.premium.append(GetObject("premium_on"))
			self.premium.append(GetObject("premium_off"))

			self.autopickitem.append(GetObject("auto_pick_item_on"))
			self.autopickitem.append(GetObject("auto_pick_item_off"))
			#self.autopickyang.append(GetObject("auto_pick_yang_on"))
			#self.autopickyang.append(GetObject("auto_pick_yang_off"))
			self.showLevelButtonList.append(GetObject("showlevel_on_button"))
			self.showLevelButtonList.append(GetObject("showlevel_off_button"))
			self.texturesOptionButtonList.append(GetObject("texture_classic"))
			self.texturesOptionButtonList.append(GetObject("texture_snow"))
			self.texturesOptionButtonList.append(GetObject("texture_desert"))
			self.texturesOptionButtonList.append(GetObject("texture_green"))

			self.renderButtonList.append(GetObject("render_on"))
			self.renderButtonList.append(GetObject("render_off"))

			global MOBILE
			if MOBILE:
				self.inputMobileButton = GetObject("input_mobile_button")
				self.deleteMobileButton = GetObject("delete_mobile_button")


		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		global MOBILE
		if MOBILE:
			self.__Load_LoadScript("uiscript/gameoptiondialog_formobile.py")
		else:
			self.__Load_LoadScript("uiscript/gameoptiondialog.py")

		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.nameColorModeButtonList[0].SAFE_SetEvent(self.__OnClickNameColorModeNormalButton)
		self.nameColorModeButtonList[1].SAFE_SetEvent(self.__OnClickNameColorModeEmpireButton)

		self.premium[0].SAFE_SetEvent(self._premium_on)
		self.premium[1].SAFE_SetEvent(self._premium_off)

		self.viewTargetBoardButtonList[0].SAFE_SetEvent(self.__OnClickTargetBoardViewButton)
		self.viewTargetBoardButtonList[1].SAFE_SetEvent(self.__OnClickTargetBoardNoViewButton)

		self.pvpModeButtonDict[player.PK_MODE_PEACE].SAFE_SetEvent(self.__OnClickPvPModePeaceButton)
		self.pvpModeButtonDict[player.PK_MODE_REVENGE].SAFE_SetEvent(self.__OnClickPvPModeRevengeButton)
		self.pvpModeButtonDict[player.PK_MODE_GUILD].SAFE_SetEvent(self.__OnClickPvPModeGuildButton)
		self.pvpModeButtonDict[player.PK_MODE_FREE].SAFE_SetEvent(self.__OnClickPvPModeFreeButton)

		self.blockButtonList[0].SetToggleUpEvent(self.__OnClickBlockExchangeButton)
		self.blockButtonList[1].SetToggleUpEvent(self.__OnClickBlockPartyButton)
		self.blockButtonList[2].SetToggleUpEvent(self.__OnClickBlockGuildButton)
		self.blockButtonList[3].SetToggleUpEvent(self.__OnClickBlockWhisperButton)
		self.blockButtonList[4].SetToggleUpEvent(self.__OnClickBlockFriendButton)
		self.blockButtonList[5].SetToggleUpEvent(self.__OnClickBlockPartyRequest)

		self.blockButtonList[0].SetToggleDownEvent(self.__OnClickBlockExchangeButton)
		self.blockButtonList[1].SetToggleDownEvent(self.__OnClickBlockPartyButton)
		self.blockButtonList[2].SetToggleDownEvent(self.__OnClickBlockGuildButton)
		self.blockButtonList[3].SetToggleDownEvent(self.__OnClickBlockWhisperButton)
		self.blockButtonList[4].SetToggleDownEvent(self.__OnClickBlockFriendButton)
		self.blockButtonList[5].SetToggleDownEvent(self.__OnClickBlockPartyRequest)

		self.viewChatButtonList[0].SAFE_SetEvent(self.__OnClickViewChatOnButton)
		self.viewChatButtonList[1].SAFE_SetEvent(self.__OnClickViewChatOffButton)

		self.alwaysShowNameButtonList[0].SAFE_SetEvent(self.__OnClickAlwaysShowNameOnButton)
		self.alwaysShowNameButtonList[1].SAFE_SetEvent(self.__OnClickAlwaysShowNameOffButton)

		self.showDamageButtonList[0].SAFE_SetEvent(self.__OnClickShowDamageOnButton)
		self.showDamageButtonList[1].SAFE_SetEvent(self.__OnClickShowDamageOffButton)
		
		self.showsalesTextButtonList[0].SAFE_SetEvent(self.__OnClickSalesTextOnButton)
		self.showsalesTextButtonList[1].SAFE_SetEvent(self.__OnClickSalesTextOffButton)
		self.MadaraModelShow[0].SetToggleUpEvent(self.__OnClickHidePetsButton)
		self.MadaraModelShow[0].SetToggleDownEvent(self.__OnClickHidePetsButton)
		self.MadaraModelShow[1].SetToggleUpEvent(self.__OnClickHideMountsButton)
		self.MadaraModelShow[1].SetToggleDownEvent(self.__OnClickHideMountsButton)	

		self.YangdropButtonList[0].SAFE_SetEvent(self.__OnClickEnableYangdrop)
		self.YangdropButtonList[1].SAFE_SetEvent(self.__OnClickDisableYangdrop)		

		self.autopickitem[0].SAFE_SetEvent(self.__OnClickPickitemOnButton)
		self.autopickitem[1].SAFE_SetEvent(self.__OnClickPickitemOffButton)
		#self.autopickyang[0].SAFE_SetEvent(self.__OnClickPickYangOnButton)
		#self.autopickyang[1].SAFE_SetEvent(self.__OnClickPickYangOffButton)
		
		self.texturesOptionButtonList[0].SAFE_SetEvent(self.__OnClickChangeTextureClassic)
		self.texturesOptionButtonList[1].SAFE_SetEvent(self.__OnClickChangeTextureSnow)
		self.texturesOptionButtonList[2].SAFE_SetEvent(self.__OnClickChangeTextureDesert)
		self.texturesOptionButtonList[3].SAFE_SetEvent(self.__OnClickChangeTextureGreen)
		
		self.showLevelButtonList[0].SAFE_SetEvent(self.__OnClickShowLevelOnButton)
		self.showLevelButtonList[1].SAFE_SetEvent(self.__OnClickShowLevelOffButton)

		self.renderButtonList[0].SAFE_SetEvent(self.__RenderOpen)
		self.renderButtonList[1].SAFE_SetEvent(self.__RenderOff)

		self.__ClickRadioButton(self.nameColorModeButtonList, constInfo.GET_CHRNAME_COLOR_INDEX())
		self.__ClickRadioButton(self.viewTargetBoardButtonList, constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD())
		self.__SetPeacePKMode()

		#global MOBILE
		if MOBILE:
			self.inputMobileButton.SetEvent(ui.__mem_func__(self.__OnChangeMobilePhoneNumber))
			self.deleteMobileButton.SetEvent(ui.__mem_func__(self.__OnDeleteMobilePhoneNumber))

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()

	def UpdateMadaraModel(self):
		if systemSetting.IsHidePets():
			self.MadaraModelShow[0].Down()
		else:
			self.MadaraModelShow[0].SetUp()

		if systemSetting.IsHideMounts():
			self.MadaraModelShow[1].Down()
		else:
			self.MadaraModelShow[1].SetUp()	
			
	def __OnClickHidePetsButton(self):
		systemSetting.SetHidePets(not systemSetting.IsHidePets())
		self.UpdateMadaraModel()

	def __OnClickHideMountsButton(self):
		systemSetting.SetHideMounts(not systemSetting.IsHideMounts())
		self.UpdateMadaraModel()	
		

	def __SetNameColorMode(self, index):
		constInfo.SET_CHRNAME_COLOR_INDEX(index)
		self.__ClickRadioButton(self.nameColorModeButtonList, index)

	def __SetTargetBoardViewMode(self, flag):
		constInfo.SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(flag)
		self.__ClickRadioButton(self.viewTargetBoardButtonList, flag)

	def __OnClickNameColorModeNormalButton(self):
		self.__SetNameColorMode(0)

	def __OnClickNameColorModeEmpireButton(self):
		self.__SetNameColorMode(1)

	def __OnClickTargetBoardViewButton(self):
		self.__SetTargetBoardViewMode(0)

	def __OnClickTargetBoardNoViewButton(self):
		self.__SetTargetBoardViewMode(1)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)

	def __OnClickBlockExchangeButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_EXCHANGE))
	def __OnClickBlockPartyButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY))
	def __OnClickBlockGuildButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_GUILD))
	def __OnClickBlockWhisperButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_WHISPER))
	def __OnClickBlockFriendButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_FRIEND))
	def __OnClickBlockPartyRequest(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY_REQUEST))

	def __OnClickViewChatOnButton(self):
		global viewChatMode
		viewChatMode = 1
		systemSetting.SetViewChatFlag(viewChatMode)
		self.RefreshViewChat()
	def __OnClickViewChatOffButton(self):
		global viewChatMode
		viewChatMode = 0
		systemSetting.SetViewChatFlag(viewChatMode)
		self.RefreshViewChat()

	def __OnClickAlwaysShowNameOnButton(self):
		systemSetting.SetAlwaysShowNameFlag(True)
		self.RefreshAlwaysShowName()

	def __OnClickAlwaysShowNameOffButton(self):
		systemSetting.SetAlwaysShowNameFlag(False)
		self.RefreshAlwaysShowName()

	def __OnClickShowDamageOnButton(self):
		systemSetting.SetShowDamageFlag(True)
		self.RefreshShowDamage()

	def __OnClickShowDamageOffButton(self):
		systemSetting.SetShowDamageFlag(False)
		self.RefreshShowDamage()
		
	def __OnClickSalesTextOnButton(self):
		systemSetting.SetShowSalesTextFlag(True)
		self.RefreshShowSalesText()
		uiPrivateShopBuilder.UpdateADBoard()
		
	def __OnClickSalesTextOffButton(self):
		systemSetting.SetShowSalesTextFlag(False)
		self.RefreshShowSalesText()

	#Yangdrop	
	def __OnClickSalesTextOffButton(self):
		systemSetting.SetShowSalesTextFlag(FALSE)
		self.RefreshShowSalesText()		
		
	def __OnClickEnableYangdrop(self):
		self.YangdropButtonList[0].Down()
		self.YangdropButtonList[1].SetUp()

		constInfo.YangDrop = 1
		chat.AppendChat(chat.CHAT_TYPE_INFO, "|cffFFC125Yang Drop Bilgisi Gosterme Aktif.")

	def __OnClickDisableYangdrop(self):
		self.YangdropButtonList[0].SetUp()
		self.YangdropButtonList[1].Down()

		constInfo.YangDrop = 0
		chat.AppendChat(chat.CHAT_TYPE_INFO, "|cffFFC125Yang Drop Gosterme Deaktif.")
	#Yangdrop		
		
	def __OnClickPickitemOnButton(self):
		constInfo.auto_pick_item = 0
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Otomatik yang ve item toplama sistemi aktive edildi.")
		self.RefreshPickitem()
		
	def __OnClickPickitemOffButton(self):
		constInfo.auto_pick_item = 1
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Otomatik yang ve item toplama sistemi deaktif edildi.")
		self.RefreshPickitem()

	def RefreshPickitem(self):
		if constInfo.auto_pick_item == 0:
			self.autopickitem[0].Down()
			self.autopickitem[1].SetUp()
		else:
			self.autopickitem[0].SetUp()
			self.autopickitem[1].Down()

	def __OnClickPickYangOnButton(self):
		constInfo.auto_pick_yang = 0
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Otomatik sadece yang toplama sistemi aktive edildi.")
		self.RefreshPickYang()
		
	def __OnClickPickYangOffButton(self):
		constInfo.auto_pick_yang = 1
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Otomatik sadece yang toplama sistemi deaktif edildi.")
		self.RefreshPickYang()

	def RefreshPickYang(self):
		if constInfo.auto_pick_yang == 0:
			self.autopickyang[0].Down()
			self.autopickyang[1].SetUp()
		else:
			self.autopickyang[0].SetUp()
			self.autopickyang[1].Down()

	def __RenderOpen(self):
		systemSetting.SetRenderHide(1)
		
		self.RefreshRender()	

	def __RenderOff(self):
		systemSetting.SetRenderHide(0)
		
		self.RefreshRender()	
		
	def RefreshRender(self):
		if systemSetting.IsRenderHide() == 1:
			self.renderButtonList[0].Down()
			self.renderButtonList[1].SetUp()
		else:
			self.renderButtonList[0].SetUp()
			self.renderButtonList[1].Down()

	def __OnClickShowLevelOnButton(self):
		systemSetting.SetShowLevelFlag(True)
		self.RefreshShowLevel()

	def __OnClickShowLevelOffButton(self):
		systemSetting.SetShowLevelFlag(False)
		self.RefreshShowLevel()

	def RefreshShowLevel(self):
		if systemSetting.IsShowLevel():
			self.showLevelButtonList[0].Down()
			self.showLevelButtonList[1].SetUp()
		else:
			self.showLevelButtonList[0].SetUp()
			self.showLevelButtonList[1].Down()
		
	def __OnClickChangeTextureClassic(self):
		systemSetting.SetSnowTexturesMode(False)
		systemSetting.SetDesertTexturesMode(False)
		systemSetting.SetGreenTexturesMode(False)
		self.RefreshTextures()
		if background.GetCurrentMapName():
			classic_maps = [
				"metin2_map_a1",
				"metin2_map_b1",
				"metin2_map_c1"
			]
			classic_map_textures = {
				"metin2_map_a1" : "textureset\metin2_A1.txt",
				"metin2_map_b1" : "textureset\metin2_B1.txt",
				"metin2_map_c1" : "textureset\metin2_C1.txt", }
			if str(background.GetCurrentMapName()) in classic_maps:
				background.TextureChange(classic_map_textures[str(background.GetCurrentMapName())])

	def __OnClickChangeTextureSnow(self):
		systemSetting.SetSnowTexturesMode(True)
		systemSetting.SetDesertTexturesMode(False)
		systemSetting.SetGreenTexturesMode(False)
		self.RefreshTextures()
		if background.GetCurrentMapName():
			snow_maps = [
				"metin2_map_a1",
				"metin2_map_b1",
				"metin2_map_c1"
			]
			snow_maps_textures = {
				"metin2_map_a1" : "textureset\metin2_a1_snown.txt",
				"metin2_map_b1" : "textureset\metin2_b1_snown.txt",
				"metin2_map_c1" : "textureset\metin2_c1_snown.txt", }
			if str(background.GetCurrentMapName()) in snow_maps:
				background.TextureChange(snow_maps_textures[str(background.GetCurrentMapName())])

	def __OnClickChangeTextureDesert(self):
		systemSetting.SetSnowTexturesMode(False)
		systemSetting.SetDesertTexturesMode(True)
		systemSetting.SetGreenTexturesMode(False)
		self.RefreshTextures()
		if background.GetCurrentMapName():
			desert_maps = [
				"metin2_map_a1",
				"metin2_map_b1",
				"metin2_map_c1"
			]
			desert_maps_textures = {
				"metin2_map_a1" : "textureset\metin2_a1_desert.txt",
				"metin2_map_b1" : "textureset\metin2_b1_desert.txt",
				"metin2_map_c1" : "textureset\metin2_c1_desert.txt", }
			if str(background.GetCurrentMapName()) in desert_maps:
				background.TextureChange(desert_maps_textures[str(background.GetCurrentMapName())])		

	def __OnClickChangeTextureGreen(self):
		systemSetting.SetSnowTexturesMode(False)
		systemSetting.SetDesertTexturesMode(False)
		systemSetting.SetGreenTexturesMode(True)
		self.RefreshTextures()
		if background.GetCurrentMapName():
			green_maps = [
				"metin2_map_a1",
				"metin2_map_b1",
				"metin2_map_c1"
			]
			green_maps_textures = {
				"metin2_map_a1" : "textureset\metin2_a1_old.txt",
				"metin2_map_b1" : "textureset\metin2_b1_old.txt",
				"metin2_map_c1" : "textureset\metin2_c1_old.txt", }
			if str(background.GetCurrentMapName()) in green_maps:
				background.TextureChange(green_maps_textures[str(background.GetCurrentMapName())])		


	def RefreshTextures(self):
		if systemSetting.IsSnowTexturesMode():
			self.texturesOptionButtonList[0].SetUp()
			self.texturesOptionButtonList[1].Down()
			self.texturesOptionButtonList[2].SetUp()
			self.texturesOptionButtonList[3].SetUp()
		elif systemSetting.IsDesertTexturesMode():
			self.texturesOptionButtonList[0].SetUp()
			self.texturesOptionButtonList[1].SetUp()
			self.texturesOptionButtonList[2].Down()
			self.texturesOptionButtonList[3].SetUp()
		elif systemSetting.IsGreenTexturesMode():
			self.texturesOptionButtonList[0].SetUp()
			self.texturesOptionButtonList[1].SetUp()
			self.texturesOptionButtonList[2].SetUp()
			self.texturesOptionButtonList[3].Down()
		else:
			self.texturesOptionButtonList[0].Down()
			self.texturesOptionButtonList[1].SetUp()
			self.texturesOptionButtonList[2].SetUp()
			self.texturesOptionButtonList[3].SetUp()
		
	def __CheckPvPProtectedLevelPlayer(self):	
		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__SetPeacePKMode()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return 1

		return 0

	def __SetPKMode(self, mode):
		for btn in self.pvpModeButtonDict.values():
			btn.SetUp()
		if self.pvpModeButtonDict.has_key(mode):
			self.pvpModeButtonDict[mode].Down()

	def __SetPeacePKMode(self):
		self.__SetPKMode(player.PK_MODE_PEACE)

	def __RefreshPVPButtonList(self):
		self.__SetPKMode(player.GetPKMode())

	def __OnClickPvPModePeaceButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 0", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeRevengeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 1", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeFreeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 2", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeGuildButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if 0 == player.GetGuildID():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
			return

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 4", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def OnChangePKMode(self):
		self.__RefreshPVPButtonList()

	def __OnChangeMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.MESSENGER_INPUT_MOBILE_PHONE_NUMBER_TITLE)
		inputDialog.SetMaxLength(13)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OnInputMobilePhoneNumber))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseInputDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def __OnDeleteMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE_PHONE_NUMBER)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDeleteMobile))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def OnInputMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		text = self.inputDialog.GetText()

		if not text:
			return

		text.replace('-', '')
		net.SendChatPacket("/mobile " + text)
		self.OnCloseInputDialog()
		return True

	def OnInputMobileAuthorityCode(self):
		global MOBILE
		if not MOBILE:
			return

		text = self.inputDialog.GetText()
		net.SendChatPacket("/mobile_auth " + text)
		self.OnCloseInputDialog()
		return True

	def OnDeleteMobile(self):
		global MOBILE
		if not MOBILE:
			return

		net.SendChatPacket("/mobile")
		self.OnCloseQuestionDialog()
		return True

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

	def RefreshMobile(self):
		global MOBILE
		if not MOBILE:
			return

		if player.HasMobilePhoneNumber():
			self.inputMobileButton.Hide()
			self.deleteMobileButton.Show()
		else:
			self.inputMobileButton.Show()
			self.deleteMobileButton.Hide()

	def OnMobileAuthority(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		inputDialog = uiCommon.InputDialogWithDescription()
		inputDialog.SetTitle(localeInfo.MESSENGER_INPUT_MOBILE_AUTHORITY_TITLE)
		inputDialog.SetDescription(localeInfo.MESSENGER_INPUT_MOBILE_AUTHORITY_DESCRIPTION)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OnInputMobileAuthorityCode))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseInputDialog))
		inputDialog.SetMaxLength(4)
		inputDialog.SetBoardWidth(310)
		inputDialog.Open()
		self.inputDialog = inputDialog

	def RefreshBlock(self):
		global blockMode
		for i in xrange(len(self.blockButtonList)):
			if 0 != (blockMode & (1 << i)):
				self.blockButtonList[i].Down()
			else:
				self.blockButtonList[i].SetUp()

	def RefreshViewChat(self):
		if systemSetting.IsViewChat():
			self.viewChatButtonList[0].Down()
			self.viewChatButtonList[1].SetUp()
		else:
			self.viewChatButtonList[0].SetUp()
			self.viewChatButtonList[1].Down()

	def RefreshAlwaysShowName(self):
		if systemSetting.IsAlwaysShowName():
			self.alwaysShowNameButtonList[0].Down()
			self.alwaysShowNameButtonList[1].SetUp()
		else:
			self.alwaysShowNameButtonList[0].SetUp()
			self.alwaysShowNameButtonList[1].Down()

	def RefreshShowDamage(self):
		if systemSetting.IsShowDamage():
			self.showDamageButtonList[0].Down()
			self.showDamageButtonList[1].SetUp()
		else:
			self.showDamageButtonList[0].SetUp()
			self.showDamageButtonList[1].Down()
			
	def RefreshShowSalesText(self):
		if systemSetting.IsShowSalesText():
			self.showsalesTextButtonList[0].Down()
			self.showsalesTextButtonList[1].SetUp()
		else:
			self.showsalesTextButtonList[0].SetUp()
			self.showsalesTextButtonList[1].Down()

	def OnBlockMode(self, mode):
		global blockMode
		blockMode = mode
		self.RefreshBlock()

	def Show(self):
		self.RefreshMobile()
		self.RefreshBlock()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def _premium_on(self):
		constInfo.premium = 1
		constInfo.premiumgoster = 1
		self.RefreshPremium()
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Premium iconlar aÁ˝ld˝.")

	def _premium_off(self):
		constInfo.premium = 1
		constInfo.premiumgoster = 0
		self.RefreshPremium()
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Premium iconlar kapat˝ld˝.")

	def RefreshPremium(self):
		if constInfo.premiumgoster == 1:
			self.premium[0].Down()
			self.premium[1].SetUp()
		else:
			self.premium[0].SetUp()
			self.premium[1].Down()
