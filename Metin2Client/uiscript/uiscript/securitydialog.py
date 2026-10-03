import uiScriptLocale
ROOT_PATH = "d:/ymir work/ui/public/"
window = {
	"name" : "GuvenlikDialog",
	"x" : SCREEN_WIDTH - 355,
	"y" : SCREEN_HEIGHT - 238,
	"style" : ("movable", "float",),
	"width" : 355,
	"height" : 238+38,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : 355,
			"height" : 238+38,
			"children" :
			(
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8,
					"y" : 8,
					"width" : 340,
					"color" : "gray",
					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",
							"x" : 340/2,
							"y" : 3,
							"text" : uiScriptLocale.SECURITY_TITLE,
							"text_horizontal_align":"center"
						},
					),
				},
				
				{
					"name" : "BlackBoard",
					"type" : "thinboard_circle",
					"x" : 13, 
					"y" : 35,
					"width" : 162, 
					"height" : 190,
					"children": 
					(
								
						{
							"name" : "namebg", 
							"type" : "expanded_image",
							"style" : ("attach",),
									
							"x" : 5, 
							"y" : 5, 
									
							"image" : "d:/ymir work/ui/pet/Pet_Incu_001.tga",
									
							"children" :
							(

								{
									"name" : "password_value",
									"type" : "editline",

									"x" : 11,
									"y" : 28,

									"width" : 129,
									"height" : 16,

									"input_limit" : 6,
									"secret_flag" : 1,

									# "text" : "text",
								},
										
								{
									"name" : "Durum",
									"type" : "text",

									"x" : 40,
									"y" : 7,



									"text" : "Güvenlik Þifren",
								},
							),
						},
								
						{
							"name" : "1",
							"type" : "button",
							"x" : 10, 
							"y" : 15+50,
									
							"text" : "1",
							
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
						{
							"name" : "2",
							"type" : "button",
							"x" : 60,  
							"y" : 15+50,
									
							"text" : "2",
									
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
						{
							"name" : "3",
							"type" : "button",
							"x" : 110,  
							"y" : 15+50,
									
							"text" : "3",
								
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
								
								
						{
							"name" : "4",
							"type" : "button",
							"x" : 10, 
							"y" : 45+50,
									
							"text" : "4",
						
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
							
						{
							"name" : "5",
							"type" : "button",
							"x" : 60,  
							"y" : 45+50,
									
							"text" : "5",
									
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
						{
							"name" : "6",
							"type" : "button",
							"x" : 110,  
							"y" : 45+50,
									
							"text" : "6",
							
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
								
						{
							"name" : "7",
							"type" : "button",
							"x" : 10, 
							"y" : 75+50,
									
							"text" : "7",
									
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
						{
							"name" : "8",
							"type" : "button",
							"x" : 60,  
							"y" : 75+50,
									
							"text" : "8",
									
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
						{
							"name" : "9",
							"type" : "button",
							"x" : 110,  
							"y" : 75+50,
									
							"text" : "9",
							
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
						{
							"name" : "0",
							"type" : "button",
							"x" : 10, 
							"y" : 105+50,
									
							"text" : "0",
									
							"default_image" : ROOT_PATH + "small_Button_01.sub",
							"over_image" : ROOT_PATH + "small_Button_02.sub",
							"down_image" : ROOT_PATH + "small_Button_03.sub",
							
						},
								
						{
							"name" : "kapatext",
							"type" : "text",
							"x" : 95, 
							"y" : 107+50,
									
							"text" : "Sistemi Kapa",
									
							
						},
								
						{
							"name" : "sistemikapa",
							"type" : "button",
							"x" : 65,  
							"y" : 105+50,
									
							"text" : "",
									
							"default_image" : "d:/ymir work/interface/checkbox/empty_01_normal.png",
							"over_image" : "d:/ymir work/interface/checkbox/empty_02_hover.png",
							"down_image" : "d:/ymir work/interface/checkbox/empty_03_active.png",
							
						},
							
										
					),
				
				},
						
						
				{
					"name" : "BlackBoard2",
					"type" : "thinboard_circle",
					"x" : 13+167, 
					"y" : 35,
					"width" : 162, 
					"height" : 190,
					"children": 
					(
								
						{
							"name" : "namebg2", 
							"type" : "expanded_image",
							"style" : ("attach",),
									
							"x" : 5, 
							"y" : 5, 
									
							"image" : "d:/ymir work/ui/pet/Pet_Incu_001.tga",
									
							"children" :
							(

								{
									"name" : "security_control",
									"type" : "text",

									"x" : 15,
									"y" : 28,


									# "text" : "text",
								},
										
								{
									"name" : "Durum2",
									"type" : "text",

									"x" : 35,
									"y" : 7,



									"text" : "Güvenlik Durumu",
								},
							),
						},
								
						{
							"name" : "accept_button",
							"type" : "button",
							"x" : 8,
							"y" : 68,
							"text" : uiScriptLocale.OK,
							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
									
								
						},
						
						{
							"name" : "clear_button",
							"type" : "button",
							"x" : 8,
							"y" : 98,
							"text" : "Temizle",
							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
						},
								
						{
							"name" : "cancel_button",
							"type" : "button",
							"x" : 8,
							"y" : 128,
							"text" : uiScriptLocale.CANCEL,
							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
						},
								
						{
							"name" : "remember_button",
							"type" : "button",
							"x" : 8,
							"y" : 128,
							"text" : uiScriptLocale.SECURITY_LOST_PASSWORD,
							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
									
								
						},
								
						{
							"name" : "kapat",
							"type" : "button",
							"x" : 8,
							"y" : 158,
							"text" : "Çýkýþ",
							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
									
						
						},
					),
					
				},
				
				{
					"name" : "BlackBoard3",
					"type" : "thinboard_circle",
					"x" : 13, 
					"y" : 35+194,
					"width" : 162+162+5, 
					"height" : 32,
					"children": 
					(
								
						{
							"name" : "bilgibutton",
							"type" : "text",
							"x" : 8,
							"y" : 7,
							"text" : "Güvenlik þifrelerin depo þifrenle aynýdýr.",

						},

					),
					
				},

				# {
					# "name": "SecurtiyInfoBoard",
					# "type": "thinboard",
					# "x": 15,
					# "y": 35,
					# "width": 246,
					# "height": 116,
					# "children": 
					# (

						
						# {
							# "name" : "info_01",
							# "type" : "text",
							# "x" : 8,
							# "y" : 8,
							# "text" : "Güvenlik sistemi hesabýnýzýn güvenliði için oluþturul-",
							# "text_horizontal_align":"left"
						# },
						# {
							# "name" : "info_02",
							# "type" : "text",
							# "outline" : 1,
							# "x" : 8,
							# "y" : 20,
							# "text" : "-muþ bir sistemdir. Oyuna ilk giriþ yaptýðýnýzda sistem",
							# "text_horizontal_align":"left"
						# },
						# {
							# "name" : "info_03",
							# "type" : "text",
							# "outline" : 1,
							# "x" : 8,
							# "y" : 32,
							# "text" : "sizden altý haneli sadece sayýlardan oluþan bir þifre",
							# "text_horizontal_align":"left"
						# },
						# {
							# "name" : "info_04",
							# "type" : "text",
							# "outline" : 1,
							# "x" : 8,
							# "y" : 44,
							# "text" : "oluþturmanýzý isteyecektir. Þifrenizi oluþturduktan son-",
							# "text_horizontal_align":"left"
						# },
						# {
							# "name" : "info_05",
							# "type" : "text",
							# "outline" : 1,
							# "x" : 8,
							# "y" : 56,
							# "text" : "ra bir yere not ediniz. Hesabýnýz baþkalarý tarafýndan",
							# "text_horizontal_align":"left"
						# },
						# {
							# "name" : "info_06",
							# "type" : "text",
							# "outline" : 1,
							# "x" : 8,
							# "y" : 68,
							# "text" : "ele geçirilirse güvenlik þifresini girilmeden hesabýn",
							# "text_horizontal_align":"left"
						# },
						# {
							# "name" : "info_07",
							# "type" : "text",
							# "outline" : 1,
							# "x" : 8,
							# "y" : 80,
							# "text" : "oynanýþ açýsýndan herhangi bir iþlevi olmayacaktýr.",
							# "text_horizontal_align":"left"
						# },
						# {
							# "name" : "security_control",
							# "type" : "text",
							# "outline" : 1,
							# "x" : 8,
							# "y" : 92,
							# "text" : "",
						# },
					# ),
				# },
				# {
					# "name" : "password_slot",
					# "type" : "slotbar",
					# "x" : 40,
					# "y" : 158,
					# "width" : 150,
					# "height" : 18,
					# "horizontal_align" : "center",
					# "image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
					# "children" :
					# (
						# {
							# "name" : "password_value",
							# "type" : "editline",
							# "x" : 3,
							# "y" : 3,
							# "width" : 100,
							# "height" : 18,
							# "input_limit" : 6,
							# "secret_flag" : 1,
						# },
					# ),
				# },
				# {
					# "name" : "enter_password",
					# "type" : "text",
					# "x" : 18,
					# "y" : 160,
					# "text" : "Güvenlik Þifresi: ",
				# },
				# {
					# "name" : "accept_button",
					# "type" : "button",
					# "x" : 15,
					# "y" : 185,
					# "text" : uiScriptLocale.OK,
					# "horizontal_align" : "left",
					# "default_image" : ROOT_PATH + "large_Button_01.sub",
					# "over_image" : ROOT_PATH + "large_Button_02.sub",
					# "down_image" : ROOT_PATH + "large_Button_03.sub",
				# },
				# {
					# "name" : "cancel_button",
					# "type" : "button",
					# "x" : 0,
					# "y" : 185,
					# "text" : uiScriptLocale.CANCEL,
					# "horizontal_align" : "center",
					# "default_image" : ROOT_PATH + "Middle_Button_01.sub",
					# "over_image" : ROOT_PATH + "Middle_Button_02.sub",
					# "down_image" : ROOT_PATH + "Middle_Button_03.sub",
				# },
				# {
					# "name" : "remember_button",
					# "type" : "button",
					# "x" : 110,
					# "y" : 185,
					# "text" : uiScriptLocale.SECURITY_LOST_PASSWORD,
					# "default_image" : ROOT_PATH + "large_Button_01.sub",
					# "over_image" : ROOT_PATH + "large_Button_02.sub",
					# "down_image" : ROOT_PATH + "large_Button_03.sub",
				# },
				
				# {
					# "name" : "kapat",
					# "type" : "button",
					# "x" : 200,
					# "y" : 185,
					# "text" : "Çýkýþ",
					# "default_image" : ROOT_PATH + "Middle_Button_01.sub",
					# "over_image" : ROOT_PATH + "Middle_Button_02.sub",
					# "down_image" : ROOT_PATH + "Middle_Button_03.sub",
				# },
			),
		},
	),
}