import app
import net
import item

import ui_offline as ui
import uiToolTip
import constInfo
import localeInfo
import wndMgr

class Battlepass(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.HideToolTip()
		self.tab = {}
		self.gauge = {}
		self.gauge_f = None
		self.text = {}
		self.reward1 = {}
		self.reward2 = {}
		self.reward3 = {}
		self.icon = {}
		self.LoadWindow()
		self.Type_Desc = [0, 
		"Sonraki öðeyi al ve aç!", ## TYPE 1
		"Görevi tamamlamak için mobu yok et", ## TYPE 2
		"Görevi tamamlamak için OX etkinliðine katýlýn",## TYPE 3
		"Görevi tamamlamak için TANAKA etkinliðine katýlýn!", ## TYPE 4
		"Görevi tamamlamak için Mavi Ejderha öldür!",## TYPE 5
		"Görevi tamamlamak için balýk yakala", ## TYPE 6
		"Görevi tamamlamak için hasar rekorunu yükselt!", ## TYPE 7
		"Eþyalarý Demirci veya Seon-Pyeong ile yükselt", ## TYPE 8
		"Görevi tamamlamak için bir oyuncuyla düello yap!",## TYPE 9
		"Eþyalarý Demirci veya Seon-Pyeong ile yükselt", ## TYPE 10
		"Bir oyuncuyu yok ederek gücünüzü gösterin", ## TYPE 11
		"Bir oyuncuyu yok ederek gücünüzü gösterin", ## TYPE 12
		"Oto Baðýrmaktan mesaj gönderin.", ## TYPE 13
		"Tüm biyolog görevlerini bitirin.", ## TYPE 14
		]
		self.Type_Images = [0,0,
		"d:/ymir work/ui/game/battle_pass/mission_1_small.tga",		## Type 2
		"d:/ymir work/ui/game/battle_pass/mission_2_small.tga",		## Type 3
		"d:/ymir work/ui/game/battle_pass/mission_3_small.tga",		## Type 4
		"d:/ymir work/ui/game/battle_pass/mission_4_small.tga",		## Type 5
		"d:/ymir work/ui/game/battle_pass/mission_5_small.tga",		## Type 6
		"d:/ymir work/ui/game/battle_pass/mission_6_small.tga",		## Type 7
		"d:/ymir work/ui/game/battle_pass/mission_7_small.tga",		## Type 8
		"d:/ymir work/ui/game/battle_pass/mission_8_small.tga",		## Type 9
		"d:/ymir work/ui/game/battle_pass/mission_9_small.tga",		## Type 10
		"d:/ymir work/ui/game/battle_pass/mission_10_small.tga",	## Type 11
		]

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Show(self):
		self.LoadWindow()
		self.ScrollBar.SetMiddleBarSize(float(6) / float(constInfo.size_battle_pass))
		self.final_reward.SetItemSlot(0, constInfo.final_rewards[0], constInfo.final_rewards[3])
		self.final_reward.SetItemSlot(1, constInfo.final_rewards[1], constInfo.final_rewards[4])
		self.final_reward.SetItemSlot(2, constInfo.final_rewards[2], constInfo.final_rewards[5])	
		for i in range(6):
			self.MakeButton(
				i,\
				self.board,\
				13, 33 + (41 * i)
			)
		self.SetCenterPosition()
		self.select = None
		ui.ScriptWindow.Show(self)
		
	def LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/battlepass.py")
		except:
			import exception
			exception.Abort("battlepass.LoadWindow.LoadObject")
		try:
			self.titleBar = self.GetChild("TitleBar")
			self.board = self.GetChild("board")
			self.board_reward = self.GetChild("DesignTop")
			self.ScrollBar = self.GetChild("ScrollBar")
			self.info1 = self.GetChild("Text1Info")
			self.info2 = self.GetChild("Text2Info")
			self.info3 = self.GetChild("Text3Info")
			self.info4 = self.GetChild("Text5Info")
			self.info5 = self.GetChild("Text6Info")
			self.info6 = self.GetChild("Text7Info")
			self.f_button = self.GetChild("FinalReward")
			self.finish_mission = self.GetChild("finish_mission")
			self.ScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))		
		except:
			import exception
			exception.Abort("battlepass.__LoadWindow.BindObject")
	
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))	
		self.f_button.SetEvent(lambda : net.SendChatPacket("/final_reward"))
		self.final_reward = ui.GridSlotWindow()
		self.final_reward.SetParent(self)
		self.final_reward.SetPosition(428, 218)
		self.final_reward.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.final_reward.ArrangeSlot(0, 3, 2, 32, 32, 0, 3)
		self.final_reward.SetOverInItemEvent(ui.__mem_func__(self.OverInItemFinal))
		self.final_reward.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.final_reward.RefreshSlot()
		self.final_reward.Show()

	def Close(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None

	def OnUpdate(self):
		if self.select != None:
			if self.Get2(self.select, "iStatus") > 0:
				self.info2.SetText("- Durumu: " + "|cff82ff7dBitti")
			else:
				self.info2.SetText("- Durumu: " + "|cffff0000Devam Ediyor")
			self.info3.SetText("- Ýlerleme: " + str(self.Get2(self.select, "iCounts")) + " / " + str(self.Get(self.select, "iCount")))
		self.gauge_f.SetPercentage(self.GetFinishedMission(), constInfo.size_battle_pass)
		for i in range(len(self.text)):
			self.gauge[i].SetPercentage(self.Get2(i, "iCounts"), self.Get(i, "iCount"))
		for i in range(len(self.tab)):
			if self.tab[i].IsDown():
				self.select = i
				MissionName = str(constInfo.info_missions_bp[int(i)]["Name"]).replace("Oldur", "Öldür")
				EfsunName = str(constInfo.info_missions_bp[int(i)]["Efsun"])
				self.info1.SetText("- Görev Adý: " + str(MissionName))
				self.info6.SetText("- Ödül: " + str(EfsunName))
				if self.Get2(i, "iStatus") > 0:
					self.info2.SetText("- Durumu: " + "|cff82ff7dBitti")
				else:
					self.info2.SetText("- Durumu: " + "|cffff0000Devam Ediyor")
				self.info3.SetText("- Ýlerleme: " + str(self.Get2(i, "iCounts")) + " / " + str(self.Get(i, "iCount")))
				self.info4.SetText("-Ýpucu: " + "|cFF00FFFF" + str(MissionName))
				self.info5.SetText("|cffffcc00" + self.Type_Desc[self.Get(i, "iType")])
				
				self.finish_mission.SetEvent(ui.__mem_func__(self.__ClickFinish), self.select)

	def __ClickFinish(self,index):
		net.SendChatPacket("/pass_finish %d" % index)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OnScroll(self):
		board_count = 6
		pos = int(self.ScrollBar.GetPos() * (constInfo.size_battle_pass - board_count))
		
		for i in xrange(board_count):
			realPos = i + pos
			self.MakeButton(
				realPos,\
				self.board,\
				13, 33 + (41 * i)
			)
	def GetFinishedMission(self):
		finished = 0
		for i in range(constInfo.size_battle_pass):
			if int(constInfo.info_missions_bp[int(i)]["iStatus"]) > 0:
				finished = finished + 1
		return finished
	
	def Get(self,index, var2):
		try:
			return int(constInfo.missions_bp[int(index)][var2])
		except KeyError:
			return 0
			
	def Get2(self,index, var2):
		try:
			return int(constInfo.info_missions_bp[int(index)][var2])
		except KeyError:
			return 0
			
	def Get3(self,index, var2):
		try:
			return int(constInfo.rewards_bp[int(index)][var2])
		except KeyError:
			return 0

	def MakeButton(self, index, parent, x, y):
		self.tab[index] = ui.MakeButton(parent, x, y, False, "d:/ymir work/battle_pass/", "tab_normal.tga", "tab_select.tga", "tab_normal.tga")
		self.gauge[index] = ui.MakeGauge(self.tab[index], 41, 23, 130)
		self.gauge_f = ui.MakeGauge(parent, 326, 235, 92)
		self.text[index] = ui.TextLine()
		self.text[index].SetParent(self.tab[index])
		self.text[index].SetPosition(50, 8)
		MissionName2 = str(constInfo.info_missions_bp[int(index)]["Name"]).replace("Oldur", "Öldür")
		self.text[index].SetText(str(MissionName2))
		self.text[index].Show()
		
		self.reward1[index] = ui.MakeGridSlot(self.tab[index], 180+7, 2+4, self.Get3(index, "iVnum1"), self.Get3(index, "iCount1"))
		self.reward1[index].SetOverInItemEvent(lambda slotindex = 0, ivnumz = index: self.OverInItem(slotindex, ivnumz, "iVnum1"))
		self.reward1[index].SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.reward2[index] = ui.MakeGridSlot(self.tab[index], 180+32+7, 2+4, self.Get3(index, "iVnum2"), self.Get3(index, "iCount2"))
		self.reward2[index].SetOverInItemEvent(lambda slotindex = 0, ivnumz = index: self.OverInItem(slotindex, ivnumz, "iVnum2"))
		self.reward2[index].SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.reward3[index] = ui.MakeGridSlot(self.tab[index], 217+28+7, 2+4, self.Get3(index, "iVnum3"), self.Get3(index, "iCount3"))
		self.reward3[index].SetOverInItemEvent(lambda slotindex = 0, ivnumz = index: self.OverInItem(slotindex, ivnumz, "iVnum3"))
		self.reward3[index].SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.icon[index] = ui.MakeImageBoxNoImg(self.tab[index], 1, 2)
		if self.Get(index, "iType") == 1: # Category: Use Items
			item.SelectItem(self.Get(index, "iVnum"))
			self.icon[index].LoadImage(item.GetIconImageFileName())
		if self.Get(index, "iType") == 2:
			self.icon[index].LoadImage("d:/ymir work/battle_pass/mobs/%d.png" % (self.Get(index, "iVnum")))
		if self.Get(index, "iType") == 13:
			self.icon[index].LoadImage("d:/ymir work/battle_pass/chat.tga")
		if self.Get(index, "iType") == 14:
			self.icon[index].LoadImage("d:/ymir work/battle_pass/biyolog.tga")
		#if self.Get(index, "iType") > 2:
			#self.icon[index].LoadImage(self.Type_Images[self.Get(index, "iType")])
	
	def OverInItem(self, slotindex, i, var):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(self.Get3(i, var))
	
	def OverInItemFinal(self, slotindex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constInfo.final_rewards[slotindex])

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def OnCancel(self):
		self.Hide()
		return True