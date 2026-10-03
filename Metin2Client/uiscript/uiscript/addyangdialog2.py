import uiScriptLocale
import localeInfo
import app

BOARD_HEIGHT = 150+30
window = {
	"name" : "addyangdialog2",

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
				## Input Slot Money
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 20+15,
					"y" : 115,
					"width" : 90+50,
					"height" : 18,
					#"horizontal_align" : "center",

					"children" :
					(
						{
							"name":"Money_Icon",
							"type":"image",

							"x":-18,
							"y":2,

							"image":"d:/ymir work/ui/itemshop/ep.png",
						},
						{
							"name" : "InputValue",
							"type" : "editline",

							"x" : 3,
							"y" : 3,

							"width" : 90+50,
							"height" : 18,

							"input_limit" : 13,
							"only_number" : 1,
						},
					),
				},
				
				## Input Slot Money
				{
					"name" : "SellInfoText",
					"type" : "text",

					"x" : 0,
					"y" : 80,
					"text" : "Çekilecek TL",
					"text_color" : 0xFFFFE3AD,
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},
				## Input Slot Money
				{
					"name" : "MoneyValue",
					"type" : "text",

					"x" : 0,
					"y" : 95,
					"text" : "999999999",
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},
				{
					"name" : "SellInfoText2",
					"type" : "text",

					"x" : 0,
					"y" : 34,
					"text" : "Toplam TL'niz",
					"text_color" : 0xFFFFE3AD,
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},
				
				## Input Slot Coin
				{
					"name" : "InputSlot_Coin",
					"type" : "slotbar",

					"x" : 20+15,
					"y" : 55,
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
							"type" : "text",

							"x" : 3,
							"y" : 3,
							
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