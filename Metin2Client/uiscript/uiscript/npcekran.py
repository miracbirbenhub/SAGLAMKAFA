import uiScriptLocale



window = {
	"name" : "GameOptionDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 380,
	"height" : 220+28*5+50,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 380,
			"height" : 220+28*5+50,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 362,
					"color" : "gray",

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3, 
						"text" : "Uzaktan NPC", 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
				
				{
					"name" : "arkaplan",
					"type" : "thinboard_circle",

					"x" : 10,
					"y" : 60,

					"width" : 362,
					"height" : 10+28*5+50,
					
					"children" :
					(
						# {
							# "name" : "epbilgi",
							# "type" : "text",

							# "x" : 15,
							# "y" : 10,

							# "text" : "|cff00ff00|H|hEjderha Parasý : 0",

						# },
						{
							"name" : "market",
							"type" : "button",

							"x" : 0,
							"y" : 10+0*1,

							"horizontal_align":"center",
							"text" : "Sancak2/Satýcý",

							"default_image" : "d:/ymir work/ui/menu/1.png",
							"over_image" : "d:/ymir work/ui/menu/2.png",
							"down_image" : "d:/ymir work/ui/menu/3.png",
						},
						{
							"name" : "silah",
							"type" : "button",

							"x" : 0,
							"y" : 10+15*2,

							"horizontal_align":"center",
							"text" : "Sancak2/Silahcý",

							"default_image" : "d:/ymir work/ui/menu/1.png",
							"over_image" : "d:/ymir work/ui/menu/2.png",
							"down_image" : "d:/ymir work/ui/menu/3.png",
						},
						{
							"name" : "zirh",
							"type" : "button",

							"x" : 0,
							"y" : 10+20*3,

							"horizontal_align":"center",
							"text" : "Sancak2/Zýrhcý",

							"default_image" : "d:/ymir work/ui/menu/1.png",
							"over_image" : "d:/ymir work/ui/menu/2.png",
							"down_image" : "d:/ymir work/ui/menu/3.png",
						},
						{
							"name" : "olay",
							"type" : "button",

							"x" : 0,
							"y" : 10+23*4,

							"horizontal_align":"center",
							"text" : "Sancak2/K.Market",

							"default_image" : "d:/ymir work/ui/menu/1.png",
							"over_image" : "d:/ymir work/ui/menu/2.png",
							"down_image" : "d:/ymir work/ui/menu/3.png",
						},
						{
							"name" : "genel",
							"type" : "button",

							"x" : 0,
							"y" : 10+25*5,

							"horizontal_align":"center",
							"text" : "Sancak2/E.Market",

							"default_image" : "d:/ymir work/ui/menu/1.png",
							"over_image" : "d:/ymir work/ui/menu/2.png",
							"down_image" : "d:/ymir work/ui/menu/3.png",
						},
						{
					"name" : "DesignTop","type" : "image","style" : ("attach",),"x" : 0+0, "y" : -30,"image" : "d:/ymir work/ui/menu/uzaknpcboard.png",	
						},
						{
					"name" : "DesignTop","type" : "image","style" : ("attach",),"x" : 20+0, "y" : 40,"image" : "d:/ymir work/ui/menu/shosol.png",	
						},
						{
					"name" : "DesignTop","type" : "image","style" : ("attach",),"x" : 270+0, "y" : 40,"image" : "d:/ymir work/ui/menu/shosol.png",	
						},
						{
					"name" : "DesignTop","type" : "image","style" : ("attach",),"x" : -2+0, "y" : 175,"image" : "d:/ymir work/ui/menu/uzakmarket.png",	
						},

					),
				},
			),
		},
	),
}
