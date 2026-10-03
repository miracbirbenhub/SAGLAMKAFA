import localeInfo
import uiScriptLocale

LOCALE_PATH = uiScriptLocale.WINDOWS_PATH

MAINBOARD_WIDTH = 244
MAINBOARD_HEIGHT = 300#361

LABEL_START_X = 159
LABEL_START_Y = 120+15 #
LABEL_START_Y2 = 120 #
LABEL_START_Y3 = 120+5 #
LABEL_WIDTH = 50
LABEL_HEIGHT = 5 #
LABEL_HEIGHT2 = 20
LABEL_GAP = LABEL_HEIGHT+5 # 
LABEL_GAP2 = LABEL_HEIGHT+5 # 
LABEL_GAP3 = 10
LABEL_NAME_POS_X = 15 #
TITLE_BAR_POS_X = 30 #
TITLE_BAR_WIDTH = 163

window = {
	"name" : "CharacterDetailsWindow",
	"style" : ("float",),
	
	"x" : 274, #24+253-3,
	"y" : (SCREEN_HEIGHT - 398) / 2,

	"width" : MAINBOARD_WIDTH,
	"height" : MAINBOARD_HEIGHT,
	
	"children" :
	(
		## MainBoard
		{
			"name" : "MainBoard",
			"type" : "board",
			"style" : ("attach","ltr"),
			
			## CharacterWindow.py 영향 받음
			"x" : 0,
			"y" : 0,

			"width" : MAINBOARD_WIDTH,
			"height" : MAINBOARD_HEIGHT,
			
			"children" :
			(
				## 타이틀바
				# {
					# "name" : "ibo_adamdir",
					# "type" : "image",
					# "image" : "ibowork/switch_background.png",
					# "x" : 5,
					# "y" : 35,
				# },
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 7,

					"width" : MAINBOARD_WIDTH - 13,
					
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : 0, "text": localeInfo.DETAILS_TITLE, "all_align":"center" },
					),
				},
				## 스크롤 바
				{
					"name" : "ScrollBar",
					"type" : "scrollbar",

					"x" : 30,
					"y" : 44,
					"size" : MAINBOARD_HEIGHT - 65,
					"horizontal_align" : "right",
				},
				{
					"name" : "istatik", "type" : "thinboard_circle", "x" : 30, "y" : 35, "width" : 175, "height" : 20,
					
					"children" : ( 
						{ "name" : "istatik_text", "type" : "text", "x" : 0, "y" : 0, "text" : "Istatistik", "all_align" : "center", },
					),
				},
				{
					"name" : "bosses_title_bg", "type" : "thinboard_circle", "x" : 35, "y" : 58+24*0, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "bosses_text", "type" : "text", "x" : 0, "y" : 0, "text" : "Patron", "all_align" : "center", },
					),
				},
				{
					"name" : "bosses_kills_bg", "type" : "thinboard_circle", "x" : 35+120+2, "y" : 58+24*0, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "bosses_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},	
				{
					"name" : "stones_title_bg", "type" : "thinboard_circle", "x" : 35, "y" : 58+24*1, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "stones_text", "type" : "text", "x" : 0, "y" : 0, "text" : "Metin", "all_align" : "center", },
					),
				},
				{
					"name" : "stones_kills_bg", "type" : "thinboard_circle", "x" : 35+120+2, "y" : 58+24*1, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "stones_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},	

				## 호리즌 바
				{ 
					"name" : "horizontalbar0", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*0, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName0", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar1", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*1, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName1", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar2", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*2, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName2", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar3", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*3, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName3", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar4", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*4, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName4", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar5", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*5, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName5", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar6", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*6, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName6", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar7", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*7, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName7", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar8", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*8, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName8", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar9", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*9, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName9", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar10", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*10, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName10", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar11", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*11, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName11", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar12", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*12, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName12", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar13", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*13, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName13", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},
				{ 
					"name" : "horizontalbar14", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":LABEL_START_Y2+LABEL_GAP2*14, "width":TITLE_BAR_WIDTH, "height" : 20,
					"children" : ( { "name" : "horizontalbarName14", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
				},


				{
					"name" : "label0", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*0, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue0", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label1", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*1, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue1", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label2", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*2, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue2", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label3", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*3, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue3", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label4", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*4, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue4", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label5", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*5, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue5", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label6", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*6, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue6", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label7", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*7, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue7", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label8", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*8, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue8", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label9", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*9, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue9", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label10", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*10, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue10", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label11", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*11, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue11", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label12", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*12, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue12", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label13", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*13, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue13", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},
				{
					"name" : "label14", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : LABEL_START_Y3+LABEL_GAP3*14, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT2,
					"children" : ( 
						{ "name" : "labelvalue14", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
					),
				},

				## 버튼
				{ 
							"name" : "labelname0", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*0, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},
				{ 
							"name" : "labelname1", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*1, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},
				{ 
							"name" : "labelname2", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*2, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},
				{ 
							"name" : "labelname3", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*3, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname4", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*4, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname5", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*5, 
							
							"text" : "", 
							
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname6", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*6, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname7", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*7, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname8", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*8, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname9", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*9, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname10", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*10, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname11", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*11, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},	
				{ 
							"name" : "labelname12", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*12, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},
				{ 
							"name" : "labelname13", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*13, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},
				{ 
							"name" : "labelname14", "type" : "button",
							"x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*14, 
							
							"text" : "", 
							
							"default_image" : "locale/tr/ui/windows/details_button.tga",
							"over_image" : "locale/tr/ui/windows/details_button.tga",
							"down_image" : "locale/tr/ui/windows/details_button.tga",
				},

			),
		}, ## MainBoard End
	),
}