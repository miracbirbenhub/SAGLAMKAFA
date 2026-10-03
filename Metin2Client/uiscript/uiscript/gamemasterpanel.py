import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"

TEMPORARY_X = +13
TEXT_TEMPORARY_X = -10
BUTTON_TEMPORARY_X = 5
PVP_X = -10

window = {
	"name" : "SystemOptionDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 280,
	"height" : 460/2+250,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 280,
			"height" : 460/2+250,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 265,
					"color" : "gray",

					"children" :
					(
						{ 
						"name":"titlename", "type":"text", "x":0, "y":3, 
						"horizontal_align":"center", "text_horizontal_align":"center",
						"text" : "Game Master Paneli",
						 },
						 {
							"name" : "info_button",
							"type" : "button",

							"x" : 3,
							"y" : 3,

							#"default_image":"d:/ymir work/ui/pattern/q_mark_01.tga",
							#"over_image":"d:/ymir work/ui/pattern/q_mark_02.tga",
							#"down_image":"d:/ymir work/ui/pattern/q_mark_01.tga",
						},
					),
				},
				## MAVI RUH DEAKTIF BUTTONS ##
				#{
				#	"name" : "material_button",
				#	"type" : "button",

				#	"x" : 20,
				#	"y" : 45,

				#	"text" : "(30K) Dönüþüm Malzemeleri",

				#	"default_image":"d:/ymir work/ui/buton/offical_button.tga",
				#	"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
				#	"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				#},
				#{
				#	"name" : "chest_button",
				#	"type" : "button",

				#	"x" : 20,
				#	"y" : 75,

				#	"text" : "(30K) Sandýklar",

				#	"default_image":"d:/ymir work/ui/buton/offical_button.tga",
				#	"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
				#	"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				#},
				#{
				#	"name" : "stone_button",
				#	"type" : "button",

				#	"x" : 20,
				#	"y" : 105,

				#	"text" : "(30K) Taþlar",

				#	"default_image":"d:/ymir work/ui/buton/offical_button.tga",
				#	"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
				#	"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				#},
				## MAVI RUH DEAKTIF BUTTONS ##
				{
					"name" : "heroman_button",
					"type" : "button",

					"x" : 20,
					"y" : 45,

					"text" : "Kahraman Yap",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "kick_button",
					"type" : "button",

					"x" : 20,
					"y" : 75,

					"text" : "Oyundan AT",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "cleaninventory_button",
					"type" : "button",

					"x" : 20,
					"y" : 105,

					"text" : "Envanter Temizle",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "levelme_button",
					"type" : "button",

					"x" : 20,
					"y" : 135,

					"text" : "Seviye",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "full_button",
					"type" : "button",

					"x" : 20,
					"y" : 165,

					"text" : "Efsunlu Ekipmanlar",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "skillperfect_button",
					"type" : "button",

					"x" : 20,
					"y" : 195,

					"text" : "Tüm Becelerilerimi P",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "skybox_button",
					"type" : "button",

					"x" : 20,
					"y" : 225,

					"text" : "HWID Ban At",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "oxmap_button",
					"type" : "button",

					"x" : 20,
					"y" : 255,

					"text" : "Ox Haritasý",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "notice_button",
					"type" : "button",

					"x" : 20,
					"y" : 285,

					"text" : "Duyuru",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "eternal_button",
					"type" : "button",

					"x" : 20,
					"y" : 315,

					"text" : "Ölümsüzlük",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "leveluser_button",
					"type" : "button",

					"x" : 20,
					"y" : 345,

					"text" : "Seviye",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "invisible_button",
					"type" : "button",

					"x" : 20,
					"y" : 375,

					"text" : "Görünmezlik",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "npc_button",
					"type" : "button",

					"x" : 20,
					"y" : 405,

					"text" : "Npc Çaðýr",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
				{
					"name" : "mute_button",
					"type" : "button",

					"x" : 20,
					"y" : 435,

					"text" : "Mute AT",

					"default_image":"d:/ymir work/ui/buton/offical_button.tga",
					"over_image":"d:/ymir work/ui/buton/offical_button_bastim.tga",
					"down_image":"d:/ymir work/ui/buton/offical_button.tga",
				},
#################################################### INFO ####################################################
				{
					"name" : "gminfo1",
					"type" : "button",

					"x" : 180,
					"y" : 48,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "userinfo1",
					"type" : "button",

					"x" : 225,
					"y" : 48,

					"text" : "",
					"tooltip_text" : "|cff00ff00Herkes Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/user_info.tga",
					"over_image":"d:/ymir work/ui/user_info.tga",
					"down_image":"d:/ymir work/ui/user_info.tga",
				},
				{
					"name" : "gminfo2",
					"type" : "button",

					"x" : 180,
					"y" : 78,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "userinfo2",
					"type" : "button",

					"x" : 225,
					"y" : 78,

					"text" : "",
					"tooltip_text" : "|cff00ff00Herkes Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/user_info.tga",
					"over_image":"d:/ymir work/ui/user_info.tga",
					"down_image":"d:/ymir work/ui/user_info.tga",
				},
				{
					"name" : "gminfo3",
					"type" : "button",

					"x" : 180,
					"y" : 108,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "gminfo4",
					"type" : "button",

					"x" : 180,
					"y" : 138,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "gminfo5",
					"type" : "button",

					"x" : 180,
					"y" : 168,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "gminfo6",
					"type" : "button",

					"x" : 180,
					"y" : 198,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "gminfo7",
					"type" : "button",

					"x" : 180,
					"y" : 228,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "userinfo7",
					"type" : "button",

					"x" : 225,
					"y" : 228,

					"text" : "",
					"tooltip_text" : "|cff00ff00Herkes Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/user_info.tga",
					"over_image":"d:/ymir work/ui/user_info.tga",
					"down_image":"d:/ymir work/ui/user_info.tga",
				},
				{
					"name" : "gminfo8",
					"type" : "button",

					"x" : 180,
					"y" : 258,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "gminfo9",
					"type" : "button",

					"x" : 180,
					"y" : 288,

					"text" : "",
					"tooltip_text" : "|cff00ff00Herkes Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "gminfo10",
					"type" : "button",

					"x" : 180,
					"y" : 318,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "gminfo11",
					"type" : "button",

					"x" : 180,
					"y" : 348,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "userinfo11",
					"type" : "button",

					"x" : 225,
					"y" : 348,

					"text" : "",
					"tooltip_text" : "|cff00ff00Herkes Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/user_info.tga",
					"over_image":"d:/ymir work/ui/user_info.tga",
					"down_image":"d:/ymir work/ui/user_info.tga",
				},
				{
					"name" : "gminfo12",
					"type" : "button",

					"x" : 180,
					"y" : 378,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "gminfo13",
					"type" : "button",

					"x" : 180,
					"y" : 408,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "userinfo13",
					"type" : "button",

					"x" : 225,
					"y" : 408,

					"text" : "",
					"tooltip_text" : "|cff00ff00Herkes Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/user_info.tga",
					"over_image":"d:/ymir work/ui/user_info.tga",
					"down_image":"d:/ymir work/ui/user_info.tga",
				},
				{
					"name" : "gminfo14",
					"type" : "button",

					"x" : 180,
					"y" : 438,

					"text" : "",
					"tooltip_text" : "|cff00ff00Kiþi Sadece Kendisi Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/gm_info.tga",
					"over_image":"d:/ymir work/ui/gm_info.tga",
					"down_image":"d:/ymir work/ui/gm_info.tga",
				},
				{
					"name" : "userinfo14",
					"type" : "button",

					"x" : 225,
					"y" : 438,

					"text" : "",
					"tooltip_text" : "|cff00ff00Herkes Ýçin Kullanabilir.",

					"default_image":"d:/ymir work/ui/user_info.tga",
					"over_image":"d:/ymir work/ui/user_info.tga",
					"down_image":"d:/ymir work/ui/user_info.tga",
				},
				#################################################### INFO ####################################################
			),
		},
	),
}
