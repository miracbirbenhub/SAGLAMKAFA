import app
import localeInfo

WINDOW_WIDTH	= 627
WINDOW_HEIGHT	= 590

try:
	ENABLE_WOLFMAN_CHARACTER = app.ENABLE_WOLFMAN_CHARACTER
except:
	ENABLE_WOLFMAN_CHARACTER = 0

try:
	ENABLE_CHEQUE_SYSTEM = app.ENABLE_CHEQUE_SYSTEM
except:
	ENABLE_CHEQUE_SYSTEM = 0




SEARCH_AND_FILTER_BACKGROUND = "offlineshop/searchfilter/base_image.png"
SAFEBOX_WITHDRAW_BUTTON	= "offlineshop/safebox/withdrawyang_%s.png"

if ENABLE_WOLFMAN_CHARACTER:
	SEARCH_AND_FILTER_BACKGROUND = "offlineshop/searchfilter/base_image_lycan.png"

if ENABLE_CHEQUE_SYSTEM:
	SAFEBOX_WITHDRAW_BUTTON = "offlineshop/safebox/withdrawyang_%s_cheque.png"




if ENABLE_CHEQUE_SYSTEM:
	SAFEBOX_CHILDREN = (
		{
			"name": "BackgroundShopSafeboxPage",
			"type": "image",

			"x": 0, "y": 0,

			"image": "offlineshop/safebox/safebox_base_image.png",
		},
		{
			"name" : "ShopSafeboxWithdrawYangButton",
			"type" : "button",

			"x" : 447-205 - 38,
			"y" : 16-4,

			"default_image" :  SAFEBOX_WITHDRAW_BUTTON%"default",
			"over_image" 	:  SAFEBOX_WITHDRAW_BUTTON%"over",
			"down_image" 	:  SAFEBOX_WITHDRAW_BUTTON%"down",
		},

		{
			"name" : "ShopSafeboxValuteText",
			"type" : "text",

			"x" : 468-154 - 38,
			"y" : 22-8,

			"text_horizontal_align" : "center",
			"text" : "000000",
		},
		
		{
			"name" : "ShopSafeboxValuteTextCheque",
			"type" : "text",

			"x" : 468-154 - 38 + 115,
			"y" : 22-8,

			"text_horizontal_align" : "center",
			"text" : "000000",
		},
	)

else:
	SAFEBOX_CHILDREN = (
		{
			"name": "BackgroundShopSafeboxPage",
			"type": "image",

			"x": 0, "y": 0,

			"image": "offlineshop/safebox/safebox_base_image.png",
		},
		{
			"name" : "ShopSafeboxWithdrawYangButton",
			"type" : "button",

			"x" : 447-205,
			"y" : 16-4,

			"default_image" :  SAFEBOX_WITHDRAW_BUTTON%"default",
			"over_image" 	:  SAFEBOX_WITHDRAW_BUTTON%"over",
			"down_image" 	:  SAFEBOX_WITHDRAW_BUTTON%"down",
		},

		{
			"name" : "ShopSafeboxValuteText",
			"type" : "text",

			"x" : 468-154,
			"y" : 22-8,

			"text_horizontal_align" : "center",
			"text" : "000000",
		},
	)






