import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"
LOCALE_PATH = "d:/ymir work/ui/privatesearch/"

ICON_SLOT_FILE = "d:/ymir work/ui/public/Slot_Base.sub"
FACE_SLOT_FILE = "d:/ymir work/ui/game/windows/box_face.sub"

#Mother Board
BOARD_WIDTH = 877 - 75
BOARD_HEIGHT = 510 + 35
POS_START_Y = 65 

#First Board
FIRST_BOARD_START_X = 10
FIRST_BOARD_START_Y = POS_START_Y
FIRST_BOARD_WIDTH = 155
FIRST_BOARD_HEIGHT = (BOARD_HEIGHT - FIRST_BOARD_START_Y - 10 + 25)

#Second Board
SECOND_BOARD_START_X = (FIRST_BOARD_START_X + FIRST_BOARD_WIDTH + 25)
SECOND_BOARD_START_Y = POS_START_Y
SECOND_BOARD_WIDTH = (BOARD_WIDTH - SECOND_BOARD_START_X - 10 - 100 + 75)
SECOND_BOARD_HEIGHT = (BOARD_HEIGHT - SECOND_BOARD_START_Y - 10 + 25 )


#Item Board
ITEM_BOARD_START_X = 5
ITEM_BOARD_START_Y = 10
ITEM_BOARD_WIDTH = 185
ITEM_BOARD_HEIGHT = 136

ITEM_BOARD_X_GAP = 10
ITEM_BOARD_Y_GAP = 10

BUY_BUTTON_Y = 100

