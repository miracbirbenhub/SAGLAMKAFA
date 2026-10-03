BAKIM_X = 120
AYIR_X = 8

window = {
	"name" : "MaintenanceAdminWindow",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH - 200,
	"y" : SCREEN_HEIGHT - 595,

	"width" : 300,
	"height" : 260,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 300,
			"height" : 260,

			"children" :
			(
				{
					"name" : "TitleBakim",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 7,

					"width" : 288,
					"color" : "gray",
					"children" :
					(
						{
							"name":"TitleName",
							"type":"text",

							"x":0,
							"y":0,

							"text" : "Bakým Paneli",
							"all_align":"center"
						},
					),
				},
				{
					"name" : "title1",
					"type" : "text",

					"x" : BAKIM_X,
					"y" : 36,

					"text" : "Bakým Nedeni",
				},
				{
					"name" : "InputSlot1",
					"type" : "slotbar",

					"x" : -1,
					"y" : 56,

					"width" : 235,
					"height" : 25,

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

					"x" : 53,
					"y" : 86,

					"text" : "Bakýma kalan süre",
				},
				{
					"name" : "InputSlot2",
					"type" : "slotbar",

					"x" : -60,
					"y" : 106,

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

					"x" : 183,
					"y" : 86,

					"text" : "Bakým süresi",
				},
				{
					"name" : "InputSlot3",
					"type" : "slotbar",

					"x" : 60,
					"y" : 106,

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
					"name" : "TimeNot",
					"type" : "text",

					"x" : 60,
					"y" : 130,

					"text" : "|cFFf05656 Not : " + "|cFFffffff Süreleri saniye cinsinden giriniz!",
				},
				{
					"name" : "CoreNot",
					"type" : "text",

					"x" : 60,
					"y" : 142,

					"text" : "|cFFf05656 CoreNot : " + "|cFFffffff Oyundaki aktif clientlere bilgi gönderir. ",
				},
				{
					"name" : "okButton",
					"type" : "button",

					"x" : 60,
					"y" : 162,

					"text" : "Bakýmý Baþlat",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "cancelButton",
					"type" : "button",

					"x" : 160,
					"y" : 162,

					"text" : "Bakýmý Ýptal Et",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "maintenanceupdateButton",
					"type" : "button",

					"x" : 60,
					"y" : 192,

					"text" : "Bakým Güncelle",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "updateclientButton",
					"type" : "button",

					"x" : 160,
					"y" : 192,

					"text" : "Coreye Bilgi Ver",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "whycancelButton",
					"type" : "button",

					"x" : 60,
					"y" : 222,

					"text" : "B.Nedeni Kaldýr",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "whyupdateButton",
					"type" : "button",

					"x" : 160,
					"y" : 222,

					"text" : "B.Nedeni Güncelle",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			),
		},
	),
}
