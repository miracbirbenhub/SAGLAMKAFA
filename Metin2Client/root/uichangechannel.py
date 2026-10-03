from ui_wrapper import _ui
import app,net,wndMgr,background
import ui,uicommon,serverinfo

class uichangechannel(ui.Window):
	def __init__(self, stream):
		ui.Window.__init__(self)
		self.stream = stream
		
		self.Board = None
		self.btnChildren = []
		self.serverID = None
		self.channels = None
		self.regionID = None
		
		self.__LoadWindow()
		self.CreateGUI()
	
	def __del__(self):
		ui.Window.__del__(self)
		
	def __LoadWindow(self):
		file = open("channel.inf", "r")
		lines = file.readlines()
		file.close()
		
		if len(lines):
			tokens = lines[0].split()
			self.serverID = int(tokens[0])
			selChannelID = int(tokens[1])
			if len(tokens) == 3:
				self.regionID = int(tokens[2])
			else:
				self.regionID = 0
		
		self.channels = serverinfo.REGION_DICT[self.regionID][self.serverID]["channel"]
	
	def CreateGUI(self):
		self.Board = _ui().BoardWithTitleBar(None, 0, 0, 0, 140, 140, "CH Deðiþtir", self.Close)
		
		for i in xrange(len(self.channels)):
			btn = _ui().Button(self.Board, self.channels[i + 1]["name"], "", 0, 35 + 35*i, lambda arg = i + 1: self.__ChangeChannel(arg), "news/1.tga", "news/2.tga", "news/3.tga")
			btn.SetDisableVisual("news/1.tga")
			btn.SetWindowHorizontalAlignCenter()
			
			# if str(net.GetServerInfo()[-1:]) == str(i + 1):
				# btn.Disable()
			self.btnChildren.append(btn)
		
		self.Board.SetSize(170, len(self.channels) * 45)
		self.Board.SetPosition(wndMgr.GetScreenWidth()/2 - 80, wndMgr.GetScreenHeight() / 2 - (len(self.channels) * 35))
		
	def __ChangeChannel(self, ch):
		
			
		net.SendChatPacket("/kanal "+str(ch))
		self.Close()
		
		# self.stream.channel = ch
		# ip = serverinfo.REGION_DICT[self.regionID][self.serverID]["channel"][ch]["ip"]
		# tcp_port = serverinfo.REGION_DICT[self.regionID][self.serverID]["channel"][ch]["tcp_port"]
		# account_ip = serverinfo.REGION_AUTH_SERVER_DICT[self.regionID][self.serverID]["ip"]
		# account_port = serverinfo.REGION_AUTH_SERVER_DICT[self.regionID][self.serverID]["port"]
		# state = serverinfo.REGION_DICT[self.regionID][self.serverID]["channel"][ch]["state"]
		# slot = self.stream.GetCharacterSlot()
		
		# if state == serverinfo.STATE_NONE:
			# self.Popup = _ui().Popup('CH deðiþtirirken sorun oluþtu!', None, None)
			# return
		# elif state == serverinfo.STATE_DICT[3]:
			# self.Popup = _ui().Popup('CH FULL!', None, None)
			# return
			
		# if self.IsInSpecialMap():
			# self.Popup = _ui().Popup('Bu haritada ch deðiþtiremezsin!', None, None)
			# return

		# self.stream.SetConnectInfo(ip, tcp_port, account_ip, account_port)
		# markKey = self.regionID * 1000 + self.serverID * 10
		# markAddrValue=serverinfo.MARKADDR_DICT[markKey]
		# net.SetMarkServer(markAddrValue["ip"], markAddrValue["tcp_port"])
		# app.SetGuildMarkPath(markAddrValue["mark"])
		# app.SetGuildSymbolPath(markAddrValue["symbol_path"])
		# self.Close()
		
		# file=pack_open("channel.cfg", "w")
		# file.write("%d %d %d" % (self.serverID, ch, self.regionID))
		# file.close()
		# net.SetServerInfo(str(net.GetServerInfo()[:-1]) + str(ch))
		# net.LogOutGame()
		# self.stream.SetLoginInfo(net.ACC_ID, net.ACC_PWD)
		# self.stream.Connect()
		
		# self.stream.SetCharacterSlot(slot)
		# self.stream.isAutoSelect=1
	
	def IsInSpecialMap(self):
		bad_maps = [
			"season1/metin2_map_oxevent", "season2/metin2_map_guild_inside01", "season2/metin2_map_empirewar01",
			"season2/metin2_map_empirewar02", "season2/metin2_map_empirewar03", "metin2_map_empirewar02",
			"metin2_map_dragon_timeattack_01", "metin2_map_dragon_timeattack_02", "metin2_map_dragon_timeattack_03",
			"metin2_map_skipia_dungeon_boss", "metin2_map_skipia_dungeon_boss2", "metin2_map_devilsCatacomb",
			"metin2_map_deviltower1", "metin2_map_t1", "metin2_map_t2", "metin2_map_t3", "metin2_map_t4",
			"metin2_map_t5", "metin2_map_wedding_01", "metin2_map_duel"
		]
		if str(background.GetCurrentMapName()) in bad_maps:
			return True
		return False

	def Show(self):
		self.Board.Show()
	
	def Close(self):
		self.Board.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
