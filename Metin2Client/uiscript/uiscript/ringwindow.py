# import uiScriptLocale
# import item

# window = {
	# "name" : "RingWindow",

	# "x" : SCREEN_WIDTH - 175 - 140 - 175,
	# "y" : SCREEN_HEIGHT - 37 - 565,

	# "style" : ("movable", "float",),

	# "width" : 175,
	# "height" : 230,

	# "children" :
	# (
		# {
			# "name" : "board",
			# "type" : "board",
			# "style" : ("attach",),

			# "x" : 0,
			# "y" : 0,

			# "width" : 175,
			# "height" : 230,
			
			# "children" :
			# (
				# Title
				# {
					# "name" : "TitleBar",
					# "type" : "titlebar",
					# "style" : ("attach",),

					# "x" : 6,
					# "y" : 6,

					# "width" : 160,
					# "color" : "yellow",

					# "children" :
					# (
						# { "name":"TitleName", "type":"text", "x":80, "y":3, "text":"Yüzük", "text_horizontal_align":"center" },
					# ),
				# },

				# Equipment Slot
				# {
					# "name" : "Costume_Base",
					# "type" : "image",

					# "x" : 10,
					# "y" : 35,
					
					# "image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "ring.png",					

					# "children" :
					# (

						# {
							# "name" : "RingSlot",
							# "type" : "slot",

							# "x" : 3,
							# "y" : 3,

							# "width" : 155,
							# "height" : 187,

							# "slot" : (
										# {"index":item.EQUIPMENT_SPECIAL_RING1, "x":10, "y":7, "width":32, "height":32}, ##
										# {"index":item.EQUIPMENT_SPECIAL_RING2, "x":112, "y":7, "width":32, "height":32}, ##
										# {"index":item.EQUIPMENT_SPECIAL_RING3, "x":90, "y":50, "width":32, "height":32}, ##
										# {"index":item.EQUIPMENT_SPECIAL_RING4, "x":32, "y":50, "width":32, "height":32}, ##
										# {"index":item.EQUIPMENT_SPECIAL_RING5, "x":32, "y":95, "width":32, "height":32}, ##
										# {"index":item.EQUIPMENT_SPECIAL_RING6, "x":90, "y":95, "width":32, "height":32}, ##
										# {"index":item.EQUIPMENT_SPECIAL_RING7, "x":10, "y":138, "width":32, "height":32}, ##
										# {"index":item.EQUIPMENT_SPECIAL_RING8, "x":112, "y":138, "width":32, "height":32}, ##
										
									# ),
						# },
					# ),
				# },

			# ),
		# },
	# ),
# }
