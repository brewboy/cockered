	object_const_def
	const_export PITBACKROOM_CLERK
	const_export PITBACKROOM_DOORMAN
	const_export PITBACKROOM_STAIRS_GUARD
	const_export PITBACKROOM_LOSER
	const_export PITBACKROOM_REGULAR

PitBackRoom_Object:
	db $f ; border block

	def_warp_events
	warp_event  4,  9, LAST_MAP, 9
	warp_event  5,  9, LAST_MAP, 9

	def_bg_events
	bg_event  7,  0, TEXT_PITBACKROOM_BOARD

	def_object_events
	object_event  1,  1, SPRITE_GAMBLER, STAY, DOWN, TEXT_PITBACKROOM_CLERK
	object_event  6,  7, SPRITE_ROCKER, STAY, LEFT, TEXT_PITBACKROOM_DOORMAN
	object_event 10,  2, SPRITE_BIKER, STAY, DOWN, TEXT_PITBACKROOM_STAIRS_GUARD
	object_event  9,  4, SPRITE_BALDING_GUY, STAY, DOWN, TEXT_PITBACKROOM_LOSER
	object_event  2,  6, SPRITE_MIDDLE_AGED_MAN, STAY, DOWN, TEXT_PITBACKROOM_REGULAR

	def_warps_to PIT_BACK_ROOM
