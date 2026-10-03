window = {
	"name" : "SelectSkill",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH / 2 - 150 ,
	"y" : SCREEN_HEIGHT / 2 - 150,

	"width" : 418,
	"height" : 234,

	"children" :
	(
		{
			"name" : "board",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 418,
			"height" : 234,

			"children" :
			(
			
				{
					"name" : "image",
					"type" : "image",

					"x" : 0,
					"y" : 0,

					"image" : "autoskill/warrior.tga",
					
					"children":
					(
						
						{
							"name" : "Skill_1_Text",
							"type" : "text",

							"x" : 152,
							"y" : 60,

							"text" : "Bedensel Savaþçý",
						},
						
						{
							"name" : "Skill_1",
							"type" : "button",

							"x" : 175,
							"y" : 85,

							"default_image" : "autoskill/accept_btn_0.tga",
							"over_image" : "autoskill/accept_btn_1.tga",
							"down_image" : "autoskill/accept_btn_2.tga",
						},
						
						{
							"name" : "Skill_2_Text",
							"type" : "text",

							"x" : 160,
							"y" : 155,

							"text" : "Zihinsel Savaþçý",
						},
						

						{
							"name" : "Skill_2",
							"type" : "button",

							"x" : 195,
							"y" : 180,

							"default_image" : "autoskill/accept_btn_0.tga",
							"over_image" : "autoskill/accept_btn_1.tga",
							"down_image" : "autoskill/accept_btn_2.tga",
						},
					),
				},
			),
		},
	),
}
