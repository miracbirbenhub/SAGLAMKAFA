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
import musicInfo

import uiSelectMusic
import background
import os
import app

MUSIC_FILENAME_MAX_LEN = 25

blockMode = 0

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()
		if app.ENABLE_FOV_OPTION:
			self.RefreshFOVOption()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE SYSTEM OPTION DIALOG"

	def __Initialize(self):
		self.tilingMode = 0
		self.titleBar = 0
		self.changeMusicButton = 0
		self.selectMusicFile = 0
		self.ctrlMusicVolume = 0
		self.ctrlSoundVolume = 0
		self.musicListDlg = 0
		self.tilingApplyButton = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.nightModeOptionButtonList = []
		self.ctrlShadowQuality = 0
		self.fonttypeButtonList = []
		if app.ENABLE_FOV_OPTION:
			self.fovButtonList = []
		self.ctrlShopNamesRange = 0
		
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
			self.selectMusicFile = GetObject("bgm_file")
			self.changeMusicButton = GetObject("bgm_button")
			self.ctrlMusicVolume = GetObject("music_volume_controller")
			self.ctrlSoundVolume = GetObject("sound_volume_controller")			
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))
			self.fogModeButtonList.append(GetObject("fog_level0"))
			self.fogModeButtonList.append(GetObject("fog_level1"))
			self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			self.tilingApplyButton=GetObject("tiling_apply")
			self.nightModeOptionButtonList.append(GetObject("night_on"))
			self.nightModeOptionButtonList.append(GetObject("night_off"))
			self.fonttypeButtonList.append(GetObject("font_type_arial"))
			self.fonttypeButtonList.append(GetObject("font_type_tahoma"))
			self.fonttypeButtonList.append(GetObject("font_type_geneva"))
			if app.ENABLE_FOV_OPTION:
				self.fovButtonList.append(GetObject("fov_on"))
				self.fovButtonList.append(GetObject("fov_off"))
			#self.ctrlShadowQuality = GetObject("shadow_bar")
			self.ctrlShopNamesRange = GetObject("salestext_range_controller")
		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/systemoptiondialog.py")
		self.__Load_BindObject()

		self.SetCenterPosition()
		
		self.popupDialog = PopupDialog(self)
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))

		self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
		self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))

