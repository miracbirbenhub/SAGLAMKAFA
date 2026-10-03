import uiCommon, ui, time, playersettingmodule, localeInfo, mouseModule, constInfo, uiScriptLocale, interfaceModule, dbg, wndMgr, snd, item, player, net, app
import eventtime

class eventsystemwindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()


	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/takvim_gui.py")
		except:
			import exception
			exception.Abort("FelixEventTakvimiPenceresi.LoadWindow.LoadObject")
		try:
			self.titleBar = self.GetChild("titlebar")
			self.board = self.GetChild("board")
			self.FelixScrollBar = self.GetChild("ScrollBar")
			self.title_name_olds = self.GetChild("title_name_old")
##---------------------------------------------------------------------------			
			self.pazartesi_baslangic = self.GetChild("pazartesi_baslangicc")
			self.pazartesi_bitis = self.GetChild("pazartesi_bitiss")
##---------------------------------------------------------------------------			
			self.sali_baslangic = self.GetChild("sali_baslangicc")
			self.sali_bitis = self.GetChild("sali_bitiss")
##---------------------------------------------------------------------------			
			self.carsamba_baslangic = self.GetChild("carsamba_baslangicc")
			self.carsamba_bitis = self.GetChild("carsamba_bitiss")
##---------------------------------------------------------------------------			
			self.persembe_baslangic = self.GetChild("persembe_baslangicc")
			self.persembe_bitis = self.GetChild("persembe_bitiss")
##---------------------------------------------------------------------------			
			self.cuma_baslangic = self.GetChild("cuma_baslangicc")
			self.cuma_bitis = self.GetChild("cuma_bitiss")
##---------------------------------------------------------------------------			
			self.ctesi_baslangic = self.GetChild("ctesi_baslangicc")
			self.ctesi_bitis = self.GetChild("ctesi_bitiss")
##---------------------------------------------------------------------------			
			self.pazar_baslangic = self.GetChild("pazar_baslangicc")
			self.pazar_bitis = self.GetChild("pazar_bitiss")
