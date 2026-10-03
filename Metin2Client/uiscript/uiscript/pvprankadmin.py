BOARD_WIDTH = 200
BOARD_HEIGHT = 185+25

window = {
	"name" : "PvPAdminWindow",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH - BOARD_WIDTH,
	"y" : SCREEN_HEIGHT - 595,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 7,

					"width" : BOARD_WIDTH-12,
					"color" : "gray",
					"children" :
					(
						{
							"name":"TitleName",
							"type":"text",

							"x":0,
							"y":0,

							"text" : "Alan Savaþý ",
							"all_align":"center"
						},
					),
				},
				{
					"name" : "title1",
					"type" : "text",

					"x" : 30,
					"y" : 38,

					"text" : "Min Level: ",
				},
				{
					"name" : "InputSlot1",
					"type" : "slotbar",

					"x" : 30,
					"y" : 36,

					"width" : 30,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "InputValue1",
							"type" : "editline",

							"x" : 3,
							"y" : 3,

							"width" : 235,
							"height" : 25,

							"input_limit" : 30,
						},
					),
				},
				{
					"name" : "title2",
					"type" : "text",

					"x" : 30,
					"y" : 38+20,

					"text" : "Max Level",
				},
				{
					"name" : "InputSlot2",
					"type" : "slotbar",

					"x" : 30,
					"y" : 36+20,

					"width" : 30,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "InputValue2",
							"type" : "editline",

							"x" : 3,
							"y" : 3,

							"width" : 235,
							"height" : 25,

							"input_limit" : 5,
						},
					),
				},
				{
					"name" : "title3",
					"type" : "text",

					"x" : 30,
					"y" : 38+20*2,

					"text" : "Max Kill",
				},
				{
					"name" : "InputSlot3",
					"type" : "slotbar",

					"x" : 30,
					"y" : 36+20*2,

					"width" : 30,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "InputValue3",
							"type" : "editline",

							"x" : 3,
							"y" : 3,

							"width" : 235,
							"height" : 25,

							"input_limit" : 5,
						},
					),
				},
				{
					"name" : "title4",
					"type" : "text",

					"x" : 30,
					"y" : 38+20*3,

					"text" : "Map Index",
				},
				{
					"name" : "InputSlot4",
					"type" : "slotbar",

					"x" : 30,
					"y" : 36+20*3,

					"width" : 30,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "InputValue4",
							"type" : "editline",

							"x" : 3,
							"y" : 3,

							"width" : 235,
							"height" : 25,

							"input_limit" : 5,
						},
					),
				},
				{
					"name" : "okButton",
					"type" : "button",

					"x" : 0,
					"y" : 36+20*5,

					"text" : "Baþlat",
					
					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "cancelButton",
					"type" : "button",

					"x" : 0,
					"y" : 36+20*7-10,

					"text" : "Bitir",
					
					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			),
		},
	),
}
