import uiscriptlocale
import item
import app
import localeinfo

BOARD_WIDTH = 320
BOARD_HEIGHT = 250+70
window = {
	"name" : "dailyreward",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
				
			"title" : "Günlük Ödül",
			
			"children" :
			(
				{
					"name" : "itemslot",
					"type" : "image",
				
					"x" : 10,
					"y" : 35,
				
					"image" : "dailyreward/slot.tga",
					
					"children" :
					(
					
						{
							"name" : "item1",
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
					"name" : "gun_bg",
					"type" : "image",
					
					"x" : 16-5,
					"y" : 90-8,
					
					"image" : "d:/ymir work/ui/public/xsmall_button_01.sub",
				},
				{
					"name" : "gun",
					"type" : "text",
					
					"x" : 16,
					"y" : 90-6,
					
					"text" : "Gün 1",
				},
				{
					"name" : "time_bg",
					"type" : "image",
				
					"x" : 16,
					"y" : 110,
				
					"image" : "d:/ymir work/ui/game/cube/cube_menu_tab1.sub",
				},
				{
					"name" : "time",
					"type" : "text",
					
					"x" : 20,
					"y" : 110,
					
					"text" : "Ödül Alýndý",
				},
				{
					"name" : "gun_bg2",
					"type" : "image",
					
					"x" : 16+10+32-5,
					"y" : 90-8,
					
					"image" : "d:/ymir work/ui/public/xsmall_button_01.sub",
				},
				{
					"name" : "gun2",
					"type" : "text",
					
					"x" : 16+10+32,
					"y" : 90-6,
					
					"text" : "Gün 2",
				},
				{
					"name" : "gun_bg3",
					"type" : "image",
					
					"x" : 16+20+32*2-5,
					"y" : 90-8,
					
					"image" : "d:/ymir work/ui/public/xsmall_button_01.sub",
				},
				{
					"name" : "gun3",
					"type" : "text",
					
					"x" : 16+20+32*2,
					"y" : 90-6,
					
					"text" : "Gün 3",
				},
				{
					"name" : "gun_bg4",
					"type" : "image",
					
					"x" : 16+30+32*3-5,
					"y" : 90-8,
					
					"image" : "d:/ymir work/ui/public/xsmall_button_01.sub",
				},
				{
					"name" : "gun4",
					"type" : "text",
					
					"x" : 16+30+32*3,
					"y" : 90-6,
					
					"text" : "Gün 4",
				},
				{
					"name" : "gun_bg5",
					"type" : "image",
					
					"x" : 16+40+32*4-5,
					"y" : 90-8,
					
					"image" : "d:/ymir work/ui/public/xsmall_button_01.sub",
				},
				{
					"name" : "gun5",
					"type" : "text",
					
					"x" : 16+40+32*4,
					"y" : 90-6,
					
					"text" : "Gün 5",
				},
				{
					"name" : "gun_bg6",
					"type" : "image",
					
					"x" : 16+50+32*5-5,
					"y" : 90-8,
					
					"image" : "d:/ymir work/ui/public/xsmall_button_01.sub",
				},
				{
					"name" : "gun6",
					"type" : "text",
					
					"x" : 16+50+32*5,
					"y" : 90-6,
					
					"text" : "Gün 6",
				},
				{
					"name" : "gun_bg7",
					"type" : "image",
					
					"x" : 16+60+32*6-5,
					"y" : 90-8,
					
					"image" : "d:/ymir work/ui/public/xsmall_button_01.sub",
				},
				{
					"name" : "gun7",
					"type" : "text",
					
					"x" : 16+60+32*6,
					"y" : 90-6,
					
					"text" : "Gün 7",
				},
				{
					"name" : "itemslot2",
					"type" : "image",
				
					"x" : 20+32,
					"y" : 35,
				
					"image" : "dailyreward/slot.tga",
					
					"children" :
					(
					
						{
							"name" : "item2",
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
					"name" : "itemslot3",
					"type" : "image",
				
					"x" : 30+32*2,
					"y" : 35,
				
					"image" : "dailyreward/slot.tga",
					
					"children" :
					(
					
						{
							"name" : "item3",
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
					"name" : "itemslot4",
					"type" : "image",
				
					"x" : 40+32*3,
					"y" : 35,
				
					"image" : "dailyreward/slot.tga",
					
					"children" :
					(
					
						{
							"name" : "item4",
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
					"name" : "itemslot5",
					"type" : "image",
				
					"x" : 50+32*4,
					"y" : 35,
				
					"image" : "dailyreward/slot.tga",
					
					"children" :
					(
					
						{
							"name" : "item5",
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
					"name" : "itemslot6",
					"type" : "image",
				
					"x" : 60+32*5,
					"y" : 35,
				
					"image" : "dailyreward/slot.tga",
					
					"children" :
					(
					
						{
							"name" : "item6",
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
					"name" : "DesignTop","type" : "image","style" : ("attach",),"x" : 10+0, "y" : 135,"image" : "d:/ymir work/battle_pass/kaplanpara.png",	
				},
				{
					"name" : "itemslot7",
					"type" : "image",
				
					"x" : 70+32*6,
					"y" : 35,
				
					"image" : "dailyreward/slot.tga",
					
					"children" :
					(
					
						{
							"name" : "item7",
							"type" : "slot",
				
				
							"x" : 4,
							"y" : 4,
							
							"width" : 32,
							"height" : 32,
							
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32,},),
						},					
					),
				},
			),
		},
	),
}
