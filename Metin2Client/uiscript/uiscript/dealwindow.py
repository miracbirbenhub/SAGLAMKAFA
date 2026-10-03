import uiScriptLocale

BOARD_WIDTH = 600
BOARD_HEIGTH = 450

ROOT = "dealornodeal/"

window = {
	"name" : "DealWindow",
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
						"text" : "Var Mýsýn? Yok Musun?", 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
				{
					"name" : "logo",
					"type" : "image",
					"x" : BOARD_WIDTH/3,
					"y" : 33,
					
					"image" : ROOT+ "logo.png", 
				},
				
				{
					"name" : "offer",
					"type" : "image",
					"x" : BOARD_WIDTH/3,
					"y" : BOARD_HEIGTH - 80,
					
					"image" : ROOT+ "offer2.png", 
					
					"children" : (
						{
							"name" : "offer_text",
							"type" : "text",
							"x" : -15,
							"y" : 5,
							
							"text" : "Teklife kalan ",
							"horizontal_align" : "center",
						},
						{
							"name" : "left_box",
							"type" : "text",
							"x" : -15,
							"y" : 25,
							
							"text" : "Son 6 sandýk",
							"horizontal_align" : "center",
						},
					),
				},
				{
					"name" : "offer_accept",
					"type" : "button",
					"x" : BOARD_WIDTH/3 + 65,
					"y" : BOARD_HEIGTH - 27,
					
					"default_image" : ROOT + "offer_accept_default.png",
					"over_image" : ROOT + "offer_accept_over.png",
					"down_image" : ROOT + "offer_accept_down.png",
				},
				{
					"name" : "offer_cancel",
					"type" : "button",
					"x" : BOARD_WIDTH/3 + 115,
					"y" : BOARD_HEIGTH - 27,
					
					"default_image" : ROOT + "offer_cancel_default.png",
					"over_image" : ROOT + "offer_cancel_over.png",
					"down_image" : ROOT + "offer_cancel_down.png",
				},

			),
		},
	),
}
