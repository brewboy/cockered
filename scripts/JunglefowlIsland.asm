JunglefowlIsland_Script:
	call EnableAutoTextBoxDrawing
	ld hl, JunglefowlIsland_ScriptPointers
	ld a, [wJunglefowlIslandCurScript]
	jp CallFunctionInTable

JunglefowlIsland_ScriptPointers:
	def_script_pointers
	dw_const JunglefowlIslandDefaultScript,         SCRIPT_JUNGLEFOWLISLAND_DEFAULT
	dw_const JunglefowlIslandCastawayArrivesScript, SCRIPT_JUNGLEFOWLISLAND_CASTAWAY_ARRIVES
	dw_const JunglefowlIslandCastawayLeavesScript,  SCRIPT_JUNGLEFOWLISLAND_CASTAWAY_LEAVES
	dw_const JunglefowlIslandWatcherRunsScript,     SCRIPT_JUNGLEFOWLISLAND_WATCHER_RUNS
	dw_const JunglefowlIslandWatcherRanScript,      SCRIPT_JUNGLEFOWLISLAND_WATCHER_RAN

JunglefowlIslandDefaultScript:
; just washed ashore: the castaway comes down to the waterline
	CheckEvent EVENT_MET_CASTAWAY
	ret nz
	CheckEvent EVENT_WASHED_OVERBOARD
	ret z
	ld a, PAD_SELECT | PAD_START | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld a, SPRITE_FACING_UP
	ld [wSpritePlayerStateData1FacingDirection], a
	ld a, TEXT_JUNGLEFOWLISLAND_WASHED_ASHORE
	ldh [hTextID], a
	call DisplayTextID
	ld a, PAD_BUTTONS | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld de, JunglefowlIslandCastawayToPlayerMovement
	ld a, JUNGLEFOWLISLAND_CASTAWAY
	ldh [hSpriteIndex], a
	call MoveSprite
	ld a, SCRIPT_JUNGLEFOWLISLAND_CASTAWAY_ARRIVES
	ld [wJunglefowlIslandCurScript], a
	ret

JunglefowlIslandCastawayToPlayerMovement:
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_DOWN
	db NPC_MOVEMENT_DOWN
	db NPC_MOVEMENT_DOWN
	db NPC_MOVEMENT_DOWN
	db -1 ; end

JunglefowlIslandCastawayArrivesScript:
	ld a, [wStatusFlags5]
	bit BIT_SCRIPTED_NPC_MOVEMENT, a
	ret nz
	ld a, JUNGLEFOWLISLAND_CASTAWAY
	ldh [hSpriteIndex], a
	ld a, SPRITE_FACING_DOWN
	ldh [hSpriteFacingDirection], a
	call SetSpriteFacingDirectionAndDelay
	ld a, SPRITE_FACING_UP
	ld [wSpritePlayerStateData1FacingDirection], a
	ld a, PAD_SELECT | PAD_START | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld a, TEXT_JUNGLEFOWLISLAND_CASTAWAY
	ldh [hTextID], a
	call DisplayTextID
	SetEvent EVENT_MET_CASTAWAY
	ld a, PAD_BUTTONS | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld de, JunglefowlIslandCastawayToHutMovement
	ld a, JUNGLEFOWLISLAND_CASTAWAY
	ldh [hSpriteIndex], a
	call MoveSprite
	ld a, SCRIPT_JUNGLEFOWLISLAND_CASTAWAY_LEAVES
	ld [wJunglefowlIslandCurScript], a
	ret

JunglefowlIslandCastawayToHutMovement:
	db NPC_MOVEMENT_UP
	db NPC_MOVEMENT_UP
	db NPC_MOVEMENT_UP
	db NPC_MOVEMENT_UP
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_UP
	db -1 ; end

JunglefowlIslandCastawayLeavesScript:
; he goes in at his door
	ld a, [wStatusFlags5]
	bit BIT_SCRIPTED_NPC_MOVEMENT, a
	ret nz
	ld a, TOGGLE_JUNGLEFOWL_ISLAND_CASTAWAY
	ld [wToggleableObjectIndex], a
	predef HideObject
	ld a, SFX_GO_INSIDE
	call PlaySound
	xor a
	ld [wJoyIgnore], a
	ld a, SCRIPT_JUNGLEFOWLISLAND_DEFAULT
	ld [wJunglefowlIslandCurScript], a
	ret

JunglefowlIslandWatcherRunsScript:
; once its text has closed, the junglefowl runs off up the path
	ld a, PAD_BUTTONS | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld de, JunglefowlIslandWatcherRunMovement
	ld a, JUNGLEFOWLISLAND_WATCHER
	ldh [hSpriteIndex], a
	call MoveSprite
	ld a, SCRIPT_JUNGLEFOWLISLAND_WATCHER_RAN
	ld [wJunglefowlIslandCurScript], a
	ret

