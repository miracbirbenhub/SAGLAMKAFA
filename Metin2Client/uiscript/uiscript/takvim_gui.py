import uiScriptLocale

#ROOT_PATH = "d:/ymir work/ui/game/myshop_deco/" # button_1.tga
ROOT_PATH = "felix_event/"
Baslangic = 11
Bitis = 33

window = {
	"name" : "FelixEventTakvimiPenceresi",
	"x" : (SCREEN_WIDTH -518) / 2,
	"y" : (SCREEN_HEIGHT - 380) / 2,
	"style" : ("movable","float",),
	"width" : 618-80 + 131,
	"height" : 380,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 618-80 + 131,
			"height" : 380+25,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 603-80 + 131,
					"color" : "yellow",
					
					"children" :
					(
						{ "name":"title_name_old", "type":"text", "x":0, "y":-1, "text": "Event Takvimi", "all_align":"center" },
					),
				},
				
				{
					"name" : "ScrollBar",
					"type" : "image",

					"x" : 13,
					"y" : 35,

					"image" : "felix_event/scroll.tga",
				},

				## menu_list bg
				{
					"name" : "menu_list",
					"type" : "thinboard",

					"x" : 14 + 20,
					"y" : 36,

					"width" : 299,
					"height" : 326+25,

					"children" :
					(
						{
							"name" : "title_image",
							"type" : "image",
							"x" : 0,
							"y" : -1,
							"image" : "felix_event/ustt.tga",
							"children" :
							(
								{ "name":"title_events", "type":"text", "x":0, "y":-1, "text": "Event Seçenekleri", "all_align":"center" },
							),
						},
						{ 
							"name" : "btnayisik", "type" : "button", "x" : 5, "y" : 40 - 15, 
							
							"text"	:	"GM Kayboldu Etkinliði",
							
							"default_image" : "d:/ymir work/ui/game/mailbox/post_default.sub",
							"over_image" : "d:/ymir work/ui/game/mailbox/post_over.sub",
							"down_image" : "d:/ymir work/ui/game/mailbox/post_select.sub",
							
							"children" : 
							(
								{
									"name" : "item_slot_1",
									"type" : "image",
									"x" : 0,
									"y" : 0,
									"image" : "d:/ymir work/ui/public/Slot_Base.sub",
									"children" :
									(
										{
											"name" : "item_ay_isik",
											"type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "icon/item/jov.tga",
										},
									),
								},
							),
						},
						
						{ 
							"name" : "btnfutbol", "type" : "button", "x" : 5, "y" : 80 - 15, 
							
							"text"	:	"GM Soru Etkinliði",
							
							"default_image" : "d:/ymir work/ui/game/mailbox/post_default.sub",
							"over_image" : "d:/ymir work/ui/game/mailbox/post_over.sub",
							"down_image" : "d:/ymir work/ui/game/mailbox/post_select.sub", 
							
							"children" : 
							(
								{
									"name" : "item_slot_1",
									"type" : "image",
									"x" : 0,
									"y" : 0,
									"image" : "d:/ymir work/ui/public/Slot_Base.sub",
									"children" :
									(
										{
											"name" : "item_futboltopu",
											"type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "icon/item/jov.tga",
										},
									),
								},
							),
						},
						
						{ 
							"name" : "btnbulmaca", "type" : "button", "x" : 5, "y" : 120 - 15, 
							
							"text"	:	"OX Etkinliði",
							
							"default_image" : "d:/ymir work/ui/game/mailbox/post_default.sub",
							"over_image" : "d:/ymir work/ui/game/mailbox/post_over.sub",
							"down_image" : "d:/ymir work/ui/game/mailbox/post_select.sub", 
							
							"children" : 
							(
								{
									"name" : "item_slot_1",
									"type" : "image",
									"x" : 0,
									"y" : 0,
									"image" : "d:/ymir work/ui/public/Slot_Base.sub",
									"children" :
									(
										{
											"name" : "item_bulmaca",
											"type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "icon/item/fove.tga",
										},
									),
								},
							),
						},
						
						{ 
							"name" : "btnokeykart", "type" : "button", "x" : 5, "y" : 160 - 15, 
							
							"text"	:	"Ronar Etkinliði",
							
							"default_image" : "d:/ymir work/ui/game/mailbox/post_default.sub",
							"over_image" : "d:/ymir work/ui/game/mailbox/post_over.sub",
							"down_image" : "d:/ymir work/ui/game/mailbox/post_select.sub", 
							
							"children" : 
							(
								{
									"name" : "item_slot_1",
									"type" : "image",
									"x" : 0,
									"y" : 0,
									"image" : "d:/ymir work/ui/public/Slot_Base.sub",
									"children" :
									(
										{
											"name" : "item_okey",
											"type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "icon/item/fove.tga",
										},
									),
								},
							),
						},
						
						{ 
							"name" : "btnexp", "type" : "button", "x" : 5, "y" : 200 - 15, 
							
							"text"	:	"Bireysel Trnuva Etkinliði",
							
							"default_image" : "d:/ymir work/ui/game/mailbox/post_default.sub",
							"over_image" : "d:/ymir work/ui/game/mailbox/post_over.sub",
							"down_image" : "d:/ymir work/ui/game/mailbox/post_select.sub", 
							
							"children" : 
							(
								{
									"name" : "item_slot_1",
									"type" : "image",
									"x" : 0,
									"y" : 0,
									"image" : "d:/ymir work/ui/public/Slot_Base.sub",
									
									"children" :
									(
										{
											"name" : "item_exp",
											"type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "icon/item/trnuva.tga",
										},
									),
								},
							),
						},
						
						{ 
							"name" : "btnaltigen", "type" : "button", "x" : 5, "y" : 240 - 15, 
							
							"text"	:	"Lonca Trnuva Etkinliði",
							
							"default_image" : "d:/ymir work/ui/game/mailbox/post_default.sub",
							"over_image" : "d:/ymir work/ui/game/mailbox/post_over.sub",
							"down_image" : "d:/ymir work/ui/game/mailbox/post_select.sub", 
							
							"children" : 
							(
								{
									"name" : "item_slot_1",
									"type" : "image",
									"x" : 0,
									"y" : 0,
									"image" : "d:/ymir work/ui/public/Slot_Base.sub",
									"children" :
									(
										{
											"name" : "item_altigen",
											"type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "icon/item/trnuva.tga",
										},
									),
								},
							),
						},

					),
				},

				{
					"name" : "time_window",
					"type" : "thinboard",

					"x" : 191 + 7 + 135,
					"y" : 36,

					"width" : 190*2 - 54,
					"height" : 326 + 25,
					
					"children" :
					(
						{
							"name": "pazartesi_eventleri",
							"type" : "image",
							"image" : "felix_event/time.tga",
							
							"x" : 4,
							"y" : -1,
							
							"children" :
							(
								{ "name" : "pazartesi_baslangicc", "type" : "text", "x" : 60, "y" : Baslangic, "text" : "", },
								{ "name" : "pazartesi_bitiss", "type" : "text", "x" : 60, "y" : Bitis, "text" : "", },	
							),
						},
						
						{
							"name": "sali_eventleri",
							"type" : "image",
							"image" : "felix_event/time.tga",
							
							"x" : 4,
							"y" : 48,
							
							"children" :
							(
								{ "name" : "sali_baslangicc", "type" : "text", "x" : 60, "y" : Baslangic, "text" : "", },
								{ "name" : "sali_bitiss", "type" : "text", "x" : 60, "y" : Bitis, "text" : "", },	
							),
						},	
						
						{
							"name": "carsamba_eventleri",
							"type" : "image",
							"image" : "felix_event/time.tga",
							
							"x" : 4,
							"y" : 96,
							
							"children" :
							(
								{ "name" : "carsamba_baslangicc", "type" : "text", "x" : 60, "y" : Baslangic, "text" : "", },
								{ "name" : "carsamba_bitiss", "type" : "text", "x" : 60, "y" : Bitis, "text" : "", },	
							),
						},
						
						{
							"name": "persembe_eventleri",
							"type" : "image",
							"image" : "felix_event/time.tga",
							
							"x" : 4,
							"y" : 144,
							
							"children" :
							(
								{ "name" : "persembe_baslangicc", "type" : "text", "x" : 60, "y" : Baslangic, "text" : "", },
								{ "name" : "persembe_bitiss", "type" : "text", "x" : 60, "y" : Bitis, "text" : "", },
							),
						},	
						{
							"name": "cuma_eventleri",
							"type" : "image",
							"image" : "felix_event/time.tga",
							
							"x" : 4,
							"y" : 192,
							
							"children" :
							(
								{ "name" : "cuma_baslangicc", "type" : "text", "x" : 60, "y" : Baslangic, "text" : "", },
								{ "name" : "cuma_bitiss", "type" : "text", "x" : 60, "y" : Bitis, "text" : "", },	
							),
						},	
						{
							"name": "ctesi_eventleri",
							"type" : "image",
							"image" : "felix_event/time.tga",
							
							"x" : 4,
							"y" : 192+48,
							
							"children" :
							(
								{ "name" : "ctesi_baslangicc", "type" : "text", "x" : 60, "y" : Baslangic, "text" : "", },
								{ "name" : "ctesi_bitiss", "type" : "text", "x" : 60, "y" : Bitis, "text" : "", },	
							),
						},	
							
						{
							"name": "pazar_eventleri",
							"type" : "image",
							"image" : "felix_event/time.tga",
							
							"x" : 4,
							"y" : 192+48+48,
							
							"children" :
							(	
								{ "name" : "pazar_baslangicc", "type" : "text", "x" : 60, "y" : Baslangic, "text" : "", },
								{ "name" : "pazar_bitiss", "type" : "text", "x" : 60, "y" : Bitis, "text" : "", },
							),
						},
					),
				},	
			),
		},
	),
}