	object_const_def
	const_export FUJIFARM_FARMHAND
	const_export FUJIFARM_NEWCOMER
	const_export FUJIFARM_OLD_IRON
	const_export FUJIFARM_SCRAPS
	const_export FUJIFARM_RAZOR
	const_export FUJIFARM_POND_HEN
	const_export FUJIFARM_SILKIE
	const_export FUJIFARM_OLD_HEN
	const_export FUJIFARM_FLOCK_1
	const_export FUJIFARM_FLOCK_2
	const_export FUJIFARM_FLOCK_3
	const_export FUJIFARM_FLOCK_4

FujiFarm_Object:
	db $f ; border block

	def_warp_events
	warp_event  6,  5, FUJI_FARM_BARN, 1
	warp_event  5, 13, FUJI_FARM_HOUSE, 1

	def_bg_events
	bg_event  3,  7, TEXT_FUJIFARM_SIGN

	def_object_events
	object_event  2, 10, SPRITE_SAFARI_ZONE_WORKER, STAY, UP, TEXT_FUJIFARM_FARMHAND
	; the last bird you retired, by the gate
	object_event  8, 10, SPRITE_MONSTER, STAY, NONE, TEXT_FUJIFARM_NEWCOMER
	; OLD IRON's pen, once the Pit's main event is over
	object_event 22,  7, SPRITE_LEGEND, STAY, NONE, TEXT_FUJIFARM_OLD_IRON
	; residents who are always here
	object_event 17,  5, SPRITE_MONSTER, STAY, NONE, TEXT_FUJIFARM_SCRAPS
	object_event 18,  8, SPRITE_MONSTER, STAY, NONE, TEXT_FUJIFARM_RAZOR
	object_event 16, 14, SPRITE_SEEL, STAY, NONE, TEXT_FUJIFARM_POND_HEN
	object_event 22, 13, SPRITE_FAIRY, STAY, NONE, TEXT_FUJIFARM_SILKIE
	object_event  9, 12, SPRITE_BIRD, STAY, NONE, TEXT_FUJIFARM_OLD_HEN
	; the flock: your retired breeds, more of them as you retire more
	object_event 12,  7, SPRITE_BIRD, STAY, NONE, TEXT_FUJIFARM_FLOCK_1
	object_event 16,  7, SPRITE_BIRD, STAY, NONE, TEXT_FUJIFARM_FLOCK_2
	object_event 19,  6, SPRITE_FAIRY, STAY, NONE, TEXT_FUJIFARM_FLOCK_3
	object_event 11, 13, SPRITE_BIRD, STAY, NONE, TEXT_FUJIFARM_FLOCK_4

	def_warps_to FUJI_FARM
