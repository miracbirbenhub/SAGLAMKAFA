import uiScriptLocale

BOARD_WITDH = 205
BOARD_HEIGHT = 190+45*2

window = {
	"name" : "MenuDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WITDH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WITDH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : BOARD_WITDH-12,
					"color" : "gray",

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3, 
						"text" : "F5 Hýzlý Menü", 
						"horizontal_align":"center", "text_horizontal_align":"center" },
						# {
						# "name" : "DesignTop","type" : "image","style" : ("attach",),"x" : 5+0, "y" : 255,"image" : "d:/ymir work/battle_pass/meno.png",	
						# },
					),
				},
				
			),
		},
	),
}
