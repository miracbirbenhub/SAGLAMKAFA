import uiScriptLocale


PATH = "fishingrank/"

BOARD_WIDTH = 275
BOARD_HEIGTH = 335

BACKGROUND_WITDH = BOARD_WIDTH-15
BACKGROUND_HEIGHT = BOARD_HEIGTH-50

window = {
	"name" : "PvPRank",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGTH,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGTH,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : BOARD_WIDTH-12,
					"color" : "gray",

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3, 
						"text" : "PvP Sýralama", 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
				{
					"name" : "RightMenu",
					"type" : "image",
					"x" : 5,
					"y" : 40,
					"image" : PATH + "rank_list.tga",
					"children":
					(
						{
							"name" : "ListBoxNEW",
							"type" : "listboxex",
							"x" : 0,
							"y" : 0,
							"width" : 400,
							"height" : 38*7,
							#"viewcount" : 4,
						},
						{
							"name": "my",
							"type" : "text",
							"x" : 13,
							"y" : 263,
							"text" : "-",
						},
						{
							"name": "my_name",
							"type" : "text",
							"x" : 64,
							"y" : 263,
							"text" : "",
						},
						{
							"name": "my_value",
							"type" : "text",
							"x" : 186,
							"y" : 263,
							"text" : "",
						},
					),
				},
			),
		},
	),
}
