	object_const_def
	const_export BREEDINGLAB_RING_SCIENTIST
	const_export BREEDINGLAB_SCIENTIST

BreedingLab_Object:
	db $17 ; border block

	def_warp_events
	warp_event  2,  9, ROUTE_20, 3
	warp_event  3,  9, ROUTE_20, 3
	warp_event  8,  0, BREEDING_LAB_PENS, 1

	def_bg_events
	bg_event  3,  0, TEXT_BREEDINGLAB_CHART
	bg_event  0,  4, TEXT_BREEDINGLAB_DIARY_NOV
	bg_event  1,  4, TEXT_BREEDINGLAB_DIARY_NOV
	bg_event 10,  4, TEXT_BREEDINGLAB_DIARY_JAN
	bg_event 11,  4, TEXT_BREEDINGLAB_DIARY_JAN

	def_object_events
	; the same man; a trainer until Giovanni gives up TEAM ROOST, then just talk
	object_event  9,  2, SPRITE_SCIENTIST, STAY, LEFT, TEXT_BREEDINGLAB_RING_SCIENTIST
	object_event  9,  2, SPRITE_SCIENTIST, STAY, LEFT, TEXT_BREEDINGLAB_SCIENTIST, OPP_SCIENTIST, 14

	def_warps_to BREEDING_LAB
