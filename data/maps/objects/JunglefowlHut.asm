	object_const_def
	const_export JUNGLEFOWLHUT_CASTAWAY

JunglefowlHut_Object:
	db $a ; border block

	def_warp_events
	; to the beach by name, not LAST_MAP: after a blackout you start in here
	warp_event  2,  7, JUNGLEFOWL_ISLAND, 2
	warp_event  3,  7, JUNGLEFOWL_ISLAND, 2

	def_bg_events
	bg_event  0,  1, TEXT_JUNGLEFOWLHUT_SHELF
	bg_event  1,  1, TEXT_JUNGLEFOWLHUT_SHELF

	def_object_events
	object_event  5,  3, SPRITE_GRAMPS, STAY, DOWN, TEXT_JUNGLEFOWLHUT_CASTAWAY

	def_warps_to JUNGLEFOWL_HUT
