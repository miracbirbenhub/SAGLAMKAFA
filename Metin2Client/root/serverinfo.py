SERVER_1	= "Sancak2"
SERVER_2	= "Sancak2 - Test"
SERVER_IP	= "193.17.4.232"
SERVER_IP2	= "192.168.1.176"
CH_1_NAME	= "CH1"
CH_2_NAME	= "CH2"
CH_3_NAME	= "CH3"
CH_4_NAME	= "CH4"
CH_1		= 12002
CH_2 		= 12102
CH_3 		= 12202
CH_4 		= 12302
CH_5 		= 12302
CH_6 		= 12302
AUTH 		= 11002
MARKADDR	= 12002

#MiniMap Social Butons
SERVER_DC = "https://discord.gg/Sancak2" #Buraya Discord Linkinizi Yazın
SERVER_DC2 = "https://www.facebook.com/Sancak2"  #Buraya Facebook Linkinizi Yazın

SERVER_DC3 = "https://www.tiktok.com/@vevobilisim/" #Buraya Tiktok Linkinizi Yazın
SERVER_DC4 = "https://www.instagram.com/vevobilisim" #Buraya Instagram Linkinizi Yazın
SERVER_DC5 = "https://www.youtube.com/vevobilisim" #Buraya Youtube Linkinizi Yazın
#MiniMap Social Butons

STATE_NONE = "KAPALI"
					
STATE_DICT = {
	0 : "....",
	1 : "NORM",
	2 : "BUSY",
	3 : "FULL"
}

SERVER01_CHANNEL_DICT = {
	1:{"key":11,"name":CH_1_NAME,"ip":SERVER_IP,"tcp_port":CH_1,"udp_port":CH_1,"state":STATE_NONE,},
	2:{"key":12,"name":CH_2_NAME,"ip":SERVER_IP,"tcp_port":CH_2,"udp_port":CH_2,"state":STATE_NONE,},
	3:{"key":13,"name":CH_3_NAME,"ip":SERVER_IP,"tcp_port":CH_3,"udp_port":CH_3,"state":STATE_NONE,},
	4:{"key":14,"name":CH_4_NAME,"ip":SERVER_IP,"tcp_port":CH_4,"udp_port":CH_4,"state":STATE_NONE,},
}
SERVER02_CHANNEL_DICT = {
	1:{"key":11,"name":CH_1_NAME,"ip":SERVER_IP,"tcp_port":CH_1,"udp_port":CH_1,"state":STATE_NONE,},
	2:{"key":12,"name":CH_2_NAME,"ip":SERVER_IP,"tcp_port":CH_2,"udp_port":CH_2,"state":STATE_NONE,},
	3:{"key":13,"name":CH_3_NAME,"ip":SERVER_IP,"tcp_port":CH_3,"udp_port":CH_3,"state":STATE_NONE,},
	4:{"key":14,"name":CH_4_NAME,"ip":SERVER_IP,"tcp_port":CH_4,"udp_port":CH_4,"state":STATE_NONE,},
}

REGION_NAME_DICT = {
	0 : "",		
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SERVER_IP, "port":AUTH, },
		2 : { "ip":SERVER_IP2, "port":AUTH, },

	}		
}

REGION_DICT = {
	0 : {
		1 : { "name" :SERVER_1, "channel" : SERVER01_CHANNEL_DICT, },
		2 : { "name" :SERVER_2, "channel" : SERVER02_CHANNEL_DICT, },
	},
}

MARKADDR_DICT = {
	10 : { "ip" : SERVER_IP, "tcp_port" : MARKADDR, "mark" : "10.tga", "symbol_path" : "10", },
	20 : { "ip" : SERVER_IP2, "tcp_port" : MARKADDR, "mark" : "10.tga", "symbol_path" : "10", },
}