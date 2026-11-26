	object_const_def
	const_export JUNGLEFOWLROOST_LEADER
	const_export JUNGLEFOWLROOST_SLEEPER1
	const_export JUNGLEFOWLROOST_SLEEPER2
	const_export JUNGLEFOWLROOST_HEN
	const_export JUNGLEFOWLROOST_SLEEPER3

JunglefowlRoost_Object:
	db $2 ; border block (trees)

	def_warp_events
	; back down to the top of the jungle path
	warp_event  9, 19, JUNGLEFOWL_ISLAND, 3
	warp_event  8, 19, JUNGLEFOWL_ISLAND, 3
	warp_event 10, 19, JUNGLEFOWL_ISLAND, 3
	warp_event 11, 19, JUNGLEFOWL_ISLAND, 3

	def_bg_events

	def_object_events
	; the flock's leader, asleep at the top of the roost
	object_event  9,  3, SPRITE_LEGEND, STAY, DOWN, TEXT_JUNGLEFOWLROOST_LEADER, DRAGONAIR, 30
	object_event  5,  7, SPRITE_MONSTER, STAY, RIGHT, TEXT_JUNGLEFOWLROOST_SLEEPER1
	object_event 14,  7, SPRITE_MONSTER, STAY, LEFT, TEXT_JUNGLEFOWLROOST_SLEEPER2
	object_event  5, 13, SPRITE_MONSTER, STAY, RIGHT, TEXT_JUNGLEFOWLROOST_HEN
	object_event 14, 13, SPRITE_MONSTER, STAY, LEFT, TEXT_JUNGLEFOWLROOST_SLEEPER3

	def_warps_to JUNGLEFOWL_ROOST
