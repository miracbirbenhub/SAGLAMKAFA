import uiScriptLocale
import item
import app
import localeInfo

ROOT_PATH = "d:/ymir work/ui/"

LOCALE_PATH = "d:/ymir work/ui/privatesearch/"
GOLD_COLOR	= 0xFFFEE3AE

BOARD_WIDTH = 700
window = {
	"name" : "PrivateShopSearchDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : 365,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : 350,
				
			"title" : "Event Takvimi",
			
			"children" :
			(
				{
					"name" : "arkaplanss",
					"type" : "image",
					"x" : 397,
					"y" : 30+9+0,
					"image" : ROOT_PATH+"furkotakvim/arkaa.jpg",
				},
				{
					"name" : "LeftTop",
					"type" : "image",
					"x" : 133-115,
					"y" : 36,
					"image" : LOCALE_PATH+"private_mainboxlefttop.sub",
				},
				{
					"name" : "RightTop",
					"type" : "image",
					"x" : 659-115-238+75,
					"y" : 36,
					"image" : LOCALE_PATH+"private_mainboxrighttop.sub",
				},
				{
					"name" : "LeftBottom",
					"type" : "image",
					"x" : 133-115,
					"y" : 320,
					"image" : LOCALE_PATH+"private_mainboxleftbottom.sub",
				},
				{
					"name" : "RightBottom",
					"type" : "image",
					"x" : 659-115-238+75,
					"y" : 320,
					"image" : LOCALE_PATH+"private_mainboxrightbottom.sub",
				},
				{
					"name" : "leftcenterImg",
					"type" : "expanded_image",
					"x" : 133-115,
					"y" : 52,
					"image" : LOCALE_PATH+"private_leftcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 15),
				},
				{
					"name" : "rightcenterImg",
					"type" : "expanded_image",
					"x" : 658-115-238+75,
					"y" : 52,
					"image" : LOCALE_PATH+"private_rightcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 15),
				},
				{
					"name" : "topcenterImg",
					"type" : "expanded_image",
					"x" : 149-115+73,
					"y" : 36,
					"image" : LOCALE_PATH+"private_topcenterImg.tga",
					"rect" : (5.0, 0.0, 15, 0),
				},
				{
					"name" : "bottomcenterImg",
					"type" : "expanded_image",
					"x" : 149-115+72,
					"y" : 320,
					"image" : LOCALE_PATH+"private_bottomcenterImg.tga",
					"rect" : (5.0, 0.0, 15, 0),
				},
				{
					"name" : "centerImg",
					"type" : "expanded_image",
					"x" : 149-115+65,
					"y" : 52,
					"image" : LOCALE_PATH+"private_centerImg.tga",
					"rect" : (0.0, 0.0, 15, 15),
				},
				{
					"name" : "eventcann",
					"type" : "image",
					"x" : 133+210+3+65,
					"y" : 30+9,
					# "image" : ROOT_PATH+"furkotakvim/baslik.tga",
					'children': 
					(	
						{
							'name': 'eventname',
							'type': 'text',
							# 'text': 'Test',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': 0,
							'y': 3,
						},
					),
				},
				
				{
					"name" : "eventno",
					"type" : "text",
					"x" : 133+210+15+65,
					"y" : 65,
					# "text" : "Tür : ",
				},

				{
					"name" : "eventdrop",
					"type" : "text",
					"x" : 133+210+15+65,
					"y" : 80+4,
					# "text" : "Drop : ",
				},
				
				{
					"name" : "eventlevel",
					"type" : "text",
					"x" : 133+210+15+65,
					"y" : 95+8,
					# "text" : "Seviye Aralýðý : ",
				},
				
				{
					"name" : "sunucusaats",
					"type" : "text",
					"x" : 133+210+15+65,
					"y" : 110+12,
					# "text" : "Sunucu Saati : ",
					'children': 
					(	
						{
							'name': 'sunucusaat',
							'type': 'text',
							# 'text': 'Test',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': 95,
							'y': 0,
						},
					),
				},
				{
					"name" : "eventcfuko",
					"type" : "image",
					"x" : 133+210+3+65,
					"y" : 210,
					# "image" : ROOT_PATH+"furkotakvim/baslik.tga",
					'children': 
					(	
						{
							'name': 'girisitemtext',
							'type': 'text',
							# 'text': 'Düþürülebilecek Eþyalar',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': 0,
							'y': 3,
						},
					),
				},
				{
					"name" : "eventbilgi",
					"type" : "image",
					"x" : 20,
					"y" : 30+9,
					"image" : ROOT_PATH+"furkotakvim/baslik.png",
					'children': 
					(	
						{
							'name': 'textck',
							'type': 'text',
							'text': '#Baþlangýç Günü#',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': -130,
							'y': 3,
						},
						{
							'name': 'textck1',
							'type': 'text',
							'text': '    	  	#Event Bilgileri#',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': -20,
							'y': 3,
						},
						{
							'name': 'textck',
							'type': 'text',
							'text': '#Baþlangýç#',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': 90,
							'y': 3,
						},
						{
							'name': 'textck',
							'type': 'text',
							'text': '#Bitiþ#',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': 145,
							'y': 3,
						},
					),
				},
				{
					"name" : "girisslot",
					"type" : "grid_table",

					"start_index" : 0,

					"x" : 133+210+15+60+65,
					"y" : 240,

					"x_count" : 1,
					"y_count" : 1,
					"x_step" : 32,
					"y_step" : 32,
					"x_blank" : 0,
					"y_blank" : 0,

					# "image" : "d:/ymir work/ui/public/slot_base.sub",
				},
				
				{
					"name" : "info_ScrollBar",
					"type" : "scrollbar",

					"x" : 325+55,
					"y" : 46,
					"size" : 36 * 7 + 5 * 8,
				},
				
			),
		},
	),
}