window = {
	"name" : "OfferDialog",
	"style" : ("movable", "float",),
	
	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

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
						"text" : "Yang Ýlaný", 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
				{
					"name" : "LoadingImage",
					"type" : "ani_image",

					"x" : 250, "y" : 75,

					"images": (
						"d:/ymir work/ui/itemshop/loading/loading_image0.png",
						"d:/ymir work/ui/itemshop/loading/loading_image1.png",
						"d:/ymir work/ui/itemshop/loading/loading_image2.png",
						"d:/ymir work/ui/itemshop/loading/loading_image3.png",
						"d:/ymir work/ui/itemshop/loading/loading_image4.png",
						"d:/ymir work/ui/itemshop/loading/loading_image5.png",
						"d:/ymir work/ui/itemshop/loading/loading_image6.png",
						"d:/ymir work/ui/itemshop/loading/loading_image7.png",
						"d:/ymir work/ui/itemshop/loading/loading_image8.png",
						"d:/ymir work/ui/itemshop/loading/loading_image9.png",
						"d:/ymir work/ui/itemshop/loading/loading_image10.png",
						"d:/ymir work/ui/itemshop/loading/loading_image11.png",
						"d:/ymir work/ui/itemshop/loading/loading_image12.png",
						"d:/ymir work/ui/itemshop/loading/loading_image13.png",
						"d:/ymir work/ui/itemshop/loading/loading_image14.png",
						"d:/ymir work/ui/itemshop/loading/loading_image15.png",
						"d:/ymir work/ui/itemshop/loading/loading_image16.png",
						"d:/ymir work/ui/itemshop/loading/loading_image17.png",
					),
				},
				{
					"name":"user_background",
					"type":"image",

					"x" : BOARD_WIDTH/2 - 60, "y" : 40,
					
					"image" : "d:/ymir work/ui/itemshop/base/user_display_background.sub",
					
					"children" :
					(
						{
							"name" : "character_name",
							"type" : "text",

							"x" : 3,
							"y" : 7,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "Metin2",
						},
					),
				},
				{
					"name":"coin_background",
					"type":"image",

					"x" : BOARD_WIDTH/2 + 130, "y" : 40,
					
					"image" : "d:/ymir work/ui/itemshop/base/coin_display_background.sub",
					
					"children" :
					(
						{
							"name" : "dragon_coin_text",
							"type" : "text",

							"x" : 33+25,
							"y" : 7,

							"text" : "999 EM",
						},
						{
							"name":"coins_icon",
							"type":"image",
							
							"x" : 33,
							"y" : 7,

							"image":"d:/ymir work/ui/itemshop/ep.png",
						},
					),
				},
				{
					"name" : "board_first",
					"type" : "window",
					"style" : ("attach",),

					"x" : FIRST_BOARD_START_X,
					"y" : FIRST_BOARD_START_Y + 12,

					"width" : FIRST_BOARD_WIDTH+10,
					"height" : FIRST_BOARD_HEIGHT,
					
					"children" : 
					(
						{
							"name" : "background",
							"type" : "image",
							"x" : 0,
							"y" : 0,
							"image" : "d:/ymir work/ui/itemshop/base/category_listbox_background.sub",
						},
						{
							"name" : "yang_category",
							"type" : "button",

							"x" : 10,
							"y" : 10,
							
							"text": "Yang Ýlanlarý",
							
							"default_image" : "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							"over_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_0.sub",
							"down_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							
							"children":(
								{
									"name" : "yang_icon",
									"type" : "image",
									"x" : 13,
									"y" : 10,
									"image": "icon/item/money.tga",
								},
							),
						},
						{
							"name" : "item_category",
							"type" : "button",

							"x" : 10,
							"y" : 10+45,
							
							"text": "Ýtem Ýlanlarý",
							
							"default_image" : "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							"over_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_0.sub",
							"down_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							
							"children":(
								{
									"name" : "yang_icon",
									"type" : "image",
									"x" : 13,
									"y" : 10,
									"image": "icon/item/50513.tga",
								},
							),
						},
						{
							"name" : "my_items",
							"type" : "button",

							"x" : 10,
							"y" : 10+45*2,
							
							"text": "Ýtem Ýlanlarým",
							
							"default_image" : "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							"over_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_0.sub",
							"down_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							
							"children":(
								{
									"name" : "yang_icon",
									"type" : "image",
									"x" : 13,
									"y" : 10,
									"image": "d:/ymir work/ui/itemshop/base/my_icon.png",
								},
							),
						},
						{
							"name" : "my_yangs",
							"type" : "button",

							"x" : 10,
							"y" : 10+45*3,
							
							"text": "Yang Ýlanlarým",
							
							"default_image" : "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							"over_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_0.sub",
							"down_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							
							"children":(
								{
									"name" : "yang_icon",
									"type" : "image",
									"x" : 13,
									"y" : 10,
									"image": "d:/ymir work/ui/itemshop/base/my_icon.png",
								},
							),
						},
						{
							"name" : "add_item",
							"type" : "button",

							"x" : 10,
							"y" : 10+45*4,
							
							"text": "Ýlan Ekle",
							
							"default_image" : "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							"over_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_0.sub",
							"down_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							
							"children":(
								{
									"name" : "yang_icon",
									"type" : "image",
									"x" : 13,
									"y" : 10,
									"image": "d:/ymir work/ui/itemshop/base/add_yang.png",
								},
							),
						},
						{
							"name" : "add_yang",
							"type" : "button",

							"x" : 10,
							"y" : 10+45*5,
							
							"text": "Yang Ekle",
							
							"default_image" : "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							"over_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_0.sub",
							"down_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							
							"children":(
								{
									"name" : "yang_icon",
									"type" : "image",
									"x" : 13,
									"y" : 10,
									"image": "d:/ymir work/ui/itemshop/base/add_yang.png",
								},
							),
						},
						{
							"name" : "bank",
							"type" : "button",

							"x" : 10,
							"y" : 10+45*6,
							
							"text": "Banka",
							
							"default_image" : "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							"over_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_0.sub",
							"down_image" 	: "d:/ymir work/ui/itemshop/base/category_slot_1.sub",
							
							"children":(
								{
									"name" : "yang_icon",
									"type" : "image",
									"x" : 13,
									"y" : 10,
									"image": "d:/ymir work/ui/itemshop/base/money_bag.png",
								},
							),
						},
					),
				},
				{
					"name" : "board_second",
					"type" : "window",
					"style" : ("attach",),

					"x" : SECOND_BOARD_START_X - 5,
					"y" : SECOND_BOARD_START_Y + 13,

					"width" : SECOND_BOARD_WIDTH,
					"height" : SECOND_BOARD_HEIGHT,

					"children"  :
					(
						{
							"name" : "background",
							"type" : "image",
							"x" : 0,
							"y" : 0,
							"image" : "d:/ymir work/ui/itemshop/base/item_listbox_background.sub",
						},
						
						
						{
							"name" : "itemBoard_01",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 0,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 0,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_01",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_01", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 1,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_01", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "", 
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_01", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_01", "type" : "text",
											"x" : 85, "y" : 60, 
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_01", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_01", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_01", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
										## Face Slot
										{ "name" : "Face_Image_01", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_01", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_01",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_01",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_01",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_01",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_01",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						
						{
							"name" : "itemBoard_02",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 1 + ITEM_BOARD_X_GAP,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 0,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_02",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_02", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 2,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_02", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "", 
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_02", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_02", "type" : "text",
											"x" : 85, "y" : 60, 
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_02", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_02", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_02", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
										## Face Slot
										{ "name" : "Face_Image_02", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_02", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_02",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_02",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_02",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_02",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_02",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						
						{
							"name" : "itemBoard_03",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 2 + ITEM_BOARD_X_GAP * 2 ,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 0,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_03",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_03", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 3,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_03", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "", 
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_03", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_03", "type" : "text",
											"x" : 85, "y" : 60,  
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_03", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_03", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_03", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
										## Face Slot
										{ "name" : "Face_Image_03", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_03", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_03",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_03",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_03",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_03",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_03",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						
						{
							"name" : "itemBoard_04",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 0,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 1 + ITEM_BOARD_Y_GAP,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_04",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_04", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 4,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_04", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "", 
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_04", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_04", "type" : "text",
											"x" : 85, "y" : 60, 
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_04", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_04", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_04", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
											## Face Slot
										{ "name" : "Face_Image_04", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_04", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_04",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_04",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_04",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_04",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_04",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						{
							"name" : "itemBoard_05",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 1 + ITEM_BOARD_X_GAP,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 1 + ITEM_BOARD_Y_GAP,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_05",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_05", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 5,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_05", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "", 
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_05", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_05", "type" : "text",
											"x" : 85, "y" : 60,  
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_05", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_05", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_05", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
										## Face Slot
										{ "name" : "Face_Image_05", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_05", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_05",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_05",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_05",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_05",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_05",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						
						{
							"name" : "itemBoard_06",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 2 + ITEM_BOARD_X_GAP * 2,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 1 + ITEM_BOARD_Y_GAP,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_06",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_06", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 6,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_06", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "",
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_06", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_06", "type" : "text",
											"x" : 85, "y" : 60, 
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_06", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_06", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_06", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
										## Face Slot
										{ "name" : "Face_Image_06", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_06", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_06",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_06",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_06",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_06",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_06",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						
						{
							"name" : "itemBoard_07",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 0,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 2 + ITEM_BOARD_Y_GAP * 2,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_07",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_07", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 7,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_07", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "", 
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_07", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_07", "type" : "text",
											"x" : 85, "y" : 60,  
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_07", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_07", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_07", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
										## Face Slot
										{ "name" : "Face_Image_07", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_07", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_07",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_07",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_07",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_07",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_07",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						
						{
							"name" : "itemBoard_08",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 1 + ITEM_BOARD_X_GAP,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 2 + ITEM_BOARD_Y_GAP * 2,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_08",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_08", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 8,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_08", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "",
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_08", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_08", "type" : "text",
											"x" : 85, "y" : 60, 
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_08", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_08", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_08", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
										## Face Slot
										{ "name" : "Face_Image_08", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_08", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_08",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_08",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_08",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_08",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_08",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						
						{
							"name" : "itemBoard_09",
							"type" : "window",
							"style" : ("attach",),

							"x" : ITEM_BOARD_START_X + ITEM_BOARD_WIDTH * 2 + ITEM_BOARD_X_GAP * 2,
							"y" : ITEM_BOARD_START_Y + ITEM_BOARD_HEIGHT * 2 + ITEM_BOARD_Y_GAP * 2,

							"width" : ITEM_BOARD_WIDTH,
							"height" : ITEM_BOARD_HEIGHT,
							
							"children" :
							(
								{
									"name" : "itemslot_image_09",
									"type":  "image",
									"x" : 10,
									"y" : 0,
									"image" : "d:/ymir work/ui/itemshop/base/itemslot.sub", "horizontal_align" : "center",
									
									"children" : 
									(
										{
											"name" : "itemSlot_09", "type" : "grid_table", "x" : 30, "y" : 30, "start_index" : 9,
											"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
										},
										
										{
											"name" : "itemName_09", "type" : "text",
											"x" : 0, "y" : 10, 
											"text" : "", 
											"horizontal_align" : "center",
											"text_horizontal_align" : "center",
										},

										{
											"name" : "itemOldPrice_09", "type" : "text",
											"x" : 60, "y" : 40, 
											"fontname" : "Tahoma:14", "text" : "",
										},
										
										{
											"name" : "itemleftTime_09", "type" : "text",
											"x" : 85, "y" : 60, 
											"text" : "",
										},
										
										{
											"name" : "itemBuyButton_09", "type" : "button",
											"x" : 85, "y" : BUY_BUTTON_Y,
											
											"text" : "", "tooltip_text" : "Satýn al",

											"default_image" : "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/buy_button.sub",
											
											"children" :
											(
												{
													"name" : "coinIcon", "type" : "image",
													"x" : 2,
													"y" : 4,
													"image" : "d:/ymir work/ui/itemshop/ep.png",
												},
											),
										},
										{
											"name" : "removeButton_09", "type" : "button",
											"x" : 85, "y" : 85,
											
											"text" : "", "tooltip_text" : "Sil",

											"default_image" : "d:/ymir work/ui/itemshop/base/remove_button.png",
											"over_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											"down_image" 	: "d:/ymir work/ui/itemshop/base/remove_button.png",
											
										},
										{
											"name" : "bottomIcon", "type" : "image",
											"x" : ITEM_BOARD_WIDTH-16,
											"y" : ITEM_BOARD_HEIGHT-16,
											"image" : "d:/ymir work/ui/itemshop/base/itemslot_right_bottom.sub",
										},
										{
											"name" : "limitIcon_09", "type" : "image",
											"x" : 0,
											"y" : 0,
											"image" : "d:/ymir work/ui/itemshop/base/badge_limitedcount.sub",
										},
											## Face Slot
										{ "name" : "Face_Image_09", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
										{ "name" : "Face_Slot_09", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
										## Character Name Slot
										{
											"name" : "Character_Name_Slot_09",
											"type" : "image",
											"x" : 0+30,
											"y" :27+7,
											"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
											"horizontal_align":"center",

											"children" :
											(
												{
													"name" : "Character_Name_09",
													"type":"text",
													"text":"Name",
													"x":0,
													"y":0,
													"r":1.0,
													"g":1.0,
													"b":1.0,
													"a":1.0,
													"all_align" : "center",
												},
											),
										},
										{
											"name":"Money_Slot_09",
											"type":"button",

											"x":8,
											"y":28+35,

											"horizontal_align":"center",
											#"vertical_align":"bottom",

											"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
											"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name":"Money_Icon_09",
													"type":"image",

													"x":-18,
													"y":2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},

												{
													"name" : "Money_09",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",

													"text" : "123456789",
												},
											),
										},
									),
								},

							),
						},
						{
							"name" : "prev_button", "type" : "button",
							"x" : SECOND_BOARD_WIDTH / 2 - 47, "y" : SECOND_BOARD_HEIGHT - 26*2,

							"default_image" : "d:/ymir work/ui/public/battle/arrow_left.sub",
							"over_image" 	: "d:/ymir work/ui/public/battle/arrow_left_over.sub",
							"down_image" 	: "d:/ymir work/ui/public/battle/arrow_left.sub",
						},
						{
							"name" : "page_text", "type" : "button",
							"x" : SECOND_BOARD_WIDTH / 2 - 17, "y" : SECOND_BOARD_HEIGHT - 28 *2,

							"text" : "0/0",

							"default_image" : LOCALE_PATH + "private_pagenumber_00.sub",
							"over_image" 	: LOCALE_PATH + "private_pagenumber_00.sub",
							"down_image" 	: LOCALE_PATH + "private_pagenumber_00.sub",
						},
						{
							"name" : "next_button", "type" : "button",
							"x" : SECOND_BOARD_WIDTH / 2 + 23, "y" : SECOND_BOARD_HEIGHT - 26*2 ,

							"default_image" : "d:/ymir work/ui/public/battle/arrow_right.sub",
							"over_image" 	: "d:/ymir work/ui/public/battle/arrow_right_over.sub",
							"down_image" 	: "d:/ymir work/ui/public/battle/arrow_right.sub",
						},
					),
				},
			),
		},
	),
}
