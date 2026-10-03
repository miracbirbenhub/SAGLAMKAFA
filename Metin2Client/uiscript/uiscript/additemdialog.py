import uiScriptLocale
import localeInfo
import app

BOARD_HEIGHT = 150+80
window = {
	"name" : "additemdialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 200,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : BOARD_HEIGHT,

			"title" : "",

			"children" :
			(
				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 80,
					"y" : 100,

					"start_index" : 0,
					"x_count" : 1,
					"y_count" : 3,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},
				{
					"name" : "SellInfoText2",
					"type" : "text",

					"x" : 0,
					"y" : 34+20,
					"text" : "Satýþ Fiyatý",
					"text_color" : 0xFFFFE3AD,
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},
				## Input Slot Money
				{
					"name" : "CoinValue",
					"type" : "text",

					"x" : 0,
					"y" : 34+20*2,
					"text" : "999",
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},
				
				## Input Slot Coin
				{
					"name" : "InputSlot_Coin",
					"type" : "slotbar",

					"x" : 20+15,
					"y" : 34,
					"width" : 90+50,
					"height" : 18,
					#"horizontal_align" : "center",

					"children" :
					(
						{
							"name":"Coin_Icon",
							"type":"image",

							"x":-18,
							"y":2,

							"image":"d:/ymir work/ui/itemshop/ep.png",
						},
						{
							"name" : "InputValue_Coin",
							"type" : "editline",

							"x" : 3,
							"y" : 3,

							"width" : 90+50,
							"height" : 18,

							"input_limit" : 9,
							"only_number" : 1,
							
							"text" : "0",
						},
					),
				},
				

				## Button
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : - 61 - 5 + 30,
					"y" : BOARD_HEIGHT - 32,
					"horizontal_align" : "center",

					"text" : uiScriptLocale.OK,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 5 + 30,
					"y" : BOARD_HEIGHT - 32,
					"horizontal_align" : "center",

					"text" : uiScriptLocale.CANCEL,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
			),
		},
	),
}