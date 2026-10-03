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


class BiyologEkran(ui.ScriptWindow):


	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		self.board = None
		self.kalan = 0
		self.gerekli = 0
		self.ruh = 0
		self.hediyee = 0
		self.ruhtami = 0
		self.durum = 0
		self.LoadWindow()
		



	def __del__(self):
		self.Destroy()
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/biyolog.py")
		except:
			import exception
			exception.Abort("BiyologEkran.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")
			self.info1 = GetObject("info1")
			self.info2 = GetObject("info2")
			self.info3 = GetObject("info3")
			self.zamantext = GetObject("zamantext")
			self.adettext = GetObject("adettext")
			self.gorevver = GetObject("gorevver")
			self.ilkitem = GetObject("ilkitem")
			self.ruhtasi = GetObject("ruhtasi")
			self.hediyeslot = GetObject("hediye")
			self.bonus1 = GetObject("bonus1")
			self.bonus2 = GetObject("bonus2")
			self.bonus3 = GetObject("bonus3")
			

			
			self.board.SetCloseEvent(ui.__mem_func__(self.__OnCloseButtonClick))
			self.gorevver.SetEvent(ui.__mem_func__(self.vergitsin))
			self.info1.SetItemSlot(0, 39023, 0)
			self.info2.SetItemSlot(0, 96053, 0)
			self.info3.SetItemSlot(0, 96054, 0)
		except:
			import exception
			exception.Abort("BiyologEkran.LoadDialog.BindObject")
			
		
		self.info1.SetSelectItemSlotEvent(ui.__mem_func__(self.Durum1))
		self.info2.SetSelectItemSlotEvent(ui.__mem_func__(self.Durum2))
		self.info3.SetSelectItemSlotEvent(ui.__mem_func__(self.Durum3))
		self.durum = 0


	
	def Durum1(self):
		if self.durum == 1:
			self.info1.DeactivateSlot(0)
			self.info2.DeactivateSlot(0)
			self.info3.DeactivateSlot(0)
			chat.AppendChat(1,"Araþtýrmacýnýn özütüyle okuma deaktif edildi.") 
			self.durum = 0
		else:
			self.durum = 1
			self.info1.ActivateSlot(0)
			self.info2.DeactivateSlot(0)
			self.info3.DeactivateSlot(0)
			chat.AppendChat(1,"Görevi verirken (varsa) araþtýrmacýnýn özütüyle okuma aktif edildi.") 
			
	def Durum2(self):
		if self.durum == 2:
			self.info1.DeactivateSlot(0)
			self.info2.DeactivateSlot(0)
			self.info3.DeactivateSlot(0)
			chat.AppendChat(1,"Biyolog süre özütüyle okuma deaktif edildi.") 
			self.durum = 0
		else:
			self.durum = 2
			self.info1.DeactivateSlot(0)
			self.info2.ActivateSlot(0)
			self.info3.DeactivateSlot(0)
			chat.AppendChat(1,"Görevi verirken (varsa) biyolog süre özütüyle okuma aktif edildi.") 
			
	def Durum3(self):
		if self.durum == 3:
			self.info1.DeactivateSlot(0)
			self.info2.DeactivateSlot(0)
			self.info3.DeactivateSlot(0)
			chat.AppendChat(1,"Biyolog özütüyle okuma deaktif edildi.") 
			self.durum = 0
		else:
			self.durum = 3
			self.info1.DeactivateSlot(0)
			self.info2.DeactivateSlot(0)
			self.info3.ActivateSlot(0)
			chat.AppendChat(1,"Görevi verirken (varsa) biyolog özütüyle okuma aktif edildi.") 
	
	
	def vergitsin(self):
		if self.durum == 0:
			net.SendChatPacket("/biyologver " +str(self.durum))
		else:
			net.SendChatPacket("/biyologver " +str(self.durum))
	
	
	def SetBiyolog(self, bioitem, verilen, toplam, kalansure, ruhtasii, hediye, ruhtamii):
		if bioitem == 0:
			self.board.SetTitleName("Biyolog")
		else:
			self.board.SetTitleName("Biyolog - "+ str(constInfo.biyologinfo[int(bioitem)][0]))
			
		if int(bioitem) == 0:
			self.ilkitem.SetSlot(0, 1, 32, 32, 0 )
		else:
			self.ilkitem.SetItemSlot(0, int(bioitem))	
			
		if int(ruhtasii) == 0:
			self.ruhtasi.SetSlot(0, 1, 32, 32, 0)
		else:
			self.ruhtasi.SetItemSlot(0, int(ruhtasii))
			
		if int(hediye) == 0:
			self.hediyeslot.SetSlot(0, 1, 32, 32,0 )
		else:
			self.hediyeslot.SetItemSlot(0, int(hediye))
			
		# self.ilkitem.SetItemSlot(0, int(bioitem))
		# self.ruhtasi.SetItemSlot(0, int(ruhtasii))
		# self.hediyeslot.SetItemSlot(0, int(hediye))
		if ruhtamii == 1:
			self.ruhtasi.ActivateSlot(0)
			self.ilkitem.DeactivateSlot(0)
		else:
			self.ilkitem.ActivateSlot(0)
			self.ruhtasi.DeactivateSlot(0)
		self.kalan = int(kalansure)
		self.gerekli = int(bioitem)
		self.ruh = int(ruhtasii)
		self.hediyee = int(hediye)
		self.ruhtami = int(ruhtamii)
		self.adettext.SetText(str(verilen)+" - "+str(toplam))
		self.bonus1.SetText("Bonus 1 : " + str(constInfo.biyologinfo[int(bioitem)][1]))
		self.bonus2.SetText("Bonus 2 : " + str(constInfo.biyologinfo[int(bioitem)][2]))
		self.bonus3.SetText("Bonus 3 : " + str(constInfo.biyologinfo[int(bioitem)][3]))
		self.RefreshSlot()
		
		
	def OnUpdate(self):
		import time
		current_milli_time = int(app.GetGlobalTimeStamp())
		if int(self.kalan) == 0:
			self.zamantext.SetText("Verilebilir!")
		elif (int(self.kalan)-current_milli_time <= 0):
			self.zamantext.SetText("Verilebilir!")
		else:
			self.zamantext.SetText(str(localeInfo.surever(int(self.kalan)-current_milli_time)))
			
			
	def RefreshSlot(self):
		vnum= int (self.gerekli)
		ruhver= int (self.ruh)
		hver= int (self.hediyee)
		
		if vnum > 0:
		
		
			if int(vnum) == 0:
				self.ilkitem.SetSlot(0, 1, 32, 32,0 )
			else:
				self.ilkitem.SetItemSlot(0, int(vnum))	
				
			if int(ruhver) == 0:
				self.ruhtasi.SetSlot(0, 1, 32, 32, 0)
			else:
				self.ruhtasi.SetItemSlot(0, int(ruhver))
				
			if int(hver) == 0:
				self.hediyeslot.SetSlot(0, 1, 32, 32, 0)
			else:
				self.hediyeslot.SetItemSlot(0, int(hver))
		
			
			if self.ruhtami == 1:
				self.ruhtasi.ActivateSlot(0)
				self.ilkitem.DeactivateSlot(0)
			else:
				self.ilkitem.ActivateSlot(0)
				self.ruhtasi.DeactivateSlot(0)
			
			
		else:	
			self.ilkitem.SetSlot(0, 1, 32, 32, 0)
			self.ruhtasi.SetSlot(0, 1, 32, 32,0 )
			self.hediyeslot.SetSlot(0, 1, 32, 32, 0)
			self.ruhtasi.DeactivateSlot(0)
			self.ilkitem.DeactivateSlot(0)
			return
			
		self.ilkitem.RefreshSlot()
		self.ruhtasi.RefreshSlot()
		self.hediyeslot.RefreshSlot()
	
	
	def Destroy(self):
		self.ClearDictionary()
		self.titleBar = None
		

	def Open(self):			
		self.Show()
		self.RefreshSlot()
		self.SetCenterPosition()


	def Close(self):
		self.Hide()


	def Clear(self):
		self.Refresh()

	def Refresh(self):
		pass

	def __OnCloseButtonClick(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()

