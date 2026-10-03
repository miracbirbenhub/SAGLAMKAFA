import uiScriptLocale
window = {
	'name': 'ChangerWindow',
	'style': ('movable', 'float'),
	'x': SCREEN_WIDTH - 400,
	'y': 56000 / SCREEN_HEIGHT,
	'width': 0,
	'height': 0,
	'children': 
	(
		{
			'name': 'Board',
			'type': 'board',
			'style': ('attach',),
			'x': 0,
			'y': 0,
			'width': 0,
			'height': 0,
			'children': 
			(
				{
					'name': 'TitleBar',
					'type': 'titlebar',
					'style': ('attach',),
					'x': 8,
					'y': 8,
					'width': 0,
					'color': 'red',
					'children': 
					(	
						{
							'name': 'TitleName',
							'type': 'text',
							'text': 'Efsun Ekle',
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
							'x': 0,
							'y': 3,
						},
					),
				},
				{
					'name': 'AcceptButton',
					'type': 'button',
					'x': -35,
					'y': 35,
					'text': uiScriptLocale.OK,
					'horizontal_align': 'center',
					'vertical_align': 'bottom',
					'default_image': 'd:/ymir work/ui/public/Middle_Button_01.sub',
					'over_image': 'd:/ymir work/ui/public/Middle_Button_02.sub',
					'down_image': 'd:/ymir work/ui/public/Middle_Button_03.sub',
				},
				{
					'name': 'CancelButton',
					'type': 'button',
					'x': 35,
					'y': 35,
					'text': uiScriptLocale.CANCEL,
					'horizontal_align': 'center',
					'vertical_align': 'bottom',
					'default_image': 'd:/ymir work/ui/public/Middle_Button_01.sub',
					'over_image': 'd:/ymir work/ui/public/Middle_Button_02.sub',
					'down_image': 'd:/ymir work/ui/public/Middle_Button_03.sub',
				},
			),
		},
	),
}