import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"

TEMPORARY_X = +13
BUTTON_TEMPORARY_X = 5
PVP_X = -10

LINE_LABEL_X 	= 30
LINE_DATA_X 	= 90
LINE_STEP	= 0
SMALL_BUTTON_WIDTH 	= 45
MIDDLE_BUTTON_WIDTH 	= 65

window = {
	"name" : "GameOptionDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 360,
	"height" : 25*17+8+10+12+16+18,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 360,
			"height" : 25*17+8+10+12+16+18,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 344,
					"color" : "gray",

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3, 
						"text" : uiScriptLocale.GAMEOPTION_TITLE, 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "BlockedOptions",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x" : 0,
					"y" : 37,
					
					"horizontal_align":"center",
					
					"image" : "d:/ymir work/ui/minigame/catchking/challenge_text_bg.sub",

					"children" :
					(
						{ 
						"name":"musicname", "type":"text", "x":0, "y":3, 
						"horizontal_align":"center", "text_horizontal_align":"center",
						"text": "Engel Seçenekleri", 
						 },
					),
				},
				## ÀÌ¸§»ö
				{
					"name" : "name_color",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 70+2,

					"text" : uiScriptLocale.OPTION_NAME_COLOR,
				},
				{
					"name" : "name_color_normal",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 70,

					"text" : uiScriptLocale.OPTION_NAME_COLOR_NORMAL,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "name_color_empire",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 70,

					"text" : uiScriptLocale.OPTION_NAME_COLOR_EMPIRE,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},

				## Å¸°ÙÃ¢
				{
					"name" : "target_board",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 95+2,

					"text" : uiScriptLocale.OPTION_TARGET_BOARD,
				},
				{
					"name" : "target_board_no_view",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 95,

					"text" : uiScriptLocale.OPTION_TARGET_BOARD_NO_VIEW,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "target_board_view",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 95,

					"text" : uiScriptLocale.OPTION_TARGET_BOARD_VIEW,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},

				
				## PvP Mode
				{
					"name" : "pvp_mode",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 120+2,

					"text" : uiScriptLocale.OPTION_PVPMODE,
				},
				{
					"name" : "pvp_peace",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*0,
					"y" : 120,

					"text" : uiScriptLocale.OPTION_PVPMODE_PEACE,
					"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_PEACE_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "pvp_revenge",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*1,
					"y" : 120,

					"text" : uiScriptLocale.OPTION_PVPMODE_REVENGE,
					"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_REVENGE_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "pvp_guild",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*2,
					"y" : 120,

					"text" : uiScriptLocale.OPTION_PVPMODE_GUILD,
					"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_GUILD_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "pvp_free",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*3,
					"y" : 120,

					"text" : uiScriptLocale.OPTION_PVPMODE_FREE,
					"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_FREE_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},

				## Block
				{
					"name" : "block",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 145+2,

					"text" : uiScriptLocale.OPTION_BLOCK,
				},
				{
					"name" : "block_exchange_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 145,

					"text" : uiScriptLocale.OPTION_BLOCK_EXCHANGE,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_party_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 145,

					"text" : uiScriptLocale.OPTION_BLOCK_PARTY,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_guild_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*2,
					"y" : 145,

					"text" : uiScriptLocale.OPTION_BLOCK_GUILD,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_whisper_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 170,

					"text" : uiScriptLocale.OPTION_BLOCK_WHISPER,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_friend_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 170,

					"text" : uiScriptLocale.OPTION_BLOCK_FRIEND,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "block_party_request_button",
					"type" : "toggle_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*2,
					"y" : 170,

					"text" : uiScriptLocale.OPTION_BLOCK_PARTY_REQUEST,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},

				{
					"name" : "GeneralOptions",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x" : 0,
					"y" : 200,
					
					"horizontal_align":"center",
					
					"image" : "d:/ymir work/ui/minigame/catchking/challenge_text_bg.sub",

					"children" :
					(
						{ 
						"name":"musicname", "type":"text", "x":0, "y":3, 
						"horizontal_align":"center", "text_horizontal_align":"center",
						"text": "Genel Seçenekler", 
						 },
					),
				},
				## Chat
				{
					"name" : "chat",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 235+2,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT,
				},
				{
					"name" : "view_chat_on_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : 235,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT_ON,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "view_chat_off_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 235,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT_OFF,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},

				## Always Show Name
				{
					"name" : "always_show_name",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 260+2,

					"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME,
				},
				{
					"name" : "always_show_name_on_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : 260,

					"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME_ON,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "always_show_name_off_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 260,

					"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME_OFF,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},

				## Effect On/Off
				{
					"name" : "effect_on_off",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 285+2,

					"text" : uiScriptLocale.OPTION_EFFECT,
				},
				{
					"name" : "show_damage_on_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : 285,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT_ON,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "show_damage_off_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 285,

					"text" : uiScriptLocale.OPTION_VIEW_CHAT_OFF,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},

				## ÆÇ¸Å¹®±¸
				{
					"name" : "salestext_on_off",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 310+2,

					"text" : uiScriptLocale.OPTION_SALESTEXT,
				},
				{
					"name" : "salestext_on_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : 310,

					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "salestext_off_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 310,

					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},				
				{
					"name" : "level_on_off",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 335+2,

					"text" : "Level",
				},
				{
					"name" : "showlevel_on_button",
					"type" : "radio_button",
					"x" : LINE_DATA_X,
					"y" : 335,
					"text" : "Göster",
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "showlevel_off_button",
					"type" : "radio_button",
					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 335,
					"text" : "Gizle",
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "textures_mode",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 360+2,

					"text" : "Zemin Stili",
				},
				
				{
					"name" : "texture_classic",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*0,
					"y" : 360,

					"text" : "Orjinal",

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "texture_snow",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*1,
					"y" : 360,

					"text" : "Karlý",

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "texture_desert",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*2,
					"y" : 360,

					"text" : "Çöl",

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "texture_green",
					"type" : "radio_button",

					"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*3,
					"y" : 360,

					"text" : "Eski",

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "item_toplama",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 385+2,

					"text" : "Ýtem Topla",
				},
				{
					"name" : "auto_pick_item_on",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 385,

					"text" : "Aktif",

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "auto_pick_item_off",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 385,

					"text" : "Kapalý",

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
                
				##{
				##	"name" : "yang_toplama",
				##	"type" : "text",
				##
				##	"x" : LINE_LABEL_X,
				##	"y" : 410+2,
				##
				##	"text" : "Yang Toplama",
				##},
				##{
				##	"name" : "auto_pick_yang_on",
				##	"type" : "radio_button",
				##
				##	"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
				##	"y" : 410,
				##
				##	"text" : "Aktif",
				##
				##	"default_image" : ROOT_PATH + "middle_button_01.sub",
				##	"over_image" : ROOT_PATH + "middle_button_02.sub",
				##	"down_image" : ROOT_PATH + "middle_button_03.sub",
				##},
				##{
				##	"name" : "auto_pick_yang_off",
				##	"type" : "radio_button",
				##
				##	"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
				##	"y" : 410,
				##
				##	"text" : "Kapalý",
				##
				##	"default_image" : ROOT_PATH + "middle_button_01.sub",
				##	"over_image" : ROOT_PATH + "middle_button_02.sub",
				##	"down_image" : ROOT_PATH + "middle_button_03.sub",
				##},
				{
					"name" : "yang_drop_on_off",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 435+2,

					# "text" : "Yang Bilgisi",
				},
				{
					"name" : "yangdrop_on_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X,
					"y" : 435,

					# "text" : "Acik",

					# "default_image" : ROOT_PATH + "middle_button_01.sub",
					# "over_image" : ROOT_PATH + "middle_button_02.sub",
					# "down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "yangdrop_off_button",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 435,

					# "text" : "Kapali",

					# "default_image" : ROOT_PATH + "middle_button_01.sub",
					# "over_image" : ROOT_PATH + "middle_button_02.sub",
					# "down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				# {
					# "name" : "block_tec_request_button",
					# "type" : "toggle_button",

					# "x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					# "y" : 455,
					# "tooltip_text" : "Tecrube almayi durdurur.",
					# "text" : "Tecrübe",

					# "default_image" : ROOT_PATH + "middle_button_01.sub",
					# "over_image" : ROOT_PATH + "middle_button_02.sub",
					# "down_image" : ROOT_PATH + "middle_button_03.sub",
				# },				                
				
				{
					"name" : "onizleme",
					"type" : "text",

					"multi_line" : 1,

					"x" : LINE_LABEL_X,
					"y" : 410+2,

					"text" : "Önizleme",
				},

				{
					"name" : "render_on",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
					"y" : 410,

					"text" : "Açýk",

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "render_off",
					"type" : "radio_button",

					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1,
					"y" : 410,

					"text" : "Kapalý",

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "hide_system",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 435+2,

					"text" : "On/Off",
				},
				{
					"name" : "ShowMadaraPetButton",
					"type" : "toggle_button",

					"x" : LINE_DATA_X,
					"y" : 435,

					"text" : "Pet",

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "ShowMadaraMountButton",
					"type" : "toggle_button",
	
					"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,
					"y" : 435,

					"text" : "Binek",

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				## premium
				{
					"name" : "premium_text",
					"type" : "text",

					"x" : LINE_LABEL_X,
					"y" : 463,

					"text" : "Premium Ef",
				},
				{
					"name" : "premium_on",
					"type" : "radio_button",

					"x": 90,
					"y" : 458+2,

					"text" : uiScriptLocale.ACIK,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},
				{
					"name" : "premium_off",
					"type" : "radio_button",

					"x": 155,
					"y" : 458+2,

					"text" : uiScriptLocale.KAPALI,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",
				},

			),
		},
	),
}
