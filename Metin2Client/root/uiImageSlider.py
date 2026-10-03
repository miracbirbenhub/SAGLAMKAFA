import ui, app, grp

SLIDER_COOLDOWN = 1 # cooldown between images in sec

SLIDER_IMAGES = [
	"d:/ymir work/ui/slider/b1.tga",
	"d:/ymir work/ui/slider/b2.tga",
]

class ImageSlider(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)

		self.logs = []

		self.AddFlag("float")
		self.AddFlag("movable")
		self.SetSize(729, 400)
		self.SetCenterPosition()
		self.SetTitleName("Metin2 ImageSlider")
		self.SetCloseEvent(ui.__mem_func__(self.Hide))
		self.Show()

		self.imageSlider = Slider()
		self.imageSlider.SetParent(self)
		self.imageSlider.SetSpecialParent(self)
		self.imageSlider.SetSize(715, 198)
		self.imageSlider.SetPosition(7, 30)
		self.imageSlider.Hide()

		for x in xrange(2):
			sliderItem = SliderItem(SLIDER_IMAGES[x])
			sliderItem.SetImageIndex(x)
			self.imageSlider.AppendItem(sliderItem)

		self.button = ui.Button()
		self.button.SetParent(self)
		self.button.SetPosition(0, 300)
		self.button.SetUpVisual("d:/ymir work/ui/public/xLarge_Button_01.sub")
		self.button.SetOverVisual("d:/ymir work/ui/public/xLarge_Button_02.sub")
		self.button.SetDownVisual("d:/ymir work/ui/public/xLarge_Button_03.sub")
		self.button.SetEvent(ui.__mem_func__(self.RuletkaTeest))
		self.button.SetWindowHorizontalAlignCenter()
		self.button.SetText("Test Slider")
		self.button.Show()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def Close(self):
		self.Hide()

	def RuletkaTeest(self):
		self.imageSlider.Show()
		self.imageSlider.RunSlider()



