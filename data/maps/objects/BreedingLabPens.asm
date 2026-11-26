	object_const_def
	const_export BREEDINGLABPENS_BROILER
	const_export BREEDINGLABPENS_CROWER
	const_export BREEDINGLABPENS_MEWPEEP
	const_export BREEDINGLABPENS_LAYER
	const_export BREEDINGLABPENS_SHOW_BIRD

BreedingLabPens_Object:
	db $17 ; border block

	def_warp_events
	warp_event  6,  9, BREEDING_LAB, 3
	warp_event  7,  9, BREEDING_LAB, 3

	def_bg_events
	bg_event  3,  1, TEXT_BREEDINGLABPENS_DIARY_OCT

	def_object_events
	; the failed experiments, in their stalls and loose
	object_event  2,  4, SPRITE_MONSTER, STAY, DOWN, TEXT_BREEDINGLABPENS_BROILER
	object_event  6,  4, SPRITE_BIRD, STAY, DOWN, TEXT_BREEDINGLABPENS_CROWER
	; the original bird, in its case (third, to match its trainer flag)
	object_event 10,  2, SPRITE_BIRD, STAY, DOWN, TEXT_BREEDINGLABPENS_MEWPEEP, MEW, 50
	object_event 10,  4, SPRITE_SEEL, STAY, DOWN, TEXT_BREEDINGLABPENS_LAYER
	object_event  3,  7, SPRITE_FAIRY, STAY, NONE, TEXT_BREEDINGLABPENS_SHOW_BIRD

	def_warps_to BREEDING_LAB_PENS
