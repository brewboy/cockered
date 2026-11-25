	object_const_def
	const_export JUNGLEFOWLISLAND_CASTAWAY
	const_export JUNGLEFOWLISLAND_DRIFTWOOD
	const_export JUNGLEFOWLISLAND_WATCHER

JunglefowlIsland_Object:
	db $43 ; border block (sea)

	def_warp_events
	; where you wash ashore; plain sand, so it never warps anywhere itself
	warp_event  9, 47, VERMILION_CITY, 1

	def_bg_events

	def_object_events
	object_event  4, 42, SPRITE_GRAMPS, STAY, DOWN, TEXT_JUNGLEFOWLISLAND_CASTAWAY
	object_event  3, 47, SPRITE_POKE_BALL, STAY, NONE, TEXT_JUNGLEFOWLISLAND_DRIFTWOOD
	object_event 13, 38, SPRITE_MONSTER, STAY, DOWN, TEXT_JUNGLEFOWLISLAND_WATCHER

	def_warps_to JUNGLEFOWL_ISLAND
