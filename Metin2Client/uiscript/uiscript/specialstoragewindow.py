import uiScriptLocale
import app

window = {
	"name" : "SpecialStorageWindow",

	"x" : SCREEN_WIDTH - 400,
	"y" : 10,

	"style" : ("movable", "float",),

	"width" : 184,
	"height" : 395+32+30,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 184,
			"height" : 395+32+30,

			"children" :
			(
			
				{
						"name" : "SeparateBaseImage",
						"type" : "image",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",

						"children" :
						(
							## Separate Button (38x24)
							{
								"name" : "SeparateButton",
								"type" : "button",

								"x" : 0,
								"y" : 0,

								"tooltip_text" : "Envanteri Düzenle",

								"default_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
								"over_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe_over.tga",
								"down_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe_down.tga",
								"disable_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
							},
						),
					},
			
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8+35,
					"y" : 7,

					"width" : 161-35,
					"color" : "gray",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":60, "y":4, "text":uiScriptLocale.UPGRADE_STORAGE_TITLE, "text_horizontal_align":"center" },
					),
				},

				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},
				
				{
					"name" : "Inventory_Tab_01",
					"type" : "radio_button",

					"x" : 8,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"children" :
					(
						{
							"name" : "Inventory_Tab_01_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "I",
						},
					),
				},
				{
					"name" : "Inventory_Tab_02",
					"type" : "radio_button",

					"x" : 10 + 39,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_02_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "II",
						},
					),
				},
				
				{
					"name" : "Inventory_Tab_03",
					"type" : "radio_button",

					"x" : 10 + 78,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_03_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "III",
						},
					),
				},
				
				{
					"name" : "Inventory_Tab_04",
					"type" : "radio_button",

					"x" : 10 + 78+39,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_04_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "IV",
						},
					),
				},

				
				{
					"name" : "Category_Tab_01",
					"type" : "radio_button",

					"x" : 30,
					"y" : 295+32+30,

					"default_image" : "d:/ymir work/ui/yuk_env_1.tga",
					"over_image" : "d:/ymir work/ui/yuk_env_2.tga",
					"down_image" : "d:/ymir work/ui/yuk_env_3.tga",

				},
					
				{
					"name" : "Category_Tab_02",
					"type" : "radio_button",

					"x" : 30+52,
					"y" : 295+32+30,

					"default_image" : "d:/ymir work/ui/bk_env_1.tga",
					"over_image" : "d:/ymir work/ui/bk_env_2.tga",
					"down_image" : "d:/ymir work/ui/bk_env_3.tga",

				},
				
				{
					"name" : "Category_Tab_03",
					"type" : "radio_button",

					"x" : 30+52+52,
					"y" : 295+32+30,

					"default_image" : "d:/ymir work/ui/tas_env_1.tga",
					"over_image" : "d:/ymir work/ui/tas_env_2.tga",
					"down_image" : "d:/ymir work/ui/tas_env_3.tga",

				},
				{ 	"name":"barcek", 
					"type":"horizontalbar", 
					"x":8, 
					"y":395, 
					"width":160, 
					"children" :
					(
						{ "name":"infotext", "type":"text", "x":77, "y":1, "text":uiScriptLocale.STORAGE_WITH_INV, "text_horizontal_align":"center" },
					),
				
				},	
				
				{
					"name" : "acceptbutton",
					"type" : "radio_button",
					"x" : 22,
					"y" : 390+30,
					"tooltip_text" : uiScriptLocale.STORAGE_WITH_INV_TEXT,
					# "vertical_align" : "bottom",
					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				
				{
					"name" : "cancelbutton",
					"type" : "radio_button",
					"x" : 22+26+52-5,
					"y" : 390+30,
					"tooltip_text" : uiScriptLocale.STORAGE_WITH_INV_TEXT2,
					# "vertical_align" : "bottom",
					"default_image" : "d:/ymir work/ui/public/cancelbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/cancelbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/cancelbutton02.sub",
				},
			
			),
		},
	),
}