#		self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
#		self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

		self.changeMusicButton.SAFE_SetEvent(self.__OnClickChangeMusicButton)

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
		self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
		self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)

		self.nightModeOptionButtonList[0].SAFE_SetEvent(self.__OnClickNightModeOptionEnableButton)
		self.nightModeOptionButtonList[1].SAFE_SetEvent(self.__OnClickNightModeOptionDisableButton)

		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)

		self.fonttypeButtonList[0].SAFE_SetEvent(self.__OnClickArialButton)
		self.fonttypeButtonList[1].SAFE_SetEvent(self.__OnClickTahomaButton)
		self.fonttypeButtonList[2].SAFE_SetEvent(self.__OnClickGenevaButton)
		
		if app.ENABLE_FOV_OPTION:
			self.__ClickRadioButton(self.fovButtonList, systemSetting.IsExtendedFOV())

		self.__SetCurTilingMode()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())
		
		if app.ENABLE_FOV_OPTION:
			self.fovButtonList[0].SAFE_SetEvent(self.__OnClickFOVButton, 1) # on
			self.fovButtonList[1].SAFE_SetEvent(self.__OnClickFOVButton, 0) # off

		if os.path.exists("gameoption.cfg"):
			fd = open( "gameoption.cfg" , "r")
			fonttype = fd.readline()
			fd.close()
			if fonttype == "0":
				self.__ClickRadioButton(self.fonttypeButtonList, 0)
			elif fonttype == "1":
				self.__ClickRadioButton(self.fonttypeButtonList, 1)
			elif fonttype == "2":
				self.__ClickRadioButton(self.fonttypeButtonList, 2)
		else:
			self.__ClickRadioButton(self.fonttypeButtonList, 0)
			
		if app.ENABLE_SHOPNAMES_RANGE:
			self.ctrlShopNamesRange.SetSliderPos(float(systemSetting.GetShopNamesRange()))
			self.ctrlShopNamesRange.SetEvent(ui.__mem_func__(self.OnChangeShopNamesRange))

		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

	def __OnClickArialButton(self):
		if os.path.exists("gameoption.cfg"):
			os.remove("gameoption.cfg")
		f = open( "gameoption.cfg", "w")
		f.write("0")
		f.close()
		self.popupDialog.Open(localeInfo.LANG_RESTART_FOR_CHANGE)
		self.__ClickRadioButton(self.fonttypeButtonList, 0)
		
	def __OnClickTahomaButton(self):
		if os.path.exists("gameoption.cfg"):
			os.remove("gameoption.cfg")
		f = open( "gameoption.cfg", "w")
		f.write("1")
		f.close()
		self.popupDialog.Open(localeInfo.LANG_RESTART_FOR_CHANGE)
		self.__ClickRadioButton(self.fonttypeButtonList, 1)
		
	def __OnClickGenevaButton(self):
		if os.path.exists("gameoption.cfg"):
			os.remove("gameoption.cfg")
		f = open( "gameoption.cfg", "w")
		f.write("2")
		f.close()
		self.popupDialog.Open(localeInfo.LANG_RESTART_FOR_CHANGE)
		self.__ClickRadioButton(self.fonttypeButtonList, 2)

	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		net.ExitGame()

	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:
			
			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()

		
	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()


	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

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

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()
		
		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	if app.ENABLE_FOV_OPTION:
		def __OnClickFOVButton(self, flag):
			self.__ClickRadioButton(self.fovButtonList, flag)
			systemSetting.SetExtendedFOV(flag)
			self.RefreshFOVOption()

		def RefreshFOVOption(self):
			if systemSetting.IsExtendedFOV():
				self.fovButtonList[1].SetUp()
				self.fovButtonList[0].Down()
			else:
				self.fovButtonList[1].Down()
				self.fovButtonList[0].SetUp()

	if app.ENABLE_SHOPNAMES_RANGE:
		def OnChangeShopNamesRange(self):
			pos = self.ctrlShopNamesRange.GetSliderPos()
			systemSetting.SetShopNamesRange(pos)
			if systemSetting.IsShowSalesText():
				uiPrivateShopBuilder.UpdateADBoard()

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * net.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	def OnChangeShadowQuality(self):
		pos = self.ctrlShadowQuality.GetSliderPos()
		systemSetting.SetShadowLevel(int(pos / 0.2))

	def __OnClickNightModeOptionEnableButton(self):
		systemSetting.SetNightMode(True)
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.RefreshNightOption()
		
	def __OnClickNightModeOptionDisableButton(self):
		systemSetting.SetNightMode(False)
		background.SetEnvironmentData(0)
		self.RefreshNightOption()
		
	def RefreshNightOption(self):
		if systemSetting.GetNightMode():
			self.nightModeOptionButtonList[0].Down()
			self.nightModeOptionButtonList[1].SetUp()
		else:
			self.nightModeOptionButtonList[0].SetUp()
			self.nightModeOptionButtonList[1].Down()

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
		self.__SetCurTilingMode()
		self.Hide()

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)	

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)
		
class PopupDialog(ui.ScriptWindow):
	def __init__(self, parent):
		print "PopupDialog::PopupDialog()"
		ui.ScriptWindow.__init__(self)

		self.__Load()
		self.__Bind()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print "PopupDialog::~PopupDialog()"

	def __Load(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")
		except:
			import exception
			exception.Abort("PopupDialog.__Load")

	def __Bind(self):
		try:
			self.textLine=self.GetChild("message")
			self.okButton=self.GetChild("accept")
		except:
			import exception
			exception.Abort("PopupDialog.__Bind")

		self.okButton.SAFE_SetEvent(self.__OnOK)

	def Open(self, msg):
		self.textLine.SetText(msg)
		self.SetCenterPosition()
		self.Show()
		self.SetTop()

	def __OnOK(self):
		self.Hide()
