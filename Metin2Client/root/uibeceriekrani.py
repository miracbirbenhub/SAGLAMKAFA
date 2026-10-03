import ui
import item
import net
import mouseModule
import player
import constInfo

class BeceriEkrani(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Ekran()

	def __Ekran(self):
		KygnPyYukle = ui.PythonScriptLoader()
		KygnPyYukle.LoadScriptFile(self, "UIScript/beceriekrani.py")

		KygnObject = self.GetChild
		self.Skill_1 = KygnObject("Skill_1")
		self.Skill_2 = KygnObject("Skill_2")
		self.image = KygnObject("image")

		self.Skill_1.SetEvent(lambda arg=1: self.ButtonEvent(arg))
		self.Skill_2.SetEvent(lambda arg=2: self.ButtonEvent(arg))
		
		skill_1_Text = self.GetChild("Skill_1_Text")
		skill_1_Text.SetFontName("Tahoma:13")
		skill_1_Text.SetPackedFontColor(0xffF8BF24)
		self.skill_1_Text = skill_1_Text
		
		skill_2_Text = self.GetChild("Skill_2_Text")
		skill_2_Text.SetFontName("Tahoma:13")
		skill_2_Text.SetPackedFontColor(0xffF8BF24)
		self.skill_2_Text = skill_2_Text

	def ButtonEvent(self, arg):
		net.SendChatPacket("/select_skill_group %d" % int(arg))
		self.Close()

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Open(self, job):
		if int(job) == 0:
			self.image.LoadImage("autoskill/warrior.tga")
			self.skill_1_Text.SetText("Bedensel Savaþçý ")
			self.skill_2_Text.SetText("Zihinsel Savaþçý ")
			self.ButtonImage(self.Skill_1, "autoskill/accept_btn_0.tga", "autoskill/accept_btn_1.tga", "autoskill/accept_btn_2.tga")
			self.ButtonImage(self.Skill_2, "autoskill/accept_btn_0.tga", "autoskill/accept_btn_1.tga", "autoskill/accept_btn_2.tga")
		elif int(job) == 1:
			self.image.LoadImage("autoskill/assassin.tga")
			self.skill_1_Text.SetText("Yakýn Dövüþ Ninja")
			self.skill_2_Text.SetText("Uzak Dövüþ Ninja")
			self.ButtonImage(self.Skill_1, "autoskill/accept_btn_0.tga", "autoskill/accept_btn_1.tga", "autoskill/accept_btn_2.tga")
			self.ButtonImage(self.Skill_2, "autoskill/accept_btn_0.tga", "autoskill/accept_btn_1.tga", "autoskill/accept_btn_2.tga")
		elif int(job) == 2:
			self.image.LoadImage("autoskill/sura.tga")
			self.skill_1_Text.SetText("Büyülü Silah Sura")
			self.skill_2_Text.SetText("Kara Büyü Sura")
			self.ButtonImage(self.Skill_1, "autoskill/accept_btn_0.tga", "autoskill/accept_btn_1.tga", "autoskill/accept_btn_2.tga")
			self.ButtonImage(self.Skill_2, "autoskill/accept_btn_0.tga", "autoskill/accept_btn_1.tga", "autoskill/accept_btn_2.tga")
		elif int(job) == 3:
			self.image.LoadImage("autoskill/shaman.tga")
			self.skill_1_Text.SetText("Ejderha Gücü Þaman")
			self.skill_2_Text.SetText("Ýyileþtirme Gücü Þaman")
			self.ButtonImage(self.Skill_1, "autoskill/accept_btn_0.tga", "autoskill/accept_btn_1.tga", "autoskill/accept_btn_2.tga")
			self.ButtonImage(self.Skill_2, "autoskill/accept_btn_0.tga", "autoskill/accept_btn_1.tga", "autoskill/accept_btn_2.tga")
		self.Show()

	def ButtonImage(self, button, UpVisual, OverVisual, DownVisual):
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.Hide()