class Slider(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.items = []
		self.selected = None
		self.basePos = 0
		self.itemWidth = 715
		self.itemStep = 0

		self.runSlider = 0
		self.progress = 0.0
		self.cooldown = 0
		self.speed = 0.01

		self.specialParent = None

		self.selectEvent = None

	def SetSpecialParent(self, parent):
		self.specialParent = parent

	def SetSize(self, w, h):
		ui.Window.SetSize(self, w, h)
		self.SetItemWidth(715)

		self.UpdateList()

	def CalcTotalItemWidth(self):
		total_width = 0
		for item in self.items:
			total_width += item.GetWidth()

		return total_width

	def GetSpeed(self):
		if self.progress < 0.8:
			return self.speed
		# elif self.progress < 0.95:
			# return 0.005
		# else:
			# return 0.0014
		else:
			self.speed = max(0.001, self.speed - 0.000275)
			return self.speed

	def SelectItem(self, item):
		self.selected = item

		if self.selectEvent:
			self.selectEvent(item)

	def AppendItem(self, item):
		item.SetParent(self)
		item.SetWidth(self.itemWidth)
		item.Show()
		self.items.append(item)

		self.UpdateList()

	def RemoveItem(self, item):
		item.Hide()

		self.items.remove(item)
		self.UpdateList()

	def ClearItems(self):
		map(lambda wnd: wnd.Hide(), self.items)
		del self.items[:]

		self.basePos = 0
		self.UpdateList()

	def UpdateList(self):
		toscr = self.CalcTotalItemWidth() - self.GetWidth()
		self.basePos = toscr * self.progress

		self.RecalcItemPositions()

	def UpdatePosition(self):
		toscr = self.CalcTotalItemWidth() - self.GetWidth()
		self.basePos = toscr * self.progress

		self.RecalcItemPositions()

	def IsEmpty(self):
		return len(self.itemList) == 0

	def SetItemWidth(self, w):
		self.itemWidth = w
		for item in self.items:
			item.SetWidth(w)

	def UpdateImages(self):
		newImageIndex = 0 if self.items[1].imageIndex == len(SLIDER_IMAGES) - 1 else self.items[1].imageIndex + 1
		self.items[0].image.LoadImage(SLIDER_IMAGES[self.items[1].imageIndex])
		self.items[0].SetImageIndex(self.items[1].imageIndex)

		self.items[1].image.LoadImage(SLIDER_IMAGES[newImageIndex])
		self.items[1].SetImageIndex(newImageIndex)

		self.progress = 0.0
		self.speed = 0.01
		self.UpdateList()

	def RecalcItemPositions(self):
		curbp = self.basePos

		itemheight = self.CalcTotalItemWidth()
		myheight = self.GetWidth() - 2 * self.itemStep

		if itemheight < myheight:
			curbp = 0

		fromPos = curbp
		curPos = 0
		toPos = curbp + self.GetWidth()
		for item in self.items:
			hw = item.GetWidth()
			if curPos + hw < fromPos:
				item.Hide()
			elif curPos < fromPos and curPos + hw > fromPos:
				item.SetRenderMin(fromPos - curPos)
				item.Show()
			elif curPos < toPos and curPos + hw > toPos:
				item.SetRenderMax(toPos - curPos)
				item.Show()
			elif curPos >= toPos:
				item.Hide()
			else:
				item.Show()

			item.SetPosition(curPos - fromPos, 0)
			curPos += hw + self.itemStep

	def AppendLogText(self, text):
		if self.specialParent:
			textLine = ui.TextLine()
			textLine.SetParent(self.specialParent)
			textLine.SetPosition(15, 260 + 13 * len(self.specialParent.logs))
			textLine.SetText(text)
			textLine.Show()

			self.specialParent.logs.append(textLine)

	def RunSlider(self):
		self.progress = 0.0
		self.runSlider = 1
		self.cooldown = app.GetTime() + SLIDER_COOLDOWN

	def OnUpdate(self):
		if self.runSlider:
			if self.cooldown and self.cooldown < app.GetTime():
				self.progress = min(self.progress + self.GetSpeed(), 1.0)
				self.UpdateList()

				if self.progress == 1.0:
					self.cooldown = app.GetTime() + SLIDER_COOLDOWN
					self.UpdateImages()


class NewSliderItem(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.width = 0
		self.height = 0
		self.minh = 0
		self.maxh = 0

		self.imageIndex = 0
		self.specialParent = None

		self.components = []

	def __del__(self):
		ui.Window.__del__(self)

	def SetColor(self, color=0xff0099ff):
		self.color = color

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)
		self.specialParent = parent

	def SetHeight(self, h):
		self.SetSize(self.width, h)

	def SetImageIndex(self, index):
		self.imageIndex = index

	def SetWidth(self, w):
		self.SetSize(w, self.height)

	def SetSize(self, w, h):
		self.width = w
		self.height = h
		self.maxh = w
		ui.Window.SetSize(self, w, h)

	def SetRenderMin(self, minh):
		self.minh = minh
		self.maxh = self.width
		self.RecalculateRenderedComponents()

	def SetRenderMax(self, maxh):
		self.maxh = maxh
		self.minh = 0
		self.RecalculateRenderedComponents()

	def RegisterComponent(self, component):
		mtype = type(component).__name__
		if mtype == "Bar":
			(x, y, w, h) = component.GetRect()
			(x, y) = component.GetLocalPosition()
			component.__list_data = [x, y, w, h]
		self.components.append(component)

	def UnregisterComponent(self, component):
		self.components.remove(component)

	def RecalculateRenderedComponents(self):
		index = 0
		for component in self.components:
			(xl, yl) = component.GetLocalPosition()
			(x, y, w, h) = component.GetRect()
			mtype = type(component).__name__

			if xl + w < self.minh:
				component.Hide()
			elif xl > self.maxh:
				component.Hide()
			else:
				if mtype == "ExpandedImageBox":

					miny = 0
					if self.minh > 0 and xl < self.minh:
						miny = float(self.minh - xl) / float(w)

					maxy = 0
					if w != 0:
						maxy = float(self.maxh - xl - w) / float(w)

					maxy = min(0, max(-1, maxy))

					component.SetRenderingRect(-miny, 0.0, maxy, 0.0)
					component.Show()

				else:
					if xl < self.minh or xl + h > self.maxh:
						component.Hide()
					else:
						component.Show()

			index += 1

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		grp.SetColor(self.color)
		grp.RenderBar(x + self.minh, y, self.maxh - self.minh, self.GetHeight())


class SliderItem(NewSliderItem):
	def __init__(self, image):
		NewSliderItem.__init__(self)

		self.image = ui.ExpandedImageBox()
		self.image.SetParent(self)
		self.image.SetPosition(0, 0)
		self.image.LoadImage(image)
		self.image.Show()

		self.RegisterComponent(self.image)

		self.SetColor(0x70000000)

		self.SetSize(715, 198)

	def __del__(self):
		NewSliderItem.__del__(self)