window = {

	"name" : "OfflineshopBoard",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH/2  - WINDOW_WIDTH/2,
	"y" : SCREEN_HEIGHT/2  - WINDOW_HEIGHT/2,

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "MainBoard",
			"type" : "board",
			
			"style" : ("attach",),
			
			"x" : 0,
			"y" : 0,
			
			"width" 	: WINDOW_WIDTH,
			"height" 	: WINDOW_HEIGHT,
			
			"children" : 
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					
					"x" : 8,
					"y" : 7,
					
					"width"  : WINDOW_WIDTH - 16,
					"color"  : "red",
					
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-1, "text":"Offline Shop", "all_align":"center" },
					),
				},





				#MyShop_noShop
				{
					"name" : "MyShopBoardNoShop",
					"type" : "window",
					
					"width" :  622,  "height" :  544,
					
					"x" : 3, "y" : 78,
					
					"children":
					(
						{
							"name" : "BackGroundCreate",
							"type" : "image",
							
							"x" : 0, "y" : 0,
							"image": "offlineshop/createshop/base_image_1.png",
							
						},
						
						# {
						# 	"name" : "HowToInsertItems",
						# 	"type" : "image",
						#
						# 	"x" : 150, "y" : 300,
						#
						# 	"image" 			: "offlineshop/createshop/howto_insert_items.png",
						#
						# },
					
						{
							"name" : "ShopNameInput",
							"type" : "editline",
							
							"width" : 217 , "height" : 15 ,
							
							"input_limit" : 35,
							"x" : 205, "y" : 34,
						},
						
						
						
						#count texts
						{
							"name" : "DaysCountText",
							"type" : "text",
							
							"text" : "0",
							"text_horizontal_align" : "center",
							"x" : 255, "y" :89,
						},
						
						
						
						{
							"name" : "HoursCountText",
							"type" : "text",
							
							"text" : "0",
							"text_horizontal_align" : "center",
							"x" : 367, "y" : 89,
						},
						
						
						
						#increase-reduce buttons
						{
							"name" : "IncreaseDaysButton",
							"type" : "button",
							

							"x" : 291-10,
							"y" : 91,

							"default_image" : "offlineshop/shopsearchp2p/btn_next_normal.dds",
							"over_image" 	: "offlineshop/shopsearchp2p/btn_next_down.dds",
							"down_image" 	: "offlineshop/shopsearchp2p/btn_next_over.dds",
						},
						
						
						{
							"name" : "DecreaseDaysButton",
							"type" : "button",
							
							"x" : 218,
							"y" : 91,
							
							"default_image" : "offlineshop/shopsearchp2p/btn_back_normal.dds",
							"over_image" 	: "offlineshop/shopsearchp2p/btn_back_down.dds",
							"down_image" 	: "offlineshop/shopsearchp2p/btn_back_over.dds",
						},
						
						
						
						{
							"name" : "IncreaseHoursButton",
							"type" : "button",
							
							"x" : 400-8,
							"y" : 91,
							
							"default_image" : "offlineshop/shopsearchp2p/btn_next_normal.dds",
							"over_image" 	: "offlineshop/shopsearchp2p/btn_next_down.dds",
							"down_image" 	: "offlineshop/shopsearchp2p/btn_next_over.dds",
						},
						
						
						{
							"name" : "DecreaseHoursButton",
							"type" : "button",
							
							"x" : 330-3,
							"y" : 91,
							
							"default_image" : "offlineshop/shopsearchp2p/btn_back_normal.dds",
							"over_image" 	: "offlineshop/shopsearchp2p/btn_back_down.dds",
							"down_image" 	: "offlineshop/shopsearchp2p/btn_back_over.dds",
						},
						
						#next button
						{
							"name" : "CreateShopButton",
							"type" : "button",
							
							"x" : 249 + 40,
							"y" : 482 - 8,
							
							"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
							"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
							"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",

						}
					),
				},




				#MyShop_Owner
				{
					"name" : "MyShopBoard",
					"type" : "window",
					
					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,
					
					"children":
					(
						{
							"name" : "BackgroundMySHop",
							"type" : "image",
							
							"x" : 0, "y" : 0,
							
							"image" : "offlineshop/myshop/base_image_0.png",
						},
						
						
						{
							"name" : "MyShopShopTitle",
							"type" : "text",
							
							"x" : 340, "y" : 5,
							
							"text" : "title",
							"text_horizontal_align" : "center",
						},
						
						{
							"name" : "MyShopEditTitleButton",
							"type" : "button",
							
							"x" : 450, "y" : 15,
							
							"tooltip_text"	: localeInfo.OFFLINESHOP_EDIT_SHOPNAME_TOOLTIP,
							
							"default_image" : "offlineshop/myshop/editname_default.png",
							"over_image" 	: "offlineshop/myshop/editname_over.png",
							"down_image" 	: "offlineshop/myshop/editname_down.png",
						},
						
						{
							"name" : "MyShopShopDuration",
							"type" : "text",
							
							"x" : 340, "y" : 24,
							
							"text" : "99 days",
							"text_horizontal_align" : "center",
						},
						
						
						{
							"name" : "MyShopCloseButton",
							"type" : "button",
							
							"x" : 15,
							"y" : 20,
							
							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",

							"text" : localeInfo.OFFLINESHOP_SCRIPTFILE_CLOSE_SHOP_TEXT,
						}
					),
				},



				#shoplist_open
				{
					"name" : "ListOfShop_OpenShop",
					"type" : "window",
					
					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,
					
					"children":
					(
						{
							"name" : "BackgroundShopListOpen",
							"type" : "image",
							
							"x" : 0, "y" : 0,
							
							"image" : "offlineshop/shoplist/base_image_open.png",
						},
						
						{
							"name" : "OpenShopBackToListButton",
							"type" : "button",
							
							"x" : 15, "y" : 5,
							
							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",

							"text" : localeInfo.OFFLINESHOP_SCRIPTFILE_CLOSE_SHOP_TEXT,
						},
						{
							"name" : "OpenShopShopTitle",
							"type" : "text",
							
							"x" : 328, "y" : 6,

							"text_horizontal_align" : "center",
							"text" : "title",
						},
						
						{
							"name" : "OpenShopShopDuration",
							"type" : "text",
							
							"x" : 328, "y" : 27,

							"text_horizontal_align" : "center",
							"text" : "99 days",
						},
					),
				},


				#shoplist_list
				{
					"name" : "ListOfShop_List",
					"type" : "window",
					
					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,
					"children":
					(
						{
							"name" : "BackgroundShopList",
							"type" : "image",
							
							"x" : 0, "y" : 0,
							
							#"image" : "offlineshop/shoplist/base_image_list.png",
						},
					),
				},



				#searchhistory
				{
					"name" : "SearchHistoryBoard",
					"type" : "window",
					
					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,
					"children":
					(
						{
							"name" : "BackgroundSearchHistory",
							"type" : "image",
							
							"x" : 0, "y" : 0,
							
							"image" : "offlineshop/searchhistory/base_image.png",
						},
					),
				},


				#mypatterns
				{
					"name" : "MyPatternsBoard",
					"type" : "window",
					
					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,
					"children":
					(
						{
							"name" : "BackgroundMyPatterns",
							"type" : "image",
							
							"x" : 0, "y" : 0,
							
							"image" : "offlineshop/mypatterns/base_image.png",
						},
					),
				},




				#searchfilter
				{
					"name" : "SearchFilterBoard",
					"type" : "window",
					
					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,
					"children":
					(
						{
							"name" : "BackgroundSearchFilter",
							"type" : "image",
							
							"x" : 0, "y" : 0,
							
							"image" : SEARCH_AND_FILTER_BACKGROUND,
						},
						
						{
							"name" : "SearchFilterItemNameInput",
							"type" : "editline",
							
							"width" : 150, "height" : 15,
							
							"input_limit" : 24,
							"x" : 80, "y" : 31,
						},
						
						
						{
							"name" : "SearchFilterItemLevelStart",
							"type" : "editline",
							
							"width" : 43, "height" : 14,
							
							"input_limit" : 3,
							"only_number" : 1,
							"x" : 363, "y" : 32,
						},
						
						
						
						{
							"name" : "SearchFilterItemLevelEnd",
							"type" : "editline",
							
							"width" : 43, "height" : 14,
							
							"input_limit" : 3,
							"only_number" : 1,
							"x" : 363, "y" : 52,
						},
						
						
						{
							"name" : "SearchFilterItemYangMin",
							"type" : "editline",
							
							"width" : 130, "height" : 15,
							
							"input_limit" : len("999999999999999999"),
							"only_number" : 1,
							"x" : 258, "y" : 103,
						},
						
						
						
						{
							"name" : "SearchFilterItemYangMax",
							"type" : "editline",
							
							"width" : 130, "height" : 15,
							
							"input_limit" : len("999999999999999999"),
							"only_number" : 1,
							"x" : 258, "y" : 127,
						},
						
						
						
						
						
						{
							"name" : "SearchFilterResetFilterButton",
							"type" : "button",
							
							"x" : 400, "y" : 487,
							
							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : localeInfo.OFFLINESHOP_SCRIPTFILE_RESET_FILTER_TEXT,
						},
						
						
						
						{
							"name" : "SearchFilterSavePatternButton",
							"type" : "button",
							
							"x" : 139, "y" : 487,
							
							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : localeInfo.OFFLINESHOP_SCRIPTFILE_SAVE_AS_PATTERN_TEXT,
						},
						
						
						{
							"name" : "SearchFilterStartSearch",
							"type" : "button",
							
							"x" : 268, "y" : 487,
							
							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : localeInfo.OFFLINESHOP_SCRIPTFILE_START_SEARCH_TEXT,
						},
						
						{
							"name" : "SearchFilterAttributeButton1",
							"type" : "button",
							
							"x" : 406, "y" : 35,
							
							"default_image" : "offlineshop/searchfilter/attribute_default.png",
							"over_image" 	: "offlineshop/searchfilter/attribute_over.png",
							"down_image" 	: "offlineshop/searchfilter/attribute_down.png",
						},
						
						
						
						{
							"name" : "SearchFilterAttributeButton2",
							"type" : "button",
							
							"x" : 406, "y" : 35+22,
							
							"default_image" : "offlineshop/searchfilter/attribute_default.png",
							"over_image" 	: "offlineshop/searchfilter/attribute_over.png",
							"down_image" 	: "offlineshop/searchfilter/attribute_down.png",
						},
						
						
						
						{
							"name" : "SearchFilterAttributeButton3",
							"type" : "button",
							
							"x" : 406, "y" : 35+22*2,
							
							"default_image" : "offlineshop/searchfilter/attribute_default.png",
							"over_image" 	: "offlineshop/searchfilter/attribute_over.png",
							"down_image" 	: "offlineshop/searchfilter/attribute_down.png",
						},
						
						
						{
							"name" : "SearchFilterAttributeButton4",
							"type" : "button",
							
							"x" : 406, "y" : 35+22*3,
							
							"default_image" : "offlineshop/searchfilter/attribute_default.png",
							"over_image" 	: "offlineshop/searchfilter/attribute_over.png",
							"down_image" 	: "offlineshop/searchfilter/attribute_down.png",
						},
						
						
						{
							"name" : "SearchFilterAttributeButton5",
							"type" : "button",
							
							"x" : 406, "y" : 35+22*4,
							
							"default_image" : "offlineshop/searchfilter/attribute_default.png",
							"over_image" 	: "offlineshop/searchfilter/attribute_over.png",
							"down_image" 	: "offlineshop/searchfilter/attribute_down.png",
						},
					),
				},



				#safebox
				{
					"name": "ShopSafeboxPage",
					"type": "window",

					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,
					"children":
					(
						SAFEBOX_CHILDREN
					),
				},




				#my offers
				{
					"name": "MyOffersPage",
					"type": "window",

					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,

					"children":
					(
						{
							"name": "BackgroundMyOffersPage",
							"type": "image",

							"x": 0, "y": 0,

							"image": "offlineshop/myoffers/base_image.png",
						},
					),
				},




				# my auction
				{
					"name": "MyAuction",
					"type": "window",

					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,

					"children":
					(
						{
							"name": "BackgroundMyAuctionPage",
							"type": "image",

							"x": 0, "y": 0,

							"image": "offlineshop/myauction/base_image.png",
						},

						{
							"name" : "MyAuction_OwnerName",
							"type" : "text",

							"x" : 235+67, "y" : 100-70,
							"text_horizontal_align" : "center",
							"text" : " noname ",
						},

						{
							"name" : "MyAuction_Duration",
							"type" : "text",

							"x" : 235+67, "y" : 145-91,
							"text_horizontal_align" : "center",
							"text" : " noname ",
						},

						{
							"name" : "MyAuction_BestOffer",
							"type" : "text",

							"x" : 235+67, "y" : 197-123,
							"text_horizontal_align" : "center",
							"text" : " noname ",
						},

						{
							"name": "MyAuction_MinRaise",
							"type": "text",

							"x": 235+67, "y": 243-147,
							"text_horizontal_align": "center",
							"text": " noname ",
						},
					),
				},




				# open acution
				{
					"name": "OpenAuction",
					"type": "window",

					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,

					"children":
					(
						{
							"name": "BackgroundOpenAuctionPage",
							"type": "image",

							"x": 0, "y": 0,

							"image": "offlineshop/openauction/base_image.png",
						},

						{
							"name": "OpenAuctionBackToListButton",
							"type": "button",

							"x": 15, "y": 5,

							"default_image": "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image": "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image": "d:/ymir work/ui/public/middle_button_03.sub",

							"text": localeInfo.OFFLINESHOP_SCRIPTFILE_CLOSE_AUCTION_TEXT,
						},

						{
							"name": "OpenAuction_OwnerName",
							"type": "text",

							"x" : 235+67, "y" : 100-70,
							"text_horizontal_align": "center",
							"text": " noname ",
						},

						{
							"name": "OpenAuction_Duration",
							"type": "text",

							"x" : 235+67, "y" : 145-91,
							"text_horizontal_align": "center",
							"text": " noname ",
						},

						{
							"name": "OpenAuction_BestOffer",
							"type": "text",

							"x": 235+67, "y": 197-123,
							"text_horizontal_align": "center",
							"text": " noname ",
						},

						{
							"name": "OpenAuction_MinRaise",
							"type": "text",

							"x": 235+67, "y": 243-147,
							"text_horizontal_align": "center",
							"text": " noname ",
						},
					),
				},




				# acutionlist
				{
					"name": "AuctionList",
					"type": "window",

					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,

					"children":
					(
						{
							"name": "BackgroundAuctionListPage",
							"type": "image",

							"x": 0, "y": 0,

							"image": "offlineshop/auctionlist/base_image.png",
						},
					),
				},



				#create auction
				{
					"name": "CreateAuction",
					"type": "window",

					"width" :  622,  "height" :  544,

					"x" : 3, "y" : 78,

					"children":
					(
						{
							"name": "BackgroundCreateAuctionPage",
							"type": "image",

							"x": 0, "y": 0,

							"image": "offlineshop/createauction/base_image.png",
						},
						{
							"name": "CreateAuctionDaysInput",
							"type": "text",

							"width": 23, "height": 17,

							"text_horizontal_align" : "center",
							"text" : "0",
							"x": 299, "y": 181,
						},
						{
							"name": "CreateAuctionStartingPriceInput",
							"type": "editline",

							"width": 122, "height": 15,

							"input_limit": 10,
							"only_number": 1,
							"x": 272, "y": 210,
						},

						{
							"name": "CreateAuctionDecreaseDaysButton",
							"type": "button",

							"x": 325,
							"y": 183,

							"default_image": "offlineshop/scrollbar/horizontal/button2_default.png",
							"over_image" : "offlineshop/scrollbar/horizontal/button2_over.png",
							"down_image" 	: "offlineshop/scrollbar/horizontal/button2_down.png",
						},


						{
							"name" : "CreateAuctionIncreaseDaysButton",
							"type" : "button",

							"x" : 267-2,
							"y" : 183,

							"default_image" : "offlineshop/scrollbar/horizontal/button1_default.png",
							"over_image" 	: "offlineshop/scrollbar/horizontal/button1_over.png",
							"down_image" 	: "offlineshop/scrollbar/horizontal/button1_down.png",
						},

						{
							"name" : "CreateAuctionCreateAuctionButton",
							"type" : "button",

							"x" : 211+98, "y" : 267-33,

							"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
							"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
							"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",

							"text" : localeInfo.OFFLINESHOP_SCRIPTFILE_CREATE_TEXT,
						}
					),
				},

				{
					"name" : "Menu",
					"type" : "thinboard_circle",
					
					"x" : 13,
					"y" : 34,

					"width" : 600,
					"height" : 40,

					"children":
					(
					
						# Back Button
						{
							"name": "SearchFilterButton",
							"type": "button",

							"x": 50, "y": 10,

							"tooltip_text" : "Esya Arama",

							"default_image" : "offlineshop/shopsearchp2p/4.png",
							"over_image" : "offlineshop/shopsearchp2p/4.png",
							"down_image" : "offlineshop/shopsearchp2p/4.png",
							
						},
						
						{
							"name": "MyShopButton",
							"type": "button",

							"x": 10, "y": 10,

							"tooltip_text" : "Pazar",

							"default_image" : "offlineshop/shopsearchp2p/2.png",
							"over_image" : "offlineshop/shopsearchp2p/2_1.png",
							"down_image" : "offlineshop/shopsearchp2p/2_2.png",
						},

						#{
							#"name": "ListOfShopButton",
							#"type": "button",

							#"x": 90, "y": 10,

							#"tooltip_text" : "Pazar Listesi",

							#"default_image" : "offlineshop/shopsearchp2p/pazarliste.png",
							#"over_image" : "offlineshop/shopsearchp2p/pazarliste2.png",
							#"down_image" : "offlineshop/shopsearchp2p/pazarliste3.png",
						#},
						
						{
							"name": "ShopSafeboxButton",
							"type": "button",

							"x": 90, "y": 10,

							"tooltip_text" : "Depo",

							"default_image" : "offlineshop/shopsearchp2p/3.png",
							"over_image" : "offlineshop/shopsearchp2p/3_1.png",
							"down_image" : "offlineshop/shopsearchp2p/3_2.png",
						},
						

						#{
							#"name": "MyOffersPageButton",
							#"type": "button",

							#"x": 170, "y": 10,

							#"tooltip_text" : "Tekliflerim",

							#"default_image" : "offlineshop/shopsearchp2p/shop_btn_log_active.dds",
							#"over_image" : "offlineshop/shopsearchp2p/shop_btn_log_hover.dds",
							#"down_image" : "offlineshop/shopsearchp2p/shop_btn_log_normal.dds",
						#},

						#{
							#"name": "SearchHistoryButton",
							#"type": "button",

							#"x": 170, "y": 10,

							#"tooltip_text" : "Gecmis",

							#"default_image" : "offlineshop/shopsearchp2p/gecmis.png",
							#"over_image" : "offlineshop/shopsearchp2p/gecmis2.png",
							#"down_image" : "offlineshop/shopsearchp2p/gecmis3.png",
						#},

						#{
							#"name": "MyPatternsButton",
							#"type": "button",

							#"x": 210, "y": 10,

							#"tooltip_text" : "Kaydettiklerim",

							#"default_image" : "offlineshop/shopsearchp2p/kaydet.png",
							#"over_image" : "offlineshop/shopsearchp2p/kaydet2.png",
							#"down_image" : "offlineshop/shopsearchp2p/kaydet3.png",
						#},

						#{
							#"name": "MyAuctionButton",
							#"type": "button",

							#"x": 270, "y": 10,

							#"tooltip_text" : "Islemlerim",

							#"default_image" : "offlineshop/shopsearchp2p/shop_btn_log_active.dds",
							#"over_image" : "offlineshop/shopsearchp2p/shop_btn_log_hover.dds",
							#"down_image" : "offlineshop/shopsearchp2p/shop_btn_log_normal.dds",
						#},

						#{
							#"name": "ListOfAuctionsButton",
							#"type": "button",

							#"x": 300, "y": 10,

							#"tooltip_text" : "Acik Arttirma",

							#"default_image" : "offlineshop/shopsearchp2p/shop_btn_log_active.dds",
							#"over_image" : "offlineshop/shopsearchp2p/shop_btn_log_hover.dds",
							#"down_image" : "offlineshop/shopsearchp2p/shop_btn_log_normal.dds",
						#},
						
					),
				},

			),
		},
	),
}













