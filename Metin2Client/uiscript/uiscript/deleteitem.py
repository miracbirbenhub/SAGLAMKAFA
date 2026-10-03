import uiScriptLocale

window = {
	"name" : "OfflineShopBuilder",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 185+30,
	"height" : 450+17,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 185+30,
			"height" : 450+17,
			
			"title" : "Toplu Nesne Ýþlemleri",

			"children" :
			(				

				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34+5,

					"start_index" : 0,
					"x_count" : 6,
					"y_count" : 10,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},

				## Ok
				{
					"name" : "OkButton",
					"type" : "button",

					"x" : 21+12-4,
					"y" : 356 + 12,

					"width" : 61,
					"height" : 21,

					"text" : "@ Sil",

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},

				{
					"name":"YangPenceresi",
					"type":"image",

					"x" : 50,
					"y" : 430,

					"image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

					"children" :
					(
						{
							"name":"Money_Icon",
							"type":"image",

							"x":-20,
							"y":2,

							"image":"d:/ymir work/ui/game/windows/money_icon.sub",
						},

						{
							"name" : "toplamfiyat",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Toplam Fiyat",
						},
					),
				},

				## Close
				{
					"name" : "CloseButton",
					"type" : "button",

					"x" : 21+12-4,
					"y" : 356 + 42,

					"width" : 61,
					"height" : 21,

					"text" : "Sýfýrla",

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
				{
					"name" : "SatButton",
					"type" : "button",

					"x" : 104+14,
					"y" : 356 + 12,

					"width" : 61,
					"height" : 21,

					"text" : "$ Sat",

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
				{
					"name" : "VazgecButton",
					"type" : "button",

					"x" : 104+14,
					"y" : 356 + 42,

					"width" : 61,
					"height" : 21,

					"text" : "Ýptal",

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
				{
					"name" : "bilgialkardes",
					"type" : "button",
					
					"x" : 170,
					"y" : 8,
					
					"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
					"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
					"down_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
				},
			),
		},
	),
}
