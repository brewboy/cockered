	object_const_def
	const_export JUNGLEFOWLISLAND_CASTAWAY
	const_export JUNGLEFOWLISLAND_DRIFTWOOD
	const_export JUNGLEFOWLISLAND_WATCHER
	const_export JUNGLEFOWLISLAND_STRUTTER
	const_export JUNGLEFOWLISLAND_SCRATCHER
	const_export JUNGLEFOWLISLAND_VINE_ROPE

JunglefowlIsland_Object:
	db $43 ; border block (sea)

	def_warp_events
	; where you wash ashore; plain sand, so it never warps anywhere itself
	warp_event  9, 47, VERMILION_CITY, 1
	warp_event  3, 41, JUNGLEFOWL_HUT, 1
	warp_event  8,  1, JUNGLEFOWL_ROOST, 1

	def_bg_events

	def_object_events
	object_event  4, 42, SPRITE_GRAMPS, STAY, DOWN, TEXT_JUNGLEFOWLISLAND_CASTAWAY
	object_event  3, 47, SPRITE_POKE_BALL, STAY, NONE, TEXT_JUNGLEFOWLISLAND_DRIFTWOOD
	object_event 13, 38, SPRITE_MONSTER, STAY, DOWN, TEXT_JUNGLEFOWLISLAND_WATCHER
	; junglefowl that wander the jungle path
	object_event 11, 19, SPRITE_MONSTER, WALK, ANY_DIR, TEXT_JUNGLEFOWLISLAND_STRUTTER
	object_event  6,  9, SPRITE_MONSTER, WALK, ANY_DIR, TEXT_JUNGLEFOWLISLAND_SCRATCHER
	; at the end of the side path
	object_event 17, 14, SPRITE_POKE_BALL, STAY, NONE, TEXT_JUNGLEFOWLISLAND_VINE_ROPE

	def_warps_to JUNGLEFOWL_ISLAND