JunglefowlIslandWatcherRanScript:
	ld a, [wStatusFlags5]
	bit BIT_SCRIPTED_NPC_MOVEMENT, a
	ret nz
	ld a, TOGGLE_JUNGLEFOWL_ISLAND_WATCHER
	ld [wToggleableObjectIndex], a
	predef HideObject
	xor a
	ld [wJoyIgnore], a
	ld a, SCRIPT_JUNGLEFOWLISLAND_DEFAULT
	ld [wJunglefowlIslandCurScript], a
	ret

JunglefowlIsland_TextPointers:
	def_text_pointers
	dw_const JunglefowlIslandCastawayText,      TEXT_JUNGLEFOWLISLAND_CASTAWAY
	dw_const JunglefowlIslandDriftwoodText,     TEXT_JUNGLEFOWLISLAND_DRIFTWOOD
	dw_const JunglefowlIslandWatcherText,       TEXT_JUNGLEFOWLISLAND_WATCHER
	dw_const JunglefowlIslandStrutterText,      TEXT_JUNGLEFOWLISLAND_STRUTTER
	dw_const JunglefowlIslandScratcherText,     TEXT_JUNGLEFOWLISLAND_SCRATCHER
	dw_const JunglefowlIslandVineRopeText,      TEXT_JUNGLEFOWLISLAND_VINE_ROPE
	dw_const JunglefowlIslandWashedAshoreText,  TEXT_JUNGLEFOWLISLAND_WASHED_ASHORE

JunglefowlIslandCastawayText:
	text_far _JunglefowlIslandCastawayText
	text_end

JunglefowlIslandWashedAshoreText:
	text_far _JunglefowlIslandWashedAshoreText
	text_end

JunglefowlIslandDriftwoodText:
	text_asm
	SetEvent EVENT_GOT_DRIFTWOOD
	ld a, TOGGLE_JUNGLEFOWL_ISLAND_DRIFTWOOD
	ld [wToggleableObjectIndex], a
	predef HideObject
	ld hl, .FoundDriftwoodText
	call PrintText
	jp TextScriptEnd

.FoundDriftwoodText:
	text_far _JunglefowlIslandFoundDriftwoodText
	sound_get_item_1
	text_far _JunglefowlIslandDriftwoodFloatsText
	text_end

JunglefowlIslandWatcherText:
; the junglefowl looks at you, crows, and runs off into the trees
	text_asm
	ld hl, .WatchingText
	call PrintText
	ld a, DRATINI
	call PlayCry
	call WaitForSoundToFinish
	ld hl, .RanOffText
	call PrintText
	SetEvent EVENT_JUNGLEFOWL_RAN_OFF
	ld a, SCRIPT_JUNGLEFOWLISLAND_WATCHER_RUNS
	ld [wJunglefowlIslandCurScript], a
	jp TextScriptEnd

.WatchingText:
	text_far _JunglefowlIslandWatcherText
	text_end

.RanOffText:
	text_far _JunglefowlIslandWatcherRanText
	text_end

JunglefowlIslandWatcherRunMovement:
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_LEFT
	db NPC_MOVEMENT_UP
	db NPC_MOVEMENT_UP
	db NPC_MOVEMENT_UP
	db -1 ; end

JunglefowlIslandStrutterText:
	text_asm
	ld hl, .StruttingText
	ld de, .NobodysText
	jr JunglefowlIslandWandererCry

.StruttingText:
	text_far _JunglefowlIslandStrutterText
	text_end

.NobodysText:
	text_far _JunglefowlIslandNobodysBirdText
	text_end

JunglefowlIslandScratcherText:
	text_asm
	ld hl, .ScratchingText
	ld de, .DoesntCareText
	; fallthrough

JunglefowlIslandWandererCry:
; a wild junglefowl on the path: you see it (hl), it crows, and it goes
; about its business (de)
	push de
	call PrintText
	ld a, DRATINI
	call PlayCry
	call WaitForSoundToFinish
	pop hl
	call PrintText
	jp TextScriptEnd

JunglefowlIslandScratcherText.ScratchingText:
	text_far _JunglefowlIslandScratcherText
	text_end

JunglefowlIslandScratcherText.DoesntCareText:
	text_far _JunglefowlIslandDoesntCareText
	text_end

JunglefowlIslandVineRopeText:
	text_asm
	SetEvent EVENT_GOT_VINE_ROPE
	ld a, TOGGLE_JUNGLEFOWL_ISLAND_VINE_ROPE
	ld [wToggleableObjectIndex], a
	predef HideObject
	ld hl, .FoundVineRopeText
	call PrintText
	jp TextScriptEnd

.FoundVineRopeText:
	text_far _JunglefowlIslandFoundVineRopeText
	sound_get_item_1
	text_far _JunglefowlIslandVineRopeToughText
	text_end

JunglefowlIslandRestoreBlackoutMap:
; for the raft home: blackouts go back to wherever they went before the island
	ld a, [wBlackoutMapBeforeIsland]
	ld [wLastBlackoutMap], a
	ret
