import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"

TEMPORARY_X = +13
TEXT_TEMPORARY_X = -10
BUTTON_TEMPORARY_X = 5
PVP_X = -10

window = {
	"name" : "SystemOptionDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 305,
	"height" : 295+65+30,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 305,
			"height" : 295+65+30,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 284,
					"color" : "gray",

					"children" :
					(
						{ 
						"name":"titlename", "type":"text", "x":0, "y":3, 
						"horizontal_align":"center", "text_horizontal_align":"center",
						"text": uiScriptLocale.SYSTEMOPTION_TITLE, 
						 },
					),
				},

				{
					"name" : "MusicOptions",
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
						"text": "Ses Seçenekleri", 
						 },
					),
				},
				{
					"name" : "GraphicOptions",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x" : 0,
					"y" : 142,

					"horizontal_align":"center",
					
					"image" : "d:/ymir work/ui/minigame/catchking/challenge_text_bg.sub",

					"children" :
					(
						{ 
						"name":"graphicname", "type":"text", "x":0, "y":3, 
						"horizontal_align":"center", "text_horizontal_align":"center",
						"text": "Görüntü Seçenekleri", 
						 },
					),
				},
				## Music
				{
					"name" : "music_name",
					"type" : "text",

					"x" : 30,
					"y" : 95,

					"text" : uiScriptLocale.OPTION_MUSIC,
				},
				
				{
					"name" : "music_volume_controller",
					"type" : "sliderbar",

					"x" : 110,
					"y" : 95,
				},
				
				{
					"name" : "bgm_button",
					"type" : "button",

					"x" : 20,
					"y" : 115,

					"text" : uiScriptLocale.OPTION_MUSIC_CHANGE,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				
				{
					"name" : "bgm_file",
					"type" : "text",

					"x" : 100,
					"y" : 115,

					"text" : uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
				},
				
				## Sound
				{
					"name" : "sound_name",
					"type" : "text",

					"x" : 30,
					"y" : 70,

					"text" : uiScriptLocale.OPTION_SOUND,
				},
				
				{
					"name" : "sound_volume_controller",
					"type" : "sliderbar",

					"x" : 110,
					"y" : 70,
				},	

				## Ä«¸Þ¶ó
				{
					"name" : "camera_mode",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 172,

					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
				},
				
				{
					"name" : "camera_short",
					"type" : "radio_button",

					"x" : 110,
					"y" : 172,

					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				
				{
					"name" : "camera_long",
					"type" : "radio_button",

					"x" : 110+70,
					"y" : 172,

					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},

				## ¾È°³
				{
					"name" : "fog_mode",
					"type" : "text",

					"x" : 30,
					"y" : 202,

					"text" : uiScriptLocale.OPTION_FOG,
				},
				
				{
					"name" : "fog_level0",
					"type" : "radio_button",

					"x" : 110,
					"y" : 202,

					"text" : uiScriptLocale.OPTION_FOG_DENSE,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "fog_level1",
					"type" : "radio_button",

					"x" : 110+50,
					"y" : 202,

					"text" : uiScriptLocale.OPTION_FOG_MIDDLE,
					
					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "fog_level2",
					"type" : "radio_button",

					"x" : 110 + 100,
					"y" : 202,

					"text" : uiScriptLocale.OPTION_FOG_LIGHT,
					
					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},

				## Å¸ÀÏ °¡¼Ó
				{
					"name" : "tiling_mode",
					"type" : "text",

					"x" : 30,
					"y" : 232,

					"text" : uiScriptLocale.OPTION_TILING,
				},
				
				{
					"name" : "tiling_cpu",
					"type" : "radio_button",

					"x" : 110,
					"y" : 232,

					"text" : uiScriptLocale.OPTION_TILING_CPU,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "tiling_gpu",
					"type" : "radio_button",

					"x" : 158,
					"y" : 232,

					"text" : uiScriptLocale.OPTION_TILING_GPU,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "tiling_apply",
					"type" : "button",

					"x" : 210,
					"y" : 232,

					"text" : uiScriptLocale.OPTION_TILING_APPLY,

					"default_image" : ROOT_PATH + "middle_Button_01.sub",
					"over_image" : ROOT_PATH + "middle_Button_02.sub",
					"down_image" : ROOT_PATH + "middle_Button_03.sub",
				},

				{
					"name" : "font_type_name",
					"type" : "text",

					"x" : 30,
					"y" : 262,

					"text" : "Yazý Tipi",
				},
				
				{
					"name" : "font_type_arial",
					"type" : "radio_button",

					"x" : 110,
					"y" : 262,

					"text" : "Arial",

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "font_type_tahoma",
					"type" : "radio_button",

					"x" : 110+50,
					"y" : 262,

					"text" : "Tahoma",

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "font_type_geneva",
					"type" : "radio_button",

					"x" : 110+100,
					"y" : 262,

					"text" : "Geneva",

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				## ENABLE_FOV_OPTION
				{
					"name" : "fov_option",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 292 + 2,

					"text" : uiScriptLocale.FOV_OPTION,
				},

				{
					"name" : "fov_on",
					"type" : "radio_button",

					"x" : 110,
					"y" : 292,

					"text" : uiScriptLocale.FOV_OPTION_ON,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},

				{
					"name" : "fov_off",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 292,

					"text" : uiScriptLocale.FOV_OPTION_OFF,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				{
					"name" : "shop_mode",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 322,

					"text" : uiScriptLocale.OPTION_SALESTEXT_RANGE,
				},
				{
					"name" : "salestext_range_controller",
					"type" : "sliderbar",

					"x" : 110,
					"y" : 322,
				},
				## END_OF_ENABLE_FOV_OPTION

				## ±×¸²ÀÚ
				{
					"name" : "night_mode",
					"type" : "text",

					"x" : 30,
					"y" : 352,

					"text" : "Gece/Gun Modu",
				},
				
				{
					"name" : "night_on",
					"type" : "radio_button",

					"x" : 110,
					"y" : 352,

					"text" : "Aktif",

					"default_image" : ROOT_PATH + "middle_Button_01.sub",
					"over_image" : ROOT_PATH + "middle_Button_02.sub",
					"down_image" : ROOT_PATH + "middle_Button_03.sub",
				},
				
				{
					"name" : "night_off",
					"type" : "radio_button",

					"x" : 110+70,
					"y" : 352,

					"text" : "Disaktif",
					
					"default_image" : ROOT_PATH + "middle_Button_01.sub",
					"over_image" : ROOT_PATH + "middle_Button_02.sub",
					"down_image" : ROOT_PATH + "middle_Button_03.sub",
				},
			),
		},
	),
}
