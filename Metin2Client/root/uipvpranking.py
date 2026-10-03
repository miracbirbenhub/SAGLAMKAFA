import ui, dbg, constInfo, player, app, net, chat
import event, chat, localeInfo, wndMgr, playerSettingModule

X_START = 30
Y_START = 40
Y_PASS = 25
WIDTH = 325
HEIGHT = 250

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "pvprank/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "pvprank/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "pvprank/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "pvprank/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "pvprank/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "pvprank/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "pvprank/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "pvprank/shaman_w.tga"
}

if app.ENABLE_PVP_RANKING_WITH_EMPIRE:
	EMPIRE_IMAGE_DICT = {
		1	: "pvprank/empire_shinsu.png",
		2	: "pvprank/empire_chunjo.png",
		3	: "pvprank/empire_jinno.png"
	}

class RankingWindow(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.Clear()
	def __del__(self):
		ui.Window.__del__(self)
		# self.Clear()
	def Destroy(self):
		# self.ClearDictionary()
		self.Clear()
	def Clear(self):
		self.children = []
		pass
	def ClearPlayerInfo(self):
		self.playerCount = 0
		self.playerNames = []
		self.playerRaces = []
		self.playerLevels = []
		self.playerEmpires = []
		self.playerKills = []
		self.playerDeads = []
		self.maxKill = 0
		self.empire1 = 0
		self.empire2 = 0
		self.empire3 = 0
		self.IsRankEmpire = 0
		
	if app.ENABLE_PVP_RANKING_WITH_EMPIRE:
		def AddPlayerInfo(self, chName, chLevel, chRace, chEmpire, chKill, chDead, maxKill, IsRankEmpire, empire1, empire2, empire3):
			self.playerNames.append(chName)
			self.playerRaces.append(chRace)
			self.playerLevels.append(chLevel)
			self.playerEmpires.append(chEmpire)
			self.playerKills.append(chKill)
			self.playerDeads.append(chDead)
			self.playerCount += 1
			self.maxKill = maxKill
			self.empire1 = empire1
			self.empire2 = empire2
			self.empire3 = empire3
			self.IsRankEmpire = IsRankEmpire
	else:
		def AddPlayerInfo(self, chName, chLevel, chRace, chEmpire, chKill, chDead, maxKill):
			self.playerNames.append(chName)
			self.playerRaces.append(chRace)
			self.playerLevels.append(chLevel)
			self.playerEmpires.append(chEmpire)
			self.playerKills.append(chKill)
			self.playerDeads.append(chDead)
			self.playerCount += 1
			self.maxKill = maxKill
			
	def RefreshWindow(self):
		self.Clear()
		self.AddFlag('movable')
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.AddFlag('not_pick')
		thinBoard.Show()
		
		self.img = ui.ImageBox()
		self.img.LoadImage("pvprank/seperator.tga")
		self.img.SetParent(self)
		self.img.SetPosition(60, -1)
		self.img.Show()
		
		self.infotext = ui.TextLine()
		self.infotext.SetParent(self)
		self.infotext.SetPosition(0, 5)
		self.infotext.SetText("Ýlk 10 sýralama ")
		self.infotext.SetPackedFontColor(0xFFFEE3AE)
		self.infotext.SetWindowHorizontalAlignCenter()
		self.infotext.SetHorizontalAlignCenter()
		self.infotext.Show()
		
		if app.ENABLE_PVP_RANKING_WITH_EMPIRE and self.IsRankEmpire == 1:
			thinBoardEmpire = ui.ThinBoard()
			thinBoardEmpire.SetPosition(7, -125)
			thinBoardEmpire.SetParent(self)
			thinBoardEmpire.AddFlag('not_pick')
			thinBoardEmpire.Show()
			
			self.imgEmpire = ui.ImageBox()
			self.imgEmpire.LoadImage("pvprank/seperator.tga")
			self.imgEmpire.SetParent(thinBoardEmpire)
			self.imgEmpire.SetPosition(60, -1)
			self.imgEmpire.Show()
			
			self.infotextEmpire = ui.TextLine()
			self.infotextEmpire.SetParent(thinBoardEmpire)
			self.infotextEmpire.SetPosition(0, 5)
			self.infotextEmpire.SetText("Krallýk Puanlarý ")
			self.infotextEmpire.SetPackedFontColor(0xFFFEE3AE)
			self.infotextEmpire.SetWindowHorizontalAlignCenter()
			self.infotextEmpire.SetHorizontalAlignCenter()
			self.infotextEmpire.Show()
			
			imageStrEmpire1 = EMPIRE_IMAGE_DICT[1]
			imageStrEmpire2 = EMPIRE_IMAGE_DICT[2]
			imageStrEmpire3 = EMPIRE_IMAGE_DICT[3]
			emEmpireStr1 = "Kýrmýzý Bayrak  %d"  % self.empire1
			emEmpireStr2 = "Sarý Bayrak %d"  % self.empire2
			emEmpireStr3 = "Mavi Bayrak %d"  % self.empire3
			flag1 = ui.MakeImageBox(thinBoardEmpire, imageStrEmpire1, X_START - 3, Y_PASS+Y_START - 25)
			flag2 = ui.MakeImageBox(thinBoardEmpire, imageStrEmpire2, X_START - 3, (Y_PASS*2)+Y_START  - 25)
			flag3 = ui.MakeImageBox(thinBoardEmpire, imageStrEmpire3, X_START - 3, (Y_PASS*3)+Y_START - 25)
			txEmpireName1 = ui.MakeTextLineNew(thinBoardEmpire, X_START + 35, Y_PASS+Y_START - 25, emEmpireStr1,)
			txEmpireName2 = ui.MakeTextLineNew(thinBoardEmpire, X_START + 35, (Y_PASS*2)+Y_START - 25, emEmpireStr2,)
			txEmpireName3 = ui.MakeTextLineNew(thinBoardEmpire, X_START + 35, (Y_PASS*3)+Y_START - 25, emEmpireStr3,)
			
			self.children.append(flag1)
			self.children.append(flag2)
			self.children.append(flag3)
			self.children.append(txEmpireName1)
			self.children.append(txEmpireName2)
			self.children.append(txEmpireName3)

		
		yPos = 0
		for i in xrange(self.playerCount):
			yPos = (Y_PASS * i) + Y_START
			imageStr = FACE_IMAGE_DICT[self.playerRaces[i]]
			nameStr = "%s [Lv.%d]  %d / %d"  % (self.playerNames[i], self.playerLevels[i], self.playerKills[i], self.playerDeads[i])
			raceImage = ui.MakeImageBox(thinBoard, imageStr, X_START - 3, yPos - 6)
			txName = ui.MakeTextLineNew(thinBoard, X_START + 25, yPos - 4, nameStr,)
			#txName.SetPackedFontColor(self.GetColorAsEmpireIndex(self.playerEmpires[i]))
			hpGauge = ui.Gauge()
			hpGauge.SetParent(thinBoard)
			hpGauge.MakeGauge(117, "red")
			hpGauge.SetPosition(200, yPos)
			hpGauge.SetPercentage(self.playerKills[i], self.maxKill)
			hpGauge.Show()
			self.children.append(raceImage)
			self.children.append(txName)
			self.children.append(hpGauge)

		self.SetSize(WIDTH, yPos + Y_PASS)
		thinBoard.SetSize(WIDTH, yPos + Y_PASS)

		self.children.append(thinBoard)
		
		if app.ENABLE_PVP_RANKING_WITH_EMPIRE and self.IsRankEmpire == 1:
			thinBoardEmpire.SetSize(WIDTH, (Y_PASS * 2) + Y_START + Y_PASS)
			self.children.append(thinBoardEmpire)

		
		self.SetPosition(5, wndMgr.GetScreenHeight() - (yPos + 120))
		if not self.IsShow(): self.Show()

	def EmptyWindow(self):
		self.Clear()
		self.AddFlag('movable')
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.AddFlag('not_pick')
		thinBoard.Show()
		yPos = 0
		#for i in xrange(self.playerCount):
		#	yPos = (Y_PASS * i) + Y_START
		#	imageStr = FACE_IMAGE_DICT[self.playerRaces[i]]
		#	nameStr = "%s [Lv.%d]  %d / %d"  % (self.playerNames[i], self.playerLevels[i], self.playerKills[i], self.playerDeads[i])
		#	raceImage = ui.MakeImageBox(thinBoard, imageStr, X_START - 3, yPos - 6)
		#	txName = ui.MakeTextLineNew(thinBoard, X_START + 25, yPos - 4, nameStr,)
		#	#txName.SetPackedFontColor(self.GetColorAsEmpireIndex(self.playerEmpires[i]))
		#	hpGauge = ui.Gauge()
		#	hpGauge.SetParent(thinBoard)
		#	hpGauge.MakeGauge(117, "red")
		#	hpGauge.SetPosition(165, yPos)
		#	hpGauge.SetPercentage(self.playerKills[i], MAX_KILL)
		#	hpGauge.Show()
		#	self.children.append(raceImage)
		#	self.children.append(txName)
		#	self.children.append(hpGauge)
		
		txName = ui.MakeTextLineNew(thinBoard, X_START + 25 + 60, yPos + 10, "Henüz skor yok.",)
		self.children.append(txName)
	
		self.SetSize(WIDTH, yPos + Y_PASS)
		thinBoard.SetSize(WIDTH, yPos + Y_PASS)

		self.children.append(thinBoard)
		self.SetPosition(5, wndMgr.GetScreenHeight() - (yPos + 120))
		if not self.IsShow(): self.Show()

	def GetColorAsEmpireIndex(self, empireIndex):
		if empireIndex == 1: return 0xffe34b4b
		if empireIndex == 2: return 0xfffaf884
		if empireIndex == 3: return 0xff84a3fa
	def Close(self):
		self.Hide()
		self.ClearPlayerInfo()
		self.Clear()

class AdminWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/pvprankadmin.py")
		except:
			import exception
			exception.Abort("PvPAdminWindow.LoadWindow")

		try:
			self.petfeed = self.GetChild("board")
			self.titleBar = self.GetChild("titlebar")

			self.editline1 = self.GetChild("InputValue1")
			self.editline2 = self.GetChild("InputValue2")
			self.editline3 = self.GetChild("InputValue3")
			self.editline4 = self.GetChild("InputValue4")

			self.okButton = self.GetChild("okButton")
			self.cancelButton = self.GetChild("cancelButton")

			self.okButton.SAFE_SetEvent(self.Ok)
			self.cancelButton.SAFE_SetEvent(self.Cancel)
			self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			self.editline1.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.editline2.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.editline3.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.editline4.SetEscapeEvent(ui.__mem_func__(self.Close))
			
			self.editline4.Hide()
		except:
			import exception
			exception.Abort("PvPAdminWindow.LoadWindow")

	def OpenDialog(self):
		self.SetTop()
		self.SetCenterPosition()
		self.editline2.SetFocus()
		self.editline3.SetFocus()
		self.editline1.SetFocus()
		# self.editline4.SetFocus()
		self.Show()

	def Ok(self):
		minLevel = self.editline1.GetText()
		maxLevel = self.editline2.GetText()
		maxKill = self.editline3.GetText()
		mapIndex = 103

		net.SendChatPacket("/pvp_ranking 1 %s %s %s %s " % (minLevel, maxLevel, maxKill, str(mapIndex)))

	def Cancel(self):
		net.SendChatPacket("/pvp_ranking 0 0 0 0 0")
		self.Close()

	def Close(self):
		self.Hide()
		return TRUE

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE
