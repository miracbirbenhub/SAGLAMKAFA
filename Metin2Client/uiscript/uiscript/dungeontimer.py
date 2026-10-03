import uiScriptLocale
import item
import app
import localeInfo

LOCALE_PATH = "d:/ymir work/ui/privatesearch/"
GOLD_COLOR	= 0xFFFEE3AE

BOARD_WIDTH = 545
window = {
	"name" : "PrivateShopSearchDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : 350,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : 350,
				
			"title" : "Takip Sistemi",
			
			"children" :
			(

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
					"x" : 659-115-238,
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
					"x" : 659-115-238,
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
					"x" : 658-115-238,
					"y" : 52,
					"image" : LOCALE_PATH+"private_rightcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 15),
				},
				{
					"name" : "topcenterImg",
					"type" : "expanded_image",
					"x" : 149-115,
					"y" : 36,
					"image" : LOCALE_PATH+"private_topcenterImg.tga",
					"rect" : (0.0, 0.0, 15, 0),
				},
				{
					"name" : "bottomcenterImg",
					"type" : "expanded_image",
					"x" : 149-115,
					"y" : 320,
					"image" : LOCALE_PATH+"private_bottomcenterImg.tga",
					"rect" : (0.0, 0.0, 15, 0),
				},
				{
					"name" : "centerImg",
					"type" : "expanded_image",
					"x" : 149-115,
					"y" : 52,
					"image" : LOCALE_PATH+"private_centerImg.tga",
					"rect" : (0.0, 0.0, 15, 15),
				},
				#######
				{
					"name" : "LeftTopInfo",
					"type" : "image",
					"x" : 133+210,
					"y" : 36,
					"image" : LOCALE_PATH+"private_mainboxlefttop.sub",
				},
				{
					"name" : "leftcenterInfoImg",
					"type" : "expanded_image",
					"x" : 133+210,
					"y" : 52,
					"image" : LOCALE_PATH+"private_leftcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 15),
				},
				{
					"name" : "LeftBottomInfo",
					"type" : "image",
					"x" : 133+210,
					"y" : 320,
					"image" : LOCALE_PATH+"private_mainboxleftbottom.sub",
				},
				
				{
					"name" : "topcenterImgInfo",
					"type" : "expanded_image",
					"x" : 149+210,
					"y" : 36,
					"image" : LOCALE_PATH+"private_topcenterImg.tga",
					"rect" : (0.0, 0.0, 8, 0),
				},
				{
					"name" : "bottomcenterImgInfo",
					"type" : "expanded_image",
					"x" : 149+210,
					"y" : 320,
					"image" : LOCALE_PATH+"private_bottomcenterImg.tga",
					"rect" : (0.0, 0.0, 8, 0),
				},
				{
					"name" : "centerImgInfo",
					"type" : "expanded_image",
					"x" : 149+210,
					"y" : 52,
					"image" : LOCALE_PATH+"private_centerImg.tga",
					"rect" : (0.0, 0.0, 8, 15),
				},
				{
					"name" : "rightcenterImg",
					"type" : "expanded_image",
					"x" : 149+210+8*19-1,
					"y" : 52,
					"image" : LOCALE_PATH+"private_rightcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 15),
				},
				{
					"name" : "RightTop",
					"type" : "image",
					"x" : 149+210+8*19,
					"y" : 36,
					"image" : LOCALE_PATH+"private_mainboxrighttop.sub",
				},
				{
					"name" : "RightBottom",
					"type" : "image",
					"x" : 149+210+8*19,
					"y" : 320,
					"image" : LOCALE_PATH+"private_mainboxrightbottom.sub",
				},
				###########
				{
					"name" : "dungeonnameimage",
					"type" : "image",
					"x" : 133+210+3,
					"y" : 30+9,
					"image" : "dungeontimer/baslik.tga",
					'children': 
					(	
						{
							'name': 'mapname',
							'type': 'text',
							'text': 'Test',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': 0,
							'y': 3,
						},
					),
				},	
				
				{
					"name" : "dungeontype",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 65,
					"text" : "Tür : ",
				},

				{
					"name" : "dungeontype2",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 80,
					"text" : "Tip : ",
				},
				
				{
					"name" : "dungeonlevel",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 95,
					"text" : "Seviye : ",
				},
				
				{
					"name" : "dungeongroup",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 110,
					"text" : "Grup Limiti : ",
				},
				
				{
					"name" : "dungeoncd",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 125,
					"text" : "Bekleme Süresi : ",
				},
				
				{
					"name" : "dungeoncd2",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 140,
					"text" : "Tamamlama Süresi : ",
				},
				
				{
					"name" : "dungeongiris",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 155,
					"text" : "Giriþ : ",
				},
				
				{
					"name" : "dungeonguclu",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 170,
					"text" : "Saldýrý Efsunlarý : ",
				},
				
				{
					"name" : "dungeondirenc",
					"type" : "text",
					"x" : 133+210+15,
					"y" : 185,
					"text" : "Savunma Efsunlarý : ",
				},
				{
					"name" : "dungeonnameimage",
					"type" : "image",
					"x" : 133+210+3,
					"y" : 210,
					"image" : "dungeontimer/baslik.tga",
					'children': 
					(	
						{
							'name': 'girisitemtext',
							'type': 'text',
							'text': 'Giriþ Ýtemi',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': 0,
							'y': 3,
						},
					),
				},
				{
					"name" : "girisslot",
					"type" : "grid_table",

					"start_index" : 0,

					"x" : 133+210+15+60,
					"y" : 240,

					"x_count" : 1,
					"y_count" : 1,
					"x_step" : 32,
					"y_step" : 32,
					"x_blank" : 0,
					"y_blank" : 0,

					"image" : "d:/ymir work/ui/public/slot_base.sub",
				},
				
				{
					"name" : "info_ScrollBar",
					"type" : "scrollbar",

					"x" : 325,
					"y" : 40,
					"size" : 36 * 7 + 5 * 8,
				},
				
				{
					"name" : "tp_button",
					"type" : "button",
					"x" : 133+210+15+5,
					"y" : 290,
					
					"default_image" : "d:/ymir work/ui/buton/1.tga",
					"over_image" : "d:/ymir work/ui/buton/2.tga",
					"down_image" : "d:/ymir work/ui/buton/3.tga",
					"text" : "Iþýnlan",
					"tooltip_text" : "Seçili zindana ýþýnlanmaný saðlar",
				},
			),
		},
	),
}
