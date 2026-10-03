import uiScriptLocale

BOARD_WIDTH = 225
BOARD_HEIGTH = 250
ROOT = "captcha/"

window = {
	"name" : "CaptchaDialog",
	"style" : ("movable", "float",),
	
	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGTH,

	"children" :
	(
		{
			"name" : "board",
			"type" : "thinboard",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGTH,

			"children" :
			(
				# Title
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
						"text" : "Bot Kontrol", 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
				{
					"name" : "item_name",
					"type" : "text",
					"x" : 0,
					"y" : 35,
					"text" : "Eþya Ýsmi",
					"horizontal_align":"center", "text_horizontal_align":"center"
				},
				{
					"name" : "info_text_img",
					"type" : "image",
				
					"x" : 7,
					"y" : 175,
				
					"image" : ROOT + "tab.png",
					
					"children" : (
						{
							"name" : "info_text",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"text" : "Ýsmi verilen eþyayý iþaretleyin.",
							"horizontal_align":"center", "text_horizontal_align":"center"
						},
					),
				},
				{
					"name" : "left_count_img",
					"type" : "image",
				
					"x" : 7,
					"y" : 195,
				
					"image" : ROOT + "tab.png",
					
					"children" : (
						{
							"name" : "left_count",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"text" : "Kalan Hak:",
							"horizontal_align":"center", "text_horizontal_align":"center"
						},
					)
				},
				{
					"name" : "time_img",
					"type" : "image",
				
					"x" : 8,
					"y" : 215,
				
					"image" : ROOT + "tab.png",
					
					"children" : (
						{
							"name" : "time_text",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"text" : "Kalan Süre:",
							"horizontal_align":"center", "text_horizontal_align":"center",
							"color" : 0xff8EC292,
						},
					),
				},
				{
					"name" : "ItemSlot",
					"type" : "grid_table",
					"x" : 18,
					"y" : 35+25,
					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 3,
					"x_step" : 40,
					"y_step" : 32,
					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},
			),
		},
	),
}
