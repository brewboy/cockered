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
	dw_const JunglefowlIslandRaftHelperScript,      SCRIPT_JUNGLEFOWLISLAND_RAFT_HELPER
	dw_const JunglefowlIslandPushOffScript,         SCRIPT_JUNGLEFOWLISLAND_PUSH_OFF

JunglefowlIslandDefaultScript:
; just washed ashore: the castaway comes down to the waterline
	CheckEvent EVENT_MET_CASTAWAY
	jr nz, JunglefowlIslandCheckJettyScript
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

JunglefowlIslandCheckJettyScript:
; with all three raft parts (he only gives the SAIL once you have the other
; two), stepping onto the old jetty brings the castaway down to help
	CheckEvent EVENT_GOT_SAIL
	ret z
	ld hl, JunglefowlIslandJettyCoords
	call ArePlayerCoordsInArray
	ret nc
	ld a, PAD_BUTTONS | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	xor a
	ldh [hJoyHeld], a
	ld a, SPRITE_FACING_UP
	ld [wSpritePlayerStateData1FacingDirection], a
	ld a, TOGGLE_JUNGLEFOWL_ISLAND_CASTAWAY
	ld [wToggleableObjectIndex], a
	predef ShowObject
	ld a, SFX_GO_OUTSIDE ; out of his hut
	call PlaySound
	ld de, JunglefowlIslandCastawayToJetty14Movement
	ld a, [wXCoord]
	cp 14
	jr z, .gotMovement
	ld de, JunglefowlIslandCastawayToJetty15Movement
.gotMovement
	ld a, JUNGLEFOWLISLAND_CASTAWAY
	ldh [hSpriteIndex], a
	call MoveSprite
	ld a, SCRIPT_JUNGLEFOWLISLAND_RAFT_HELPER
	ld [wJunglefowlIslandCurScript], a
	ret

JunglefowlIslandJettyCoords:
	dbmapcoord 14, 48
	dbmapcoord 15, 48
	db -1 ; end

; from his door to the top of the jetty, just above the player
JunglefowlIslandCastawayToJetty15Movement:
	db NPC_MOVEMENT_RIGHT
JunglefowlIslandCastawayToJetty14Movement:
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_RIGHT
	db NPC_MOVEMENT_DOWN
	db NPC_MOVEMENT_DOWN
	db NPC_MOVEMENT_DOWN
	db NPC_MOVEMENT_DOWN
	db NPC_MOVEMENT_DOWN
	db -1 ; end

JunglefowlIslandRaftHelperScript:
; he lashes the raft together and says goodbye
	ld a, [wStatusFlags5]
	bit BIT_SCRIPTED_NPC_MOVEMENT, a
	ret nz
	ld a, JUNGLEFOWLISLAND_CASTAWAY
	ldh [hSpriteIndex], a
	ld a, SPRITE_FACING_DOWN
	ldh [hSpriteFacingDirection], a
	call SetSpriteFacingDirectionAndDelay
	ld a, PAD_SELECT | PAD_START | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld a, TEXT_JUNGLEFOWLISLAND_RAFT
	ldh [hTextID], a
	call DisplayTextID
	ld a, PAD_BUTTONS | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld a, SCRIPT_JUNGLEFOWLISLAND_PUSH_OFF
	ld [wJunglefowlIslandCurScript], a
	ret

JunglefowlIslandPushOffScript:
; off to sea, and a day and a night later, Vermilion (see VermilionCity.asm)
	ld a, PAD_SELECT | PAD_START | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld a, TEXT_JUNGLEFOWLISLAND_PUSHED_OFF
	ldh [hTextID], a
	call DisplayTextID
	ld a, PAD_BUTTONS | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	call JunglefowlIslandRestoreBlackoutMap
	SetEvent EVENT_LEFT_JUNGLEFOWL_ISLAND
	SetEvent EVENT_RAFT_JUST_LANDED
	ld a, SCRIPT_JUNGLEFOWLISLAND_DEFAULT
	ld [wJunglefowlIslandCurScript], a
	ld a, VERMILION_CITY
	ldh [hWarpDestinationMap], a
	ld a, 5 ; the dock gate, where Vermilion walks you up into town
	ld [wDestinationWarpID], a
; Warps only load the arrival spot when the tileset changes, and the island
; and Vermilion are both OVERWORLD, so put the player there ourselves (as map
; connections do).
	ld hl, JunglefowlIslandVermilionArrival
	ld de, wCurrentTileBlockMapViewPointer
	ld bc, 4 ; view pointer, then y and x
	call CopyData
	ld a, 31 & 1
	ld [wYBlockCoord], a
	ld a, 18 & 1
	ld [wXBlockCoord], a
	ld hl, wStatusFlags3
	set BIT_WARP_FROM_CUR_SCRIPT, [hl]
	ret

JunglefowlIslandVermilionArrival:
	event_displacement VERMILION_CITY_WIDTH, 18, 31 ; Vermilion's dock gate

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
	dw_const JunglefowlIslandRaftText,          TEXT_JUNGLEFOWLISLAND_RAFT
	dw_const JunglefowlIslandPushedOffText,     TEXT_JUNGLEFOWLISLAND_PUSHED_OFF

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

JunglefowlIslandRaftText:
	text_asm
	ld hl, .LashItText
	call PrintText
	ld a, SFX_CUT
	call PlaySoundWaitForCurrent
	call WaitForSoundToFinish
	ld c, 20
	call DelayFrames
	ld a, SFX_PUSH_BOULDER
	call PlaySoundWaitForCurrent
	call WaitForSoundToFinish
	ld hl, .ItFloatsText
	call PrintText
; the goodbye depends on what you took from the island
	ld hl, .CaughtTheLeaderText
	CheckEvent EVENT_CAUGHT_ROOST_LEADER
	jr nz, .goodbye
	call JunglefowlIslandCaughtAJunglefowl ; clobbers hl
	ld hl, .CaughtSomeText
	jr nz, .goodbye
	ld hl, .CaughtNoneText
.goodbye
	call PrintText
	jp TextScriptEnd

.LashItText:
	text_far _JunglefowlIslandLashItText
	text_end

.ItFloatsText:
	text_far _JunglefowlIslandItFloatsText
	text_end

.CaughtTheLeaderText:
	text_far _JunglefowlIslandCaughtTheLeaderText
	text_end

.CaughtSomeText:
	text_far _JunglefowlIslandCaughtSomeText
	text_end

.CaughtNoneText:
	text_far _JunglefowlIslandCaughtNoneText
	text_end

JunglefowlIslandCaughtAJunglefowl:
; nz if DRATCHICK or DRAGONCOMB is registered as owned
	ld c, DEX_DRATINI - 1
	call .IsOwned
	ret nz
	ld c, DEX_DRAGONAIR - 1
.IsOwned:
	ld hl, wPokedexOwned
	ld b, FLAG_TEST
	predef FlagActionPredef
	ld a, c
	and a
	ret

JunglefowlIslandPushedOffText:
	text_far _JunglefowlIslandPushedOffText
	text_end
