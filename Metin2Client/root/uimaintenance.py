import ui, wndMgr, time, app, locale, chat, constInfo

pText_x = 65
pText_y = 5 

def pTableTranslate(i):
	pTextColor = (
					"|cFFf2e2bc|H|h", "|cFFc9ff00|H|h", "|cFF0080FF|H|h", "|cFF80f076|H|h")
	translate = {
					1	:	pTextColor[0] + "Bakýma kalan süre: " + pTextColor[3] + "[%s]",
					2	:	pTextColor[1] + "Bakým süresi:        " + pTextColor[3] + "[%s]",
					3	:	pTextColor[2] + "Bakým nedeni:      " + pTextColor[3] + "[%s]",
					4	:	pTextColor[2] + "Bakým nedeni:      " + pTextColor[3] + "[Yok!]",
					5	:	" Gün",
					6	:	" Saat",
					7	:	" Dakika",
				}

	if translate.has_key(i):
		return translate[i]

global_t = (0,24,60)

def CalculateTimeLeft(iTime):
	A, B = divmod(iTime, global_t[2])
	C, A = divmod(A, global_t[2])
	return "%02d:%02d:%02d" % (C, A, B)	

def CalculateDuration(iDuration):
	if iDuration < global_t[2]:
		return "0" + (pTableTranslate(7))

	pMin = int((iDuration / global_t[2]) % global_t[2])
	pHour = int((iDuration / global_t[2]) / global_t[2]) % global_t[1]
	pDay = int(int((iDuration / global_t[2]) / global_t[2]) / global_t[1])

	iText = ""
	if pDay > global_t[0]:
		iText += str(pDay) + (pTableTranslate(5))
		iText += " "
	if pHour > global_t[0]:
		iText += str(pHour) + (pTableTranslate(6))
		iText += " "
	if pMin > global_t[0]:
		iText += str(pMin) + (pTableTranslate(7))

	return iText

class MaintenanceClass(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self)
		self.AddFlag("float")
		
		self.sLogo = ui.AniImageBox()
		self.sTime = ui.TextLine()
		self.sDuration = ui.TextLine()
		self.sReason = ui.TextLine()

		self.sTime.SetPosition(pText_x - 30, pText_y)
		self.sDuration.SetPosition(pText_x - 30, pText_y + 15)
		self.sReason.SetPosition(pText_x - 30, pText_y + 29)

		pWindow = [self.sTime,self.sDuration,self.sReason]
		pLogo = [self.sLogo]

		for i in pWindow:
			i.SetFontName("Tahoma:15")
			i.SetParent(self)
			i.Show()

		for i in pLogo:
			i.SetParent(self)
			i.Show()
			i.SetDelay(4.5)
			i.AppendImage("maintenance/pc_1.tga")
			i.AppendImage("maintenance/pc_2.tga")
			i.AppendImage("maintenance/pc_3.tga")
			i.AppendImage("maintenance/pc_4.tga")
			i.SetPosition(367, 3)
			i.SetSize(32, 55)

		self.SetPosition(wndMgr.GetScreenWidth()/2 - 420/2, 2)
		self.SetSize(420, 55) 

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def SetTime(self, iLeft):
		timeLeft = iLeft - app.GetGlobalTimeStamp()
		if timeLeft < 0:
			timeLeft = 0 
			self.Hide()

		self.sTime.SetText((pTableTranslate(1) % (CalculateTimeLeft(timeLeft))))

	def OpenMaintenance(self, iTime, iDuration, iReason):
		self.leftTime = app.GetGlobalTimeStamp() + int(iTime)
		self.sDuration.SetText((pTableTranslate(2) % (CalculateDuration(int(iDuration)))))

		if str(iReason) != "no_reason":
			self.sReason.SetText((pTableTranslate(3) % (str(iReason).replace("//"," "))))
		else:
			self.sReason.SetText((pTableTranslate(4)))

		self.Show()

	def OnUpdate(self):
		self.SetTime(int(self.leftTime))

	def Close(self):
		self.Hide()
