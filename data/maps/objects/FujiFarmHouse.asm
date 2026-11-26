	object_const_def
	const_export FUJIFARMHOUSE_FARMER

FujiFarmHouse_Object:
	db $a ; border block

	def_warp_events
	warp_event  2,  7, FUJI_FARM, 2
	warp_event  3,  7, FUJI_FARM, 2

	def_bg_events
	bg_event  7,  0, TEXT_FUJIFARMHOUSE_NEST

	def_object_events
	object_event  3,  4, SPRITE_GRANNY, STAY, DOWN, TEXT_FUJIFARMHOUSE_FARMER

	def_warps_to FUJI_FARM_HOUSE