##---------------------------------------------------------------------------			
			
			self.GetChild("btnayisik").SAFE_SetEvent(self.__MenuFunction, 1)
			self.GetChild("btnfutbol").SAFE_SetEvent(self.__MenuFunction, 2)
			self.GetChild("btnbulmaca").SAFE_SetEvent(self.__MenuFunction, 3)
			self.GetChild("btnokeykart").SAFE_SetEvent(self.__MenuFunction, 4)
			self.GetChild("btnexp").SAFE_SetEvent(self.__MenuFunction, 5)
			self.GetChild("btnaltigen").SAFE_SetEvent(self.__MenuFunction, 6)
		except:
			import exception
			exception.Abort("FelixEventTakvimiPenceresi.LoadWindow.BindObject")
			
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		

		
		self.pazartesi_baslangic.SetText("Pazartesi Baþlangýç : " + "Event seçimi yapýlmadý !")
		self.pazartesi_bitis.SetText("Pazartesi Bitiþ : " + "Event seçimi yapýlmadý !")
		self.sali_baslangic.SetText("Salý Baþlangýç : " + "Event seçimi yapýlmadý !")
		self.sali_bitis.SetText("Salý Bitiþ : " + "Event seçimi yapýlmadý !")
		self.carsamba_baslangic.SetText("Çarþamba Baþlangýç : " + "Event seçimi yapýlmadý !")
		self.carsamba_bitis.SetText("Çarþamba Bitiþ : " + "Event seçimi yapýlmadý !")
		self.persembe_baslangic.SetText("Perþembe Baþlangýç : " + "Event seçimi yapýlmadý !")
		self.persembe_bitis.SetText("Perþembe Bitiþ : " + "Event seçimi yapýlmadý !")
		self.cuma_baslangic.SetText("Cuma Baþlangýç : " + "Event seçimi yapýlmadý !")
		self.cuma_bitis.SetText("Cuma Bitiþ : " + "Event seçimi yapýlmadý !")
		self.ctesi_baslangic.SetText("Cumartesi Baþlangýç : " + "Event seçimi yapýlmadý !")
		self.ctesi_bitis.SetText("Cumartesi Bitiþ : " + "Event seçimi yapýlmadý !")
		self.pazar_baslangic.SetText("Pazar Baþlangýç : " + "Event seçimi yapýlmadý !")
		self.pazar_bitis.SetText("Pazar Bitiþ : " + "Event seçimi yapýlmadý !")

	def __MenuFunction(self, value):
		if value == 1:
			self.title_name_olds.SetText("GM Kayboldu Etkinliði Takvimi Gösteriliyor")
			self.pazartesi_baslangic.SetText("Pazartesi Baþlangýç : " + eventtime.AY_ISIK["pazartesi_basla"])
			self.pazartesi_bitis.SetText("Pazartesi Bitiþ : " + eventtime.AY_ISIK["pazartesi_bitir"])
			self.sali_baslangic.SetText("Salý Baþlangýç : " + eventtime.AY_ISIK["sali_basla"])
			self.sali_bitis.SetText("Salý Bitiþ : " + eventtime.AY_ISIK["sali_bitir"])
			self.carsamba_baslangic.SetText("Çarþamba Baþlangýç : " + eventtime.AY_ISIK["carsamba_basla"])
			self.carsamba_bitis.SetText("Çarþamba Bitiþ : " + eventtime.AY_ISIK["carsamba_bitir"])
			self.persembe_baslangic.SetText("Perþembe Baþlangýç : " + eventtime.AY_ISIK["persembe_basla"])
			self.persembe_bitis.SetText("Perþembe Bitiþ : " + eventtime.AY_ISIK["persembe_bitir"])
			self.cuma_baslangic.SetText("Cuma Baþlangýç : " + eventtime.AY_ISIK["cuma_basla"])
			self.cuma_bitis.SetText("Cuma Bitiþ : " + eventtime.AY_ISIK["cuma_bitir"])
			self.ctesi_baslangic.SetText("Cumartesi Baþlangýç : " + eventtime.AY_ISIK["ctesi_basla"])
			self.ctesi_bitis.SetText("Cumartesi Bitiþ : " + eventtime.AY_ISIK["ctesi_bitir"])
			self.pazar_baslangic.SetText("Pazar Baþlangýç : " + eventtime.AY_ISIK["pazar_basla"])
			self.pazar_bitis.SetText("Pazar Bitiþ : " + eventtime.AY_ISIK["pazar_bitir"])
			
		elif value == 2:
			self.title_name_olds.SetText("GM Soru Etkinliði Takvimi Gösteriliyor")
			self.pazartesi_baslangic.SetText("Pazartesi Baþlangýç : " + eventtime.FUTBOL["pazartesi_basla"])
			self.pazartesi_bitis.SetText("Pazartesi Bitiþ : " + eventtime.FUTBOL["pazartesi_bitir"])
			self.sali_baslangic.SetText("Salý Baþlangýç : " + eventtime.FUTBOL["sali_basla"])
			self.sali_bitis.SetText("Salý Bitiþ : " + eventtime.FUTBOL["sali_bitir"])
			self.carsamba_baslangic.SetText("Çarþamba Baþlangýç : " + eventtime.FUTBOL["carsamba_basla"])
			self.carsamba_bitis.SetText("Çarþamba Bitiþ : " + eventtime.FUTBOL["carsamba_bitir"])
			self.persembe_baslangic.SetText("Perþembe Baþlangýç : " + eventtime.FUTBOL["persembe_basla"])
			self.persembe_bitis.SetText("Perþembe Bitiþ : " + eventtime.FUTBOL["persembe_bitir"])
			self.cuma_baslangic.SetText("Cuma Baþlangýç : " + eventtime.FUTBOL["cuma_basla"])
			self.cuma_bitis.SetText("Cuma Bitiþ : " + eventtime.FUTBOL["cuma_bitir"])
			self.ctesi_baslangic.SetText("Cumartesi Baþlangýç : " + eventtime.FUTBOL["ctesi_basla"])
			self.ctesi_bitis.SetText("Cumartesi Bitiþ : " + eventtime.FUTBOL["ctesi_bitir"])
			self.pazar_bitis.SetText("Pazar Bitiþ : " + eventtime.FUTBOL["pazar_bitir"])
			self.pazar_baslangic.SetText("Pazar Baþlangýç : " + eventtime.FUTBOL["pazar_basla"])

		elif value == 3:
			self.title_name_olds.SetText("Ox Etkinliði Takvimi Gösteriliyor")
			self.pazartesi_baslangic.SetText("Pazartesi Baþlangýç : " + eventtime.BULMACA["pazartesi_basla"])
			self.pazartesi_bitis.SetText("Pazartesi Bitiþ : " + eventtime.BULMACA["pazartesi_bitir"])
			self.sali_baslangic.SetText("Salý Baþlangýç : " + eventtime.BULMACA["sali_basla"])
			self.sali_bitis.SetText("Salý Bitiþ : " + eventtime.BULMACA["sali_bitir"])
			self.carsamba_baslangic.SetText("Çarþamba Baþlangýç : " + eventtime.BULMACA["carsamba_basla"])
			self.carsamba_bitis.SetText("Çarþamba Bitiþ : " + eventtime.BULMACA["carsamba_bitir"])
			self.persembe_baslangic.SetText("Perþembe Baþlangýç : " + eventtime.BULMACA["persembe_basla"])
			self.persembe_bitis.SetText("Perþembe Bitiþ : " + eventtime.BULMACA["persembe_bitir"])
			self.cuma_baslangic.SetText("Cuma Baþlangýç : " + eventtime.BULMACA["cuma_basla"])
			self.cuma_bitis.SetText("Cuma Bitiþ : " + eventtime.BULMACA["cuma_bitir"])
			self.ctesi_baslangic.SetText("Cumartesi Baþlangýç : " + eventtime.BULMACA["ctesi_basla"])
			self.ctesi_bitis.SetText("Cumartesi Bitiþ : " + eventtime.BULMACA["ctesi_bitir"])
			self.pazar_baslangic.SetText("Pazar Baþlangýç : " + eventtime.BULMACA["pazar_basla"])
			self.pazar_bitis.SetText("Pazar Bitiþ : " + eventtime.BULMACA["pazar_bitir"])

		elif value == 4:
			self.title_name_olds.SetText("Ronark Etkinliði Takvimi Gösteriliyor")
			self.pazartesi_baslangic.SetText("Pazartesi Baþlangýç : " + eventtime.OKEY_KART["pazartesi_basla"])
			self.pazartesi_bitis.SetText("Pazartesi Bitiþ : " + eventtime.OKEY_KART["pazartesi_bitir"])
			self.sali_baslangic.SetText("Salý Baþlangýç : " + eventtime.OKEY_KART["sali_basla"])
			self.sali_bitis.SetText("Salý Bitiþ : " + eventtime.OKEY_KART["sali_bitir"])
			self.carsamba_baslangic.SetText("Çarþamba Baþlangýç : " + eventtime.OKEY_KART["carsamba_basla"])
			self.carsamba_bitis.SetText("Çarþamba Bitiþ : " + eventtime.OKEY_KART["carsamba_bitir"])
			self.persembe_baslangic.SetText("Perþembe Baþlangýç : " + eventtime.OKEY_KART["persembe_basla"])
			self.persembe_bitis.SetText("Perþembe Bitiþ : " + eventtime.OKEY_KART["persembe_bitir"])
			self.cuma_baslangic.SetText("Cuma Baþlangýç : " + eventtime.OKEY_KART["cuma_basla"])
			self.cuma_bitis.SetText("Cuma Bitiþ : " + eventtime.OKEY_KART["cuma_bitir"])
			self.ctesi_baslangic.SetText("Cumartesi Baþlangýç : " + eventtime.OKEY_KART["ctesi_basla"])
			self.ctesi_bitis.SetText("Cumartesi Bitiþ : " + eventtime.OKEY_KART["ctesi_bitir"])
			self.pazar_baslangic.SetText("Pazar Baþlangýç : " + eventtime.OKEY_KART["pazar_basla"])
			self.pazar_bitis.SetText("Pazar Bitiþ : " + eventtime.OKEY_KART["pazar_bitir"])

		elif value == 5:
			self.title_name_olds.SetText("Bireysel Turnuva Etkinliði Takvimi Gösteriliyor")
			self.pazartesi_baslangic.SetText("Pazartesi Baþlangýç : " + eventtime.EXP["pazartesi_basla"])
			self.pazartesi_bitis.SetText("Pazartesi Bitiþ : " + eventtime.EXP["pazartesi_bitir"])
			self.sali_baslangic.SetText("Salý Baþlangýç : " + eventtime.EXP["sali_basla"])
			self.sali_bitis.SetText("Salý Bitiþ : " + eventtime.EXP["sali_bitir"])
			self.carsamba_baslangic.SetText("Çarþamba Baþlangýç : " + eventtime.EXP["carsamba_basla"])
			self.carsamba_bitis.SetText("Çarþamba Bitiþ : " + eventtime.EXP["carsamba_bitir"])
			self.persembe_baslangic.SetText("Perþembe Baþlangýç : " + eventtime.EXP["persembe_basla"])
			self.persembe_bitis.SetText("Perþembe Bitiþ : " + eventtime.EXP["persembe_bitir"])
			self.cuma_baslangic.SetText("Cuma Baþlangýç : " + eventtime.EXP["cuma_basla"])
			self.cuma_bitis.SetText("Cuma Bitiþ : " + eventtime.EXP["cuma_bitir"])
			self.ctesi_baslangic.SetText("Cumartesi Baþlangýç : " + eventtime.EXP["ctesi_basla"])
			self.ctesi_bitis.SetText("Cumartesi Bitiþ : " + eventtime.EXP["ctesi_bitir"])
			self.pazar_baslangic.SetText("Pazar Baþlangýç : " + eventtime.EXP["pazar_basla"])
			self.pazar_bitis.SetText("Pazar Bitiþ : " + eventtime.EXP["pazar_bitir"])

		elif value == 6:
			self.title_name_olds.SetText("Lonca Turnuvasý Etkinliði Takvimi Gösteriliyor")
			self.pazartesi_baslangic.SetText("Pazartesi Baþlangýç : " + eventtime.ALTIGEN["pazartesi_basla"])
			self.pazartesi_bitis.SetText("Pazartesi Bitiþ : " + eventtime.ALTIGEN["pazartesi_bitir"])
			self.sali_baslangic.SetText("Salý Baþlangýç : " + eventtime.ALTIGEN["sali_basla"])
			self.sali_bitis.SetText("Salý Bitiþ : " + eventtime.ALTIGEN["sali_bitir"])
			self.carsamba_baslangic.SetText("Çarþamba Baþlangýç : " + eventtime.ALTIGEN["carsamba_basla"])
			self.carsamba_bitis.SetText("Çarþamba Bitiþ : " + eventtime.ALTIGEN["carsamba_bitir"])
			self.persembe_baslangic.SetText("Perþembe Baþlangýç : " + eventtime.ALTIGEN["persembe_basla"])
			self.persembe_bitis.SetText("Perþembe Bitiþ : " + eventtime.ALTIGEN["persembe_bitir"])
			self.cuma_baslangic.SetText("Cuma Baþlangýç : " + eventtime.ALTIGEN["cuma_basla"])
			self.cuma_bitis.SetText("Cuma Bitiþ : " + eventtime.ALTIGEN["cuma_bitir"])
			self.ctesi_baslangic.SetText("Cumartesi Baþlangýç : " + eventtime.ALTIGEN["ctesi_basla"])
			self.ctesi_bitis.SetText("Cumartesi Bitiþ : " + eventtime.ALTIGEN["ctesi_bitir"])
			self.pazar_baslangic.SetText("Pazar Baþlangýç : " + eventtime.ALTIGEN["pazar_basla"])
			self.pazar_bitis.SetText("Pazar Bitiþ : " + eventtime.ALTIGEN["pazar_bitir"])


	def Destroy(self):
		self.ClearDictionary()
		self.board = None

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

