import ui
import uiscriptlocale
import mousemodule
import constInfo
import localeInfo
import skill
import net
import item
import chr
import effect
import dbg
import background
import math
import constInfo
import app
import chat
import uiToolTip
import wndMgr

class DailyReward(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.HideToolTip()
		self.board = None
		self.LoadWindow()
		



	def __del__(self):
		self.Destroy()
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/dailyreward.py")
		except:
			import exception
			exception.Abort("DailyReward.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")
			self.item1 = GetObject("item1")
			self.item2 = GetObject("item2")
			self.item3 = GetObject("item3")
			self.item4 = GetObject("item4")
			self.item5 = GetObject("item5")
			self.item6 = GetObject("item6")
			self.item7 = GetObject("item7")
			self.time = GetObject("time")

			self.board.SetCloseEvent(ui.__mem_func__(self.__OnCloseButtonClick))
			
			self.item1.SetItemSlot(0, constInfo.daily_reward[1][0], constInfo.daily_reward[1][1])
			self.item2.SetItemSlot(0, constInfo.daily_reward[2][0], constInfo.daily_reward[2][1])
			self.item3.SetItemSlot(0, constInfo.daily_reward[3][0], constInfo.daily_reward[3][1])
			self.item4.SetItemSlot(0, constInfo.daily_reward[4][0], constInfo.daily_reward[4][1])
			self.item5.SetItemSlot(0, constInfo.daily_reward[5][0], constInfo.daily_reward[5][1])
			self.item6.SetItemSlot(0, constInfo.daily_reward[6][0], constInfo.daily_reward[6][1])
			self.item7.SetItemSlot(0, constInfo.daily_reward[7][0], constInfo.daily_reward[7][1])


		except:
			import exception
			exception.Abort("DailyReward.LoadDialog.BindObject")
					
		self.item1.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.item1.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.item2.SetOverInItemEvent(ui.__mem_func__(self.OverInItem2))
		self.item2.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.item3.SetOverInItemEvent(ui.__mem_func__(self.OverInItem3))
		self.item3.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.item4.SetOverInItemEvent(ui.__mem_func__(self.OverInItem4))
		self.item4.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.item5.SetOverInItemEvent(ui.__mem_func__(self.OverInItem5))
		self.item5.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.item6.SetOverInItemEvent(ui.__mem_func__(self.OverInItem6))
		self.item6.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.item7.SetOverInItemEvent(ui.__mem_func__(self.OverInItem7))
		self.item7.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		
		self.item1.SetSelectItemSlotEvent(ui.__mem_func__(self.GiveReward))
		self.item2.SetSelectItemSlotEvent(ui.__mem_func__(self.GiveReward2))
		self.item3.SetSelectItemSlotEvent(ui.__mem_func__(self.GiveReward3))
		self.item4.SetSelectItemSlotEvent(ui.__mem_func__(self.GiveReward4))
		self.item5.SetSelectItemSlotEvent(ui.__mem_func__(self.GiveReward5))
		self.item6.SetSelectItemSlotEvent(ui.__mem_func__(self.GiveReward6))
		self.item7.SetSelectItemSlotEvent(ui.__mem_func__(self.GiveReward7))
		
	def SetLeftTime(self,time):
		self.time.SetText(localeInfo.LEFT_TIME + " : " + time)
		
	def Collect(self,index):
		if int(index) == 1:
			constInfo.DAILY_REWARD_COLLECT1 = 1
		elif int(index) == 2:
			constInfo.DAILY_REWARD_COLLECT2 = 1
		elif int(index) == 3:
			constInfo.DAILY_REWARD_COLLECT3 = 1
		elif int(index) == 4:
			constInfo.DAILY_REWARD_COLLECT4 = 1
		elif int(index) == 5:
			constInfo.DAILY_REWARD_COLLECT5 = 1
		elif int(index) == 6:
			constInfo.DAILY_REWARD_COLLECT6 = 1
		elif int(index) == 7:
			constInfo.DAILY_REWARD_COLLECT7 = 1
			
	def Collect2(self,index):
		if int(index) == 1:
			constInfo.DAILY_REWARD_COLLECT1 = 0
		elif int(index) == 2:
			constInfo.DAILY_REWARD_COLLECT2 = 0
		elif int(index) == 3:
			constInfo.DAILY_REWARD_COLLECT3 = 0
		elif int(index) == 4:
			constInfo.DAILY_REWARD_COLLECT4 = 0
		elif int(index) == 5:
			constInfo.DAILY_REWARD_COLLECT5 = 0
		elif int(index) == 6:
			constInfo.DAILY_REWARD_COLLECT6 = 0
		elif int(index) == 7:
			constInfo.DAILY_REWARD_COLLECT7 = 0
			
	#def ShowReward(self):
	#	self.item1.SetItemSlot(0, constInfo.daily_reward[0], constInfo.daily_reward[1])
	#	self.item2.SetItemSlot(0, constInfo.daily_reward[2], constInfo.daily_reward[3])
	#	self.item3.SetItemSlot(0, constInfo.daily_reward[4], constInfo.daily_reward[5])
	#	self.item4.SetItemSlot(0, constInfo.daily_reward[6], constInfo.daily_reward[7])
	#	self.item5.SetItemSlot(0, constInfo.daily_reward[8], constInfo.daily_reward[9])
	#	self.item6.SetItemSlot(0, constInfo.daily_reward[10], constInfo.daily_reward[11])
	#	self.item7.SetItemSlot(0, constInfo.daily_reward[12], constInfo.daily_reward[13])
		
	def OnUpdate(self):
		if constInfo.DAILY_REWARD_COLLECT1 == 1:
			self.item1.SetCantMouseEventSlot(0)
		if constInfo.DAILY_REWARD_COLLECT2 == 1:
			self.item2.SetCantMouseEventSlot(0)
		if constInfo.DAILY_REWARD_COLLECT3 == 1:
			self.item3.SetCantMouseEventSlot(0)
		if constInfo.DAILY_REWARD_COLLECT4 == 1:
			self.item4.SetCantMouseEventSlot(0)
		if constInfo.DAILY_REWARD_COLLECT5 == 1:
			self.item5.SetCantMouseEventSlot(0)
		if constInfo.DAILY_REWARD_COLLECT6 == 1:
			self.item6.SetCantMouseEventSlot(0)
		if constInfo.DAILY_REWARD_COLLECT7 == 1:
			self.item7.SetCantMouseEventSlot(0)
		if int(constInfo.daily_reward_left_time) > app.GetGlobalTimeStamp():
			self.SetLeftTime(localeInfo.SecondToDHM(int(constInfo.daily_reward_left_time) - app.GetGlobalTimeStamp()))
		else:
			self.time.SetText("|cff82ff7dÖdül Alýnabilir")

			
	def GiveReward(self):
		net.SendChatPacket("/givedailyreward 1")
		
	def GiveReward2(self):
		net.SendChatPacket("/givedailyreward 2")
		
	def GiveReward3(self):
		net.SendChatPacket("/givedailyreward 3")
	
	def GiveReward4(self):
		net.SendChatPacket("/givedailyreward 4")
		
	def GiveReward5(self):
		net.SendChatPacket("/givedailyreward 5")
		
	def GiveReward6(self):
		net.SendChatPacket("/givedailyreward 6")
		
	def GiveReward7(self):
		net.SendChatPacket("/givedailyreward 7")
			
	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Destroy(self):
		self.ClearDictionary()
		self.titleBar = None
		self.tooltipItem = None
		

	def Open(self):			
		self.Show()
		#self.ShowReward()
		self.SetCenterPosition()


	def Close(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.Hide()
		

	def Clear(self):
		self.Refresh()

	def Refresh(self):
		pass

	def __OnCloseButtonClick(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
	
	def OverInItem(self, slotindex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constInfo.daily_reward[1][0])
			
	def OverInItem2(self, slotindex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constInfo.daily_reward[2][0])
			
	def OverInItem3(self, slotindex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constInfo.daily_reward[3][0])
			
	def OverInItem4(self, slotindex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constInfo.daily_reward[4][0])
			
	def OverInItem5(self, slotindex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constInfo.daily_reward[5][0])
			
	def OverInItem6(self, slotindex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constInfo.daily_reward[6][0])
			
	def OverInItem7(self, slotindex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constInfo.daily_reward[7][0])
