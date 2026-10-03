import ui
import chat
import app
import player
import snd
import item
import net
import game

class BonusBoardDialog(ui.ScriptWindow):
	MaxBoni = { "1": 16000, "2": 320, "3": 32, "4": 32, "5": 32, "6": 32, "7": 16, "9": 40, "10": 60, "11": 60, "12": 16, "13": 24, "14": 16, "15": 30, "16": 30, "17": 50, "18": 100, "19": 100, "20": 100, "21": 100, "22": 100, "23": 20, "24": 40, "27": 15, "28": 30, "29": 72, "30": 72, "31": 72, "32": 72, "33": 72, "34": 72, "35": 60, "36": 60, "37": 40, "38": 60, "39": 20, "41": 10, "43": 60, "44": 60, "45": 40, "48": 1, "53": 50 }
	BonusDict = ["PvP Bonus", "PvM Bonus", "Diðer"]
	BonusIDListe = [["", 0, 0],["Maks HP", 1, 0],["Maks SP", 2, 0],["HP", 3, 0],["Zeka", 4, 0],["Güç", 5, 0],["Çeviklik", 6, 0],["Saldýrý Hýzý", 7, 0],["Hareket Hýzý", 8, 0],["Büyü Hýzý", 9, 0],["HP Üretimi", 10, 32],["SP Üretimi", 11, 33],["Zehirleme Deðiþimi", 12, 37],["Sersemletme Þansý", 13, 38],["Yavaþlatma Þansý", 14, 39],["Kritik Vuruþ Þansý", 15, 40],["Delici Vuruþ Þansý", 16, 41],["Yarý Ýnsanlara Karþý Güçlü", 17, 43],["Hayvanlara Karþý Güçlü", 18, 44],["Orklara Karþý Güçlü", 19, 45],["Mistiklere Karþý Güçlü", 20, 46],["Ölümsüzlere Karþý Güçlü", 21, 47],["Þeytanlara Karþý Güçlü", 22, 48],["HP Emilimi", 23, 63],["SP Emilimi", 24, 64],["SP Çalma", 25, 65],["Vuruþ Ýle SP Çalma", 26, 66],["Beden Karþýsý Ataklarý Bloklama", 27, 67],["Oklardan Korunma Þansý", 28, 68],["Kýlýç Savunmasý", 29, 69],["Çift El Savunmasý", 30, 70],["Býçak Savunmasý", 31, 71],["Çan Savunmasý", 32, 72],["Yelpaze Savunmasý", 33, 73],["Okdan Korunma Þansý", 34, 74],["Ateþe Karþý Dayanýklýlýk", 35, 75],["Þimþeðe Karþý Dayanýklýlýk", 36, 76],["Büyüye Karþý Dayanýklýlýk", 37, 77],["Rüzgara Karþý Dayanýklýlýk", 38, 78],["Vücut Darbelerini Yansýtma", 39, 79],["Lanet Yansýtmasý", 40, 80],["Zehire Karþý Koyma", 41, 81],["SP Yükselmesi Deðiþimi", 42, 82],["Exp-Bonus", 43, 83],["Yang-Drop", 44, 84],["Item-Drop", 45, 85],["Ýksir Etkisi Yükseltme", 46, 86],["HP Yükselmesi Deðiþti", 47, 87],["Sersemlik Karþýsýnda Baðýþýklýk", 48, 88],["Yavaþlýk Karþýsýnda Baðýþýklýk", 49, 89],["Yere Düþme Karþýsýnda Baðýþýklýk", 50, 90],["APPLY_SKILL", 51, 0],["Yay Menzili", 52, 95],["Saldýrý Deðeri", 53, 0],["Savunma", 54, 96],["Büyülü Saldýrý Deðeri", 55, 97],["Büyü Savunmasý", 56, 98],["", 57, 0],["Maks. Dayanýklýk", 58, 0],["Savaþçýlara Karþý Güçlü", 59, 54],["Ninjalara Karþý Güçlü", 60, 55],["Suralara Karþý Güçlü", 61, 56],["Þamanlara Karþý Güçlü", 62, 57],["Canavarlara Karþý Güçlü", 63, 53],["Saldýrý", 64, 114],["Savunma", 65, 115],["Itemshop Exp-Bonus", 66, 116],["Itemshop Item-Bonus", 67, 117],["Itemshop Yang-Bonus", 68, 118],["APPLY_MAX_HP_PCT", 69, 119],["APPLY_MAX_SP_PCT", 70, 120],["Beceri Hasarý", 71, 121],["Ortalama Hasar", 72, 122],["Beceri Hasarýna Direniþ", 73, 123],["Ortalama Hasara Direniþ", 74, 124],["", 75, 0],["iCafe EXP-Bonus", 76, 125],["iCafe Item-Bonus", 77, 126],["Savaþçý Saldýrýlarýna Savunma", 78, 59],["Ninja Saldýrýlarýna Savunma", 79, 60],["Sura Saldýrýlarýna Savunma", 80, 61],["Þaman Saldýrýlarýna Savunma", 81, 62]]
	SpecialBoni = { 1: "Norm.State", 2: "Norm.State", 3: "Norm.State", 4: "Norm.State", 5: "Norm.State", 6: "Norm.State", 55: "Norm.State", 56: "Norm.State", 58: "Norm.State" }
	PvPOffenseBoni = ["Yarý Ýnsanlara Karþý Güçlü", "Kritik Vuruþ Þansý", "Delici Vuruþ Þansý", "Ortalama Hasar", "Beceri Hasarý", "HP", "Zeka", "Güç", "Çeviklik", "Büyü Hýzý"]
	PvPDefenseBoni = ["Kýlýç Savunmasý", "Çift El Savunmasý", "Býçak Savunmasý", "Çan Savunmasý", "Yelpaze Savunmasý", "Okdan Korunma Þansý", "Oklardan Korunma Þansý", "Büyüye Karþý Dayanýklýlýk", "Beden Karþýsý Ataklarý Bloklama", "Sersemlik Karþýsýnda Baðýþýklýk"]
	PvMOffenseBoni = ["Canavarlara Karþý Güçlü", "Þeytanlara Karþý Güçlü", "Ölümsüzlere Karþý Güçlü", "Hayvanlara Karþý Güçlü", "Orklara Karþý Güçlü", "Mistiklere Karþý Güçlü", "Sersemletme Þansý", "Zehirleme Deðiþimi", "Saldýrý Hýzý", "Saldýrý Deðeri"]
	PvMDefenseBoni = ["Maks HP", "Maks SP", "Beden Karþýsý Ataklarý Bloklama", "HP Üretimi", "SP Üretimi", "HP Emilimi", "SP Emilimi", "Exp-Bonus", "Yang-Drop", "Item-Drop"]
	LeftoversOffenseBoni = ["Savaþçýlara Karþý Güçlü", "Ninjalara Karþý Güçlü", "Suralara Karþý Güçlü", "Þamanlara Karþý Güçlü"]
	LeftoversDefenseBoni = ["Savaþçý Saldýrýlarýna Savunma", "Ninja Saldýrýlarýna Savunma", "Sura Saldýrýlarýna Savunma", "Þaman Saldýrýlarýna Savunma", ]

	BonusList = []
	UI = []
	
	TestSystem = 0
	ProcessTimeStamp = 0
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadUI()
		game.BPisLoaded = 1
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Board.Hide()
		game.BPisLoaded = 0

	def LoadUI(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(343, 418)
		self.Board.SetCenterPosition()
		self.Board.AddFlag("movable")
		self.Board.AddFlag("float")
		self.Board.SetTitleName("Efsun Tablosu")
		self.Board.SetCloseEvent(self.__del__)
		self.Board.Show()
		
		Vertical = ui.Line()
		Vertical.SetParent(self.Board)
		Vertical.SetPosition(23, 60)
		Vertical.SetSize(298, 0)
		Vertical.SetColor(0xff777777)
		Vertical.Show()
		self.UI.append(Vertical)
		
		x = 25
		for i in xrange(3):
			ChangeBonusDict = ui.Button()
			ChangeBonusDict.SetParent(self.Board)
			ChangeBonusDict.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			ChangeBonusDict.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			ChangeBonusDict.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			ChangeBonusDict.SetText(self.BonusDict[i])
			ChangeBonusDict.SetPosition(x, 380)
			ChangeBonusDict.SetEvent(lambda arg = ChangeBonusDict.GetText(): self.ChangeBonusDict(arg))
			ChangeBonusDict.Show()
			x += 97
			self.UI.append(ChangeBonusDict)
			
		x = 50
		Type = ["Saldýrý", "Defans"]
		for i in xrange(2):
			BonusDescription = ui.TextLine()
			BonusDescription.SetParent(self.Board)
			BonusDescription.SetPosition(x, 35)
			BonusDescription.SetText(str(Type[i]))
			BonusDescription.SetFontColor(4.0, 0.83, 0)
			BonusDescription.Show()			
			x += 150
			self.UI.append(BonusDescription)

		self.SetBoni(self.BonusDict[0])
		self.dict = self.BonusDict[0]
		
	def SetBoni(self, type):
		Offense = [[25, 70], [25, 100], [25, 130], [25, 160], [25, 190], [25, 220], [25, 250], [25, 280], [25, 310], [25, 340]]
		Defense = [[170, 70], [170, 100], [170, 130], [170, 160], [170, 190], [170, 220], [170, 250], [170, 280], [170, 310], [170, 340]]
		for bonus in self.BonusIDListe:
			if type == self.BonusDict[0]:
				self.CheckBonus(bonus, self.PvPOffenseBoni, Offense)
				self.CheckBonus(bonus, self.PvPDefenseBoni, Defense)
			elif type == self.BonusDict[1]:
				self.CheckBonus(bonus, self.PvMOffenseBoni, Offense)
				self.CheckBonus(bonus, self.PvMDefenseBoni, Defense)
			elif type == self.BonusDict[2]:
				self.CheckBonus(bonus, self.LeftoversOffenseBoni, Offense)
				self.CheckBonus(bonus, self.LeftoversDefenseBoni, Defense)
			else:
				return
				
	def CheckBonus(self, bonus, bonuslist, offset):
		for boni in bonuslist:
			if bonus[0] == boni:
				try:
					Index = bonuslist.index(boni)
					BonusDescription = ui.TextLine()
					BonusDescription.SetParent(self.Board)
					BonusDescription.SetPosition(offset[Index][0], offset[Index][1])
					BonusDescription.SetText(str(bonus[0]))
					BonusDescription.Show()
					
					BonusSlotBar = ui.SlotBar()
					BonusSlotBar.SetParent(self.Board)
					BonusSlotBar.SetSize(125, 15)
					BonusSlotBar.SetPosition(offset[Index][0], offset[Index][1] + 15)
					BonusSlotBar.Show()
					
					BonusAttrLine = ui.TextLine()
					BonusAttrLine.SetParent(self.Board)
					BonusAttrLine.SetPosition(offset[Index][0] + 5, offset[Index][1] + 15)
					
					try:
						Type = self.SpecialBoni[bonus[1]]
						Attribute = self.EquipAttribute(bonus)
					except:
						Attribute = player.GetStatus(int(bonus[2]))
					if self.TestSystem != 1:
						BonusAttrLine.SetText(str(Attribute))
						try:
							if int(Attribute) >= int(self.MaxBoni[str(bonus[1])]):
								BonusAttrLine.SetFontColor(1.0, 0.63, 0)
							else:
								BonusAttrLine.SetFontColor(1, 1, 1)
						except:
							BonusAttrLine.SetFontColor(1, 1, 1)
					else:
						BonusAttrLine.SetText("Test system is active")
						BonusAttrLine.SetFontColor(0.1, 0.7, 1.0)
					
					BonusAttrLine.Show()
					self.BonusList.append([BonusDescription, BonusAttrLine, BonusSlotBar])
				except:
					pass		
				
	def EquipAttribute(self, bonus):
		value = 0
		for slot in xrange(90, 101):
			for attr in xrange(0, 7):
				attr, val = player.GetItemAttribute(slot, attr)
				if int(attr) == bonus[1]:
					value += int(val)
		return int(value)

	def ChangeBonusDict(self, dict):
		self.dict = dict
		for bonus in self.BonusList:
			try:
				for array in bonus:
					array.Hide()
			except:
				pass			
		self.SetBoni(dict)
		
	def OnUpdate(self):
		import item
		if int(app.GetTime()) > int(self.ProcessTimeStamp) + 6:
			self.SetBoni(self.dict)
			self.ProcessTimeStamp = app.GetTime()

#BonusBoardDialog().Show()
