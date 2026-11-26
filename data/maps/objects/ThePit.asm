	object_const_def
	const_export THEPIT_BIKER
	const_export THEPIT_ROCKER
	const_export THEPIT_BLACKBELT
	const_export THEPIT_BOOKIE
	const_export THEPIT_BIRD1
	const_export THEPIT_BIRD2
	const_export THEPIT_BEAUTY
	const_export THEPIT_MIDDLE_AGED_MAN
	const_export THEPIT_BALDING_GUY
	const_export THEPIT_GAMBLER

ThePit_Object:
	db $2e ; border block

	def_warp_events
	warp_event 17,  2, PIT_BACK_ROOM, 3

	def_bg_events

	def_object_events
	; the undercard, fought in this order
	object_event 17,  9, SPRITE_BIKER, STAY, LEFT, TEXT_THEPIT_BIKER
	object_event 17, 12, SPRITE_ROCKER, STAY, LEFT, TEXT_THEPIT_ROCKER
	object_event 12, 14, SPRITE_HIKER, STAY, UP, TEXT_THEPIT_BLACKBELT
	; the bookie, behind his desk
	object_event  2, 14, SPRITE_GENTLEMAN, STAY, UP, TEXT_THEPIT_BOOKIE
	; tonight's fight, and the crowd round the ring
	object_event  8,  7, SPRITE_MONSTER, STAY, RIGHT, TEXT_THEPIT_BIRD1
	object_event 11,  7, SPRITE_MONSTER, STAY, LEFT, TEXT_THEPIT_BIRD2
	object_event  7,  3, SPRITE_BEAUTY, STAY, DOWN, TEXT_THEPIT_BEAUTY
	object_event 12,  3, SPRITE_MIDDLE_AGED_MAN, STAY, DOWN, TEXT_THEPIT_MIDDLE_AGED_MAN
	object_event  3,  8, SPRITE_BALDING_GUY, STAY, RIGHT, TEXT_THEPIT_BALDING_GUY
	object_event 16,  6, SPRITE_GAMBLER, STAY, LEFT, TEXT_THEPIT_GAMBLER

	def_warps_to THE_PIT
