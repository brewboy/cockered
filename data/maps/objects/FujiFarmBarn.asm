	object_const_def
	const_export FUJIFARMBARN_PRIMEFOWL
	const_export FUJIFARMBARN_FLOCK_1
	const_export FUJIFARMBARN_FLOCK_2
	const_export FUJIFARMBARN_FLOCK_3
	const_export FUJIFARMBARN_FLOCK_4
	const_export FUJIFARMBARN_FLOCK_5
	const_export FUJIFARMBARN_FLOCK_6
	const_export FUJIFARMBARN_FLOCK_7

FujiFarmBarn_Object:
	db $a ; border block

	def_warp_events
	warp_event  6,  9, FUJI_FARM, 1
	warp_event  7,  9, FUJI_FARM, 1

	def_bg_events
	bg_event  3,  0, TEXT_FUJIFARMBARN_PHOTO
	bg_event  9,  0, TEXT_FUJIFARMBARN_LEDGER
	bg_event 10,  0, TEXT_FUJIFARMBARN_LEDGER

	def_object_events
	; the BLACKBELT's bird, once you've beaten him in the Pit
	object_event 10,  4, SPRITE_MONSTER, STAY, DOWN, TEXT_FUJIFARMBARN_PRIMEFOWL
	object_event  2,  3, SPRITE_BIRD, STAY, NONE, TEXT_FUJIFARMBARN_FLOCK_1
	object_event  5,  4, SPRITE_BIRD, STAY, NONE, TEXT_FUJIFARMBARN_FLOCK_2
	object_event  8,  3, SPRITE_FAIRY, STAY, NONE, TEXT_FUJIFARMBARN_FLOCK_3
	object_event  3,  7, SPRITE_MONSTER, STAY, NONE, TEXT_FUJIFARMBARN_FLOCK_4
	object_event  9,  7, SPRITE_BIRD, STAY, NONE, TEXT_FUJIFARMBARN_FLOCK_5
	object_event  1,  5, SPRITE_FAIRY, STAY, NONE, TEXT_FUJIFARMBARN_FLOCK_6
	object_event  7,  6, SPRITE_BIRD, STAY, NONE, TEXT_FUJIFARMBARN_FLOCK_7

	def_warps_to FUJI_FARM_BARN
