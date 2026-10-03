import uiScriptLocale

LOCALE_PATH = "d:/ymir work/ui/privatesearch/"

#Mother Board
BOARD_WIDTH = 877
BOARD_HEIGHT = 510
POS_START_Y = 65

#First Board
FIRST_BOARD_START_X = 10
FIRST_BOARD_START_Y = POS_START_Y
FIRST_BOARD_WIDTH = 155
FIRST_BOARD_HEIGHT = (BOARD_HEIGHT - FIRST_BOARD_START_Y - 10)

#Second Board
SECOND_BOARD_START_X = (FIRST_BOARD_START_X + FIRST_BOARD_WIDTH)
SECOND_BOARD_START_Y = POS_START_Y
SECOND_BOARD_WIDTH = (BOARD_WIDTH - SECOND_BOARD_START_X - 10 - 200)
SECOND_BOARD_HEIGHT = (BOARD_HEIGHT - SECOND_BOARD_START_Y - 10)

#Third Board
THIRD_BOARD_START_X = (SECOND_BOARD_START_X + SECOND_BOARD_WIDTH)
THIRD_BOARD_START_Y = POS_START_Y
THIRD_BOARD_WIDTH = (BOARD_WIDTH - THIRD_BOARD_START_X - 10)
THIRD_BOARD_HEIGHT = (BOARD_HEIGHT - THIRD_BOARD_START_Y - 10)

#Item Board
ITEM_BOARD_START_X = 10
ITEM_BOARD_START_Y = 10
ITEM_BOARD_WIDTH = 160
ITEM_BOARD_HEIGHT = 130

