import uiscriptlocale
import item
import app
import localeinfo

LOCALE_PATH = "d:/ymir work/ui/privatesearch/"
ROOT_PATH = "d:/ymir work/ui/public/"
GOLD_COLOR	= 0xFFFEE3AE

BOARD_WIDTH = 340
window = {
	"name" : "biyolog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : 485,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : 485,
				
			"title" : "Biyolog",
			
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
					"y" : 320+130,
					"image" : LOCALE_PATH+"private_mainboxleftbottom.sub",
				},
				{
					"name" : "RightBottom",
					"type" : "image",
					"x" : 659-115-238,
					"y" : 320+130,
					"image" : LOCALE_PATH+"private_mainboxrightbottom.sub",
				},
				{
					"name" : "leftcenterImg",
					"type" : "expanded_image",
					"x" : 133-115,
					"y" : 52,
					"image" : LOCALE_PATH+"private_leftcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 23),
				},
				{
					"name" : "rightcenterImg",
					"type" : "expanded_image",
					"x" : 658-115-238,
					"y" : 52,
					"image" : LOCALE_PATH+"private_rightcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 23),
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
					"y" : 320+130,
					"image" : LOCALE_PATH+"private_bottomcenterImg.tga",
					"rect" : (0.0, 0.0, 15, 0),
				},
				{
					"name" : "centerImg",
					"type" : "expanded_image",
					"x" : 149-115,
					"y" : 52,
					"image" : LOCALE_PATH+"private_centerImg.tga",
					"rect" : (0.0, 0.0, 15, 23),
				},
				{
					"name" : "ilkslot",
					"type" : "image",

					"x" : 80,
					"y" : 50,

					"image" : "biyolog/biyoslot.tga",
					
					"children" :
					(
					
						{
							"name" : "ilkitem",
							"type" : "slot",


							"x" : 4,
							"y" : 4,
							
							"width" : 32,
							"height" : 32,
							
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32,},),
						},					
					),
				},
				
				{
					"name" : "i1",
					"type" : "image",


					"x" : 130,
					"y" : 65,


					"image" : LOCALE_PATH + "private_last_next_btn_01.sub",
				},
				
				{
					"name" : "ruhslot",
					"type" : "image",

					"x" : 150,
					"y" : 50,

					"image" : "biyolog/biyoslot.tga",
					
					"children" :
					(
					
						{
							"name" : "ruhtasi",
							"type" : "slot",


							"x" : 4,
							"y" : 4,
							
							"width" : 32,
							"height" : 32,
							
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32,},),
						},					
					),
				},
				
				{
					"name" : "i2",
					"type" : "image",


					"x" : 200,
					"y" : 65,


					"image" : LOCALE_PATH + "private_last_next_btn_01.sub",
				},
				
				{
					"name" : "hediyeslot",
					"type" : "image",

					"x" : 220,
					"y" : 50,

					"image" : "biyolog/biyoslot.tga",
					
					"children" :
					(
					
						{
							"name" : "hediye",
							"type" : "slot",


							"x" : 4,
							"y" : 4,
							
							"width" : 32,
							"height" : 32,
							
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32,},),
						},					
					),
				},
				
				{
					"name" : "adetler",
					"type" : "image",


					"x" : 105,
					"y" : 105,


					"image" : "d:/ymir work/ui/public/Parameter_Slot_05.sub",
					
					"children" :
					(
						{
							"name" : "adettext",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"text" : "0 - 10",

							"all_align" : "center",
						},
					),
				},
				
				{
					"name" : "zaman",
					"type" : "image",


					"x" : 105,
					"y" : 130,


					"image" : "d:/ymir work/ui/public/Parameter_Slot_05.sub",
					
					"children" :
					(
						{
							"name" : "zamantext",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"text" : "Verilebilir",

							"all_align" : "center",
						},
					),
				},
				
				{
					"name" : "bonusimg",
					"type" : "image",


					"x" : 85,
					"y" : 160,


					"image" : ROOT_PATH + "public_intro_btn/raceName_btn.sub",
					
					"children" :
					(
						{
							"name" : "bonustextt",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"text" : "Bonuslar",

							"all_align" : "center",
						},
					),
				},
				
				{
					"name" : "bonus1",
					"type" : "text",
					"x" : 105,
					"y" : 190,
					"text" : "Bonus 1 : Hareket Hýzý %10",
				},
				
				{
					"name" : "bonus2",
					"type" : "text",
					"x" : 105,
					"y" : 205,
					"text" : "Bonus 2 : Saldýrý Deðeri +50",
				},
				
				{
					"name" : "bonus3",
					"type" : "text",
					"x" : 105,
					"y" : 220,
					"text" : "Bonus 3 : Savunma +100",
				},
				
				{
					"name" : "sep",
					"type" : "text",
					"x" : 50,
					"y" : 235,
					"text" : "_______________________________________________",
				},
				
				
				{
					"name" : "info1slot",
					"type" : "image",

					"x" : 60,
					"y" : 260,

					"image" : "biyolog/biyoslot.tga",
					
					"children" :
					(
					
						{
							"name" : "info1",
							"type" : "slot",


							"x" : 4,
							"y" : 4,
							
							"width" : 32,
							"height" : 32,
							
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32,},),
						},					
					),
				},
				
				{
					"name" : "bonus111",
					"type" : "text",
					"x" : 150,
					"y" : 260,
					"text" : "|cffFDD017|H|h" + "Araþtýrmacýnýn Özütü",
				},
				
				{
					"name" : "bonus11",
					"type" : "text",
					"x" : 110,
					"y" : 275,
					"text" : "Biyolog görevinin %100 geçmesini saðlar",
				},
				
				{
					"name" : "info2slot",
					"type" : "image",

					"x" : 60,
					"y" : 305,

					"image" : "biyolog/biyoslot.tga",
					
					"children" :
					(
					
						{
							"name" : "info2",
							"type" : "slot",


							"x" : 4,
							"y" : 4,
							
							"width" : 32,
							"height" : 32,
							
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32,},),
						},					
					),
				},
				
				{
					"name" : "bonus222",
					"type" : "text",
					"x" : 150,
					"y" : 300,
					"text" : "|cffFDD017|H|h" + "Biyolog Süre Özütü",
				},
				
				{
					"name" : "bonus22",
					"type" : "text",
					"x" : 110,
					"y" : 315,
					"text" : "Biyolog görevinin süresini sýfýrlar",
				},
				
				{
					"name" : "info3slot",
					"type" : "image",

					"x" : 60,
					"y" : 350,

					"image" : "biyolog/biyoslot.tga",
					
					"children" :
					(
					
						{
							"name" : "info3",
							"type" : "slot",


							"x" : 4,
							"y" : 4,
							
							"width" : 32,
							"height" : 32,
							
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32,},),
						},					
					),
				},
				
				{
					"name" : "bonus333",
					"type" : "text",
					"x" : 150,
					"y" : 340,
					"text" : "|cffFDD017|H|h" + "Biyolog Özütü",
				},
				
				{
					"name" : "bonus33",
					"type" : "text",
					"x" : 110,
					"y" : 355,
					"text" : "Biyolog görevinin süresini sýfýrlar",
				},
				
				{
					"name" : "bonus333",
					"type" : "text",
					"x" : 120,
					"y" : 370,
					"text" : "ve %100 geçmesini saðlar",
				},
				
				{
					"name" : "sep2",
					"type" : "text",
					"x" : 50,
					"y" : 390,
					"text" : "_______________________________________________",
				},
				
				{
					"name" : "gorevver",
					"type" : "button",
					"x" : 100,
					"y" : 420,
					
					"default_image" : "d:/ymir work/ui/buton/1.tga",
					"over_image" : "d:/ymir work/ui/buton/2.tga",
					"down_image" : "d:/ymir work/ui/buton/3.tga",
					"text" : "Görevi Ver",
					"tooltip_text" : "Biyolog görevini ver",
				},
				
				
			),
		},
	),
}
