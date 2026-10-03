import uiScriptLocale



window = {
	"name" : "GameOptionDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 180,
	"height" : 264,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 180,
			"height" : 264,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 165,
					"color" : "gray",

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3, 
						"text" : "Taþ Satma", 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
				
				{
					"name" : "arkaplan",
					"type" : "thinboard_circle",

					"x" : 10,
					"y" : 30,

					"width" : 160,
					"height" : 220,
					
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
							"name" : "stonesell0",
							"type" : "button",

							"x" : 0,
							"y" : 20,

							"horizontal_align":"center",
							"text" : "+0 Taþlarý Sat",

							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
						},
						{
							"name" : "stonesell1",
							"type" : "button",

							"x" : 0,
							"y" : 50,

							"horizontal_align":"center",
							"text" : "+1 Taþlarý Sat",

							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
						},
						{
							"name" : "stonesell2",
							"type" : "button",

							"x" : 0,
							"y" : 80,

							"horizontal_align":"center",
							"text" : "+2 Taþlarý Sat",

							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
						},
						{
							"name" : "stonesell3",
							"type" : "button",

							"x" : 0,
							"y" : 110,

							"horizontal_align":"center",
							"text" : "+3 Taþlarý Sat",

							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
						},
						{
							"name" : "stonesell4",
							"type" : "button",

							"x" : 0,
							"y" : 140,

							"horizontal_align":"center",
							"text" : "+4 Taþlarý Sat",

							"default_image" : "d:/ymir work/ui/buton/1.tga",
							"over_image" : "d:/ymir work/ui/buton/2.tga",
							"down_image" : "d:/ymir work/ui/buton/3.tga",
						},
						{
							"name" : "sellinfo",
							"type" : "text",

							"x" : -65,
							"y" : 175,

							"horizontal_align":"center",
							"text" : "Bu ekran ile üzerinde bulunan",
						},
						{
							"name" : "sellinfo1",
							"type" : "text",

							"x" : -60,
							"y" : 185,

							"horizontal_align":"center",
							"text" : "taþlarýn satýþýný konfüçyusa",
						},		
						{
							"name" : "sellinfo2",
							"type" : "text",

							"x" : -50,
							"y" : 195,

							"horizontal_align":"center",
							"text" : "gitmeden yapabilirsin.",
						},							
					),
				},
			),
		},
	),
}