window = {
	"name" : "ItemShopWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

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
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : BOARD_WIDTH-13,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":BOARD_WIDTH/2, "y":3, "text": "Nesne Market", "text_horizontal_align":"center" },
					),
				},
				
				{
					"name" : "search_slotbar", "type" : "slotbar",
					"x" : 15, "y" : POS_START_Y - 30,
					"width" : 160, "height" : 24,
					
					"children" : (
						{
							"name" : "search_editline", "type" : "editline",
							"x" : 3, "y" : 4, "width" : 160, "height" : 24,
							"input_limit" : 24, "fontname" : "Tahoma:16",
						},
					),
				},
				
				{
					"name" : "search_button", "type" : "button",
					"x" : 190, "y" : POS_START_Y - 30,

					"default_image" : "d:/ymir work/ui/itemshop/search_button_default.sub",
					"over_image" 	: "d:/ymir work/ui/itemshop/search_button_over.sub",
					"down_image" 	: "d:/ymir work/ui/itemshop/search_button_down.sub",
				},
				{
					"name":"coins_icon",
					"type":"image",
					
					"x" : BOARD_WIDTH - 230 - 28, "y" : POS_START_Y - 25,

					"image":"d:/ymir work/ui/itemshop/ep.png",
				},					
				{
					"name":"Coins_Slot",
					"type":"image",

					"x" : BOARD_WIDTH - 210 - 28, "y" : POS_START_Y - 27,
					
					"image" : "d:/ymir work/ui/public/Parameter_Slot_01.sub",

					"children" :
					(
						{
							"name" : "dragon_coin_text",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "999 EM",
						},
					),
				},		
				{
					"name":"mark_icon",
					"type":"image",
					
					"x" : BOARD_WIDTH - 155 - 28, "y" : POS_START_Y - 25,

					"image":"d:/ymir work/ui/itemshop/em.png",
				},					
				{
					"name":"Mark_Slot",
					"type":"image",

					"x" : BOARD_WIDTH - 136 - 28, "y" : POS_START_Y - 27,
					
					"image" : "d:/ymir work/ui/public/Parameter_Slot_01.sub",

					"children" :
					(
						{
							"name" : "dragon_mark_text",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "999 EM",
						},
					),
				},		

				{
					"name" : "coin_buy_button", "type" : "button",
					"x" : BOARD_WIDTH - 96 - 15, "y" : POS_START_Y - 30,
					
					"text" : "|cffFFB14AEp Yükle",

					"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
					"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
					"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
				},

				{
					"name" : "board_first",
					"type" : "board",
					"style" : ("attach",),

					"x" : FIRST_BOARD_START_X,
					"y" : FIRST_BOARD_START_Y,

					"width" : FIRST_BOARD_WIDTH,
					"height" : FIRST_BOARD_HEIGHT,
					
					"children" : 
					(
						{
							"name" : "ScrollBar",
							"type" : "scrollbar",

							"x" : 25,
							"y" : 10,
							"size" : FIRST_BOARD_HEIGHT - 20,
							"horizontal_align" : "right",
						},
					),
				},

				{
					"name" : "board_second",
					"type" : "board",
					"style" : ("attach",),

					"x" : SECOND_BOARD_START_X,
					"y" : SECOND_BOARD_START_Y,

					"width" : SECOND_BOARD_WIDTH,
					"height" : SECOND_BOARD_HEIGHT,

					"children"  :
					(
						{
							"name" : "itemBoard_01",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 0,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 0,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_01", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 1,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},

								{
									"name" : "itemName_01", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},

								{
									"name" : "itemOldPrice_01", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},

								{
									"name" : "itemPreviewButton_01", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},

								{
									"name" : "itemBuyButton_01", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},
						
						{
							"name" : "itemBoard_02",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 1,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 0,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_02", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 2,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},
								
								{
									"name" : "itemName_02", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemOldPrice_02", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemPreviewButton_02", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},

								{
									"name" : "itemBuyButton_02", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},
						
						{
							"name" : "itemBoard_03",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 2,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 0,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_03", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 3,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},
								
								{
									"name" : "itemName_03", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemOldPrice_03", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemPreviewButton_03", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},
								
								{
									"name" : "itemBuyButton_03", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},
						
						{
							"name" : "itemBoard_04",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 0,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 1,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_04", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 4,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},
								
								{
									"name" : "itemName_04", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemOldPrice_04", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemPreviewButton_04", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},

								{
									"name" : "itemBuyButton_04", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},
						
						{
							"name" : "itemBoard_05",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 1,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 1,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_05", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 5,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},
								
								{
									"name" : "itemName_05", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemOldPrice_05", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemPreviewButton_05", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},

								{
									"name" : "itemBuyButton_05", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},
						
						{
							"name" : "itemBoard_06",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 2,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 1,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_06", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 6,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},
								
								{
									"name" : "itemName_06", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemOldPrice_06", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemPreviewButton_06", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},

								{
									"name" : "itemBuyButton_06", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},
						
						{
							"name" : "itemBoard_07",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 0,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 2,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_07", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 7,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},
								
								{
									"name" : "itemName_07", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemOldPrice_07", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemPreviewButton_07", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},

								{
									"name" : "itemBuyButton_07", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},
						
						{
							"name" : "itemBoard_08",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 1,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 2,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_08", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 8,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},
								
								{
									"name" : "itemName_08", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemOldPrice_08", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemPreviewButton_08", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},

								{
									"name" : "itemBuyButton_08", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},
						
						{
							"name" : "itemBoard_09",
							"type" : "board",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 2,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 2,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemSlot_09", "type" : "grid_table", "x" : 10, "y" : 10, "start_index" : 9,
									"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 2, "y_blank" : 2,
									"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
								},
								
								{
									"name" : "itemName_09", "type" : "text",
									"x" : 46, "y" : 10, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemOldPrice_09", "type" : "text",
									"x" : 60, "y" : 40, 
									"fontname" : "Tahoma:14", "text" : "",
								},
								{
									"name" : "itemPreviewButton_09", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 65,
									
									"tooltip_text" : "Ön Ýzleme",

									"default_image" : "d:/ymir work/ui/itemshop/preview_button_01.tga",
									"over_image" 	: "d:/ymir work/ui/itemshop/preview_button_02.tga",
									"down_image" 	: "d:/ymir work/ui/itemshop/preview_button_03.tga",
								},

								{
									"name" : "itemBuyButton_09", "type" : "button",
									"x" : ITEM_BOARD_WIDTH - 105, "y" : ITEM_BOARD_HEIGHT - 40,
									
									"text" : "", "tooltip_text" : "Satýn al",

									"default_image" : "d:/ymir work/ui/itemshop/buy_button_default.sub",
									"over_image" 	: "d:/ymir work/ui/itemshop/buy_button_over.sub",
									"down_image" 	: "d:/ymir work/ui/itemshop/buy_button_down.sub",
								},
							),
						},

						{
							"name" : "prev_button", "type" : "button",
							"x" : SECOND_BOARD_WIDTH / 2 - 47, "y" : SECOND_BOARD_HEIGHT - 26,

							"default_image" : "d:/ymir work/ui/public/battle/arrow_left.sub",
							"over_image" 	: "d:/ymir work/ui/public/battle/arrow_left_over.sub",
							"down_image" 	: "d:/ymir work/ui/public/battle/arrow_left.sub",
						},
						{
							"name" : "page_text", "type" : "button",
							"x" : SECOND_BOARD_WIDTH / 2 - 17, "y" : SECOND_BOARD_HEIGHT - 28,

							"text" : "0/0",

							"default_image" : LOCALE_PATH + "private_pagenumber_00.sub",
							"over_image" 	: LOCALE_PATH + "private_pagenumber_00.sub",
							"down_image" 	: LOCALE_PATH + "private_pagenumber_00.sub",
						},
						{
							"name" : "next_button", "type" : "button",
							"x" : SECOND_BOARD_WIDTH / 2 + 23, "y" : SECOND_BOARD_HEIGHT - 26,

							"default_image" : "d:/ymir work/ui/public/battle/arrow_right.sub",
							"over_image" 	: "d:/ymir work/ui/public/battle/arrow_right_over.sub",
							"down_image" 	: "d:/ymir work/ui/public/battle/arrow_right.sub",
						},
					),
				},
				
				{
					"name" : "board_third",
					"type" : "board",
					"style" : ("attach",),

					"x" : THIRD_BOARD_START_X,
					"y" : THIRD_BOARD_START_Y,

					"width" : THIRD_BOARD_WIDTH,
					"height" : THIRD_BOARD_HEIGHT,
					
					"children" :
					(
						{
							"name" : "RenderTarget",
							"type" : "render_target",
		
							"x" : 7,
							"y" : 7,
		
							"width" : THIRD_BOARD_WIDTH-14,
							"height" : THIRD_BOARD_HEIGHT-14,
							"index" : "6",
						},
					),
				},
			),
		},
	),
}
