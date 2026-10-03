import uiScriptLocale
import localeInfo

window = {
	"name" : "Chall",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 339,
	"height" : 420,

	"children" :
	(
		## Board and buttons
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 339,
			"height" : 420,

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
								"name" : "refresh",
								"type" : "button",

								"x" : 0,
								"y" : 0,

								"tooltip_text" : "Yenile",

								"default_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
								"over_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe_over.tga",
								"down_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe_down.tga",
								"disable_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
							},
						),
					},
				{
					"name" : "ScrollBar","type" : "scrollbar","x" : 303,"y" : 33,"size" : 253,
				},

				{
					"name" : "yuzdelik",
					"type" : "text",

					"x" : 115+25,
					"y" : 130,

					"text" : "%",
				},
				{
					"name" : "DesignTop","type" : "image","style" : ("attach",),"x" : 12+0, "y" : 287,"image" : "d:/ymir work/battle_pass/challange.png",	
				},
				## TitleBar
				{"name" : "TitleBar","type" : "titlebar","style" : ("attach",),"x" : 8+35,"y" : 8,"width" : 337 - 45,"color" : "gray",
					"children" :
					(
						{ 
							"name":"TitleName", "type":"text", "x" : (337 - 45) / 2, "y":4, "text":"Meydan Okuma Menusu", "text_horizontal_align":"center" 
						},
					),
				},
				
			),
		},
	),
}