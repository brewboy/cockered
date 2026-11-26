; MR.FUJI's farm, east of Lavender, where birds go when nobody wants them.
; You can retire birds from your party here for good (FujiFarmHouse). The
; farm remembers which breeds you've retired, and the flock grows with them.

DEF FARM_GIFT_EVERY EQU 5 ; a gift for every 5 different breeds retired
DEF NUM_FARM_GIFTS EQU 10 ; FarmGifts, in FujiFarmHouse.asm
DEF NUM_FARM_FLOCK_SLOTS EQU 11 ; FarmFlockSlots

FujiFarm_Script:
	call EnableAutoTextBoxDrawing
	call FujiFarmCheckSync
	ld hl, FujiFarm_ScriptPointers
	ld a, [wFujiFarmCurScript]
	jp CallFunctionInTable

FujiFarmCheckSync:
; Sort out who's about when you arrive: by a warp (the map-loaded flag) or
; on foot from Lavender (wFarmNeedsSync, set by the maps next door).
	ld hl, wCurrentMapScriptFlags
	bit BIT_CUR_MAP_LOADED_1, [hl]
	res BIT_CUR_MAP_LOADED_1, [hl]
	jr nz, .sync
	ld a, [wFarmNeedsSync]
	and a
	ret z
.sync
	xor a
	ld [wFarmNeedsSync], a
	call FarmTurnRotation
	jp FarmSyncResidents

FujiFarm_ScriptPointers:
	def_script_pointers
	dw_const FujiFarmDefaultScript,    SCRIPT_FUJIFARM_DEFAULT
	dw_const FujiFarmTurnedBackScript, SCRIPT_FUJIFARM_TURNED_BACK

FujiFarmDefaultScript:
; while MR.FUJI is missing, the farmhand turns you back at the gate
	CheckEvent EVENT_RESCUED_MR_FUJI
	ret nz
	ld a, [wXCoord]
	cp 1
	ret nz
	ld a, PAD_SELECT | PAD_START | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	xor a
	ldh [hJoyHeld], a
	ld a, TEXT_FUJIFARM_FARMHAND
	ldh [hTextID], a
	call DisplayTextID
	xor a
	ld [wJoyIgnore], a
	ld a, 1
	ld [wSimulatedJoypadStatesIndex], a
	ld a, PAD_LEFT
	ld [wSimulatedJoypadStatesEnd], a
	call StartSimulatingJoypadStates
	ld a, SCRIPT_FUJIFARM_TURNED_BACK
	ld [wFujiFarmCurScript], a
	ret

FujiFarmTurnedBackScript:
	ld a, [wSimulatedJoypadStatesIndex]
	and a
	ret nz
	xor a ; SCRIPT_FUJIFARM_DEFAULT
	ld [wJoyIgnore], a
	ld [wFujiFarmCurScript], a
	ret

; ---- shared by the farm, the barn and the farmhouse

FarmCountRetiredBreeds:
; a = [wNumSetBits] = how many different breeds you've retired
	ld hl, wFarmRetiredFlags
	ld b, wFarmRetiredFlagsEnd - wFarmRetiredFlags
	call CountSetBits
	ld a, [wNumSetBits]
	ret

FarmGetRetiredBreed:
; in: a = n; out: a = species of the nth retired breed (in Pokédex order),
; its name in wNameBuffer
	ld e, a
	ld hl, wFarmRetiredFlags
	ld d, 1 ; bit mask
	ld c, 0 ; Pokédex number - 1
.loop
	ld a, [hl]
	and d
	jr z, .next
	ld a, e
	and a
	jr z, .found
	dec e
.next
	inc c
	ld a, c
	cp NUM_POKEMON
	jr nc, .found ; not reached: n is always less than the count
	rlc d
	jr nc, .loop
	inc hl
	jr .loop
.found
	ld a, c
	inc a
	ld [wPokedexNum], a
	callfar PokedexToIndex
	ld a, [wPokedexNum]
	ld [wNamedObjectIndex], a
	push af
	call GetMonName
	pop af
	ret

FarmRecordBreed:
; in: a = species; marks it retired. nz if it's a new breed for the ledger
	ld [wPokedexNum], a
	predef IndexToPokedex
	ld a, [wPokedexNum]
	dec a
	ld c, a
	push bc
	ld hl, wFarmRetiredFlags
	ld b, FLAG_TEST
	predef FlagActionPredef
	ld a, c
	pop bc
	and a
	jr nz, .known
	ld hl, wFarmRetiredFlags
	ld b, FLAG_SET
	predef FlagActionPredef
	or 1
	ret
.known
	xor a
	ret

FarmTurnRotation:
; each visit, the flock shows a different set of your retired breeds
	call FarmCountRetiredBreeds
	and a
	ret z
	ld b, a
	ld a, [wFarmRotation]
	inc a
	cp b
	jr c, .ok
	xor a
.ok
	ld [wFarmRotation], a
	ret

FarmSyncResidents:
; Show or hide everyone who comes and goes, for the farm and the barn.
	call FarmCountRetiredBreeds
	ld e, a
	ld hl, FarmFlockSlots
	ld d, NUM_FARM_FLOCK_SLOTS
.flockLoop
	ld c, [hl] ; toggle
	inc hl
	ld a, e
	cp [hl] ; threshold
	inc hl
	inc hl ; skip rank
	inc hl ; and verb
	inc hl
	ld a, 0
	jr c, .gotFlock
	inc a
.gotFlock
	push hl
	push de
	call FarmShowIf
	pop de
	pop hl
	dec d
	jr nz, .flockLoop
	ld c, TOGGLE_FUJI_FARM_NEWCOMER
	ld a, [wFarmNewcomerSpecies]
	call FarmShowIf
	ld c, TOGGLE_FUJI_FARM_OLD_IRON
	ld a, [wEventFlags + EVENT_PIT_MAIN_EVENT_DONE / 8]
	and 1 << (EVENT_PIT_MAIN_EVENT_DONE % 8)
	call FarmShowIf
	ld c, TOGGLE_FUJI_FARM_BARN_PRIMEFOWL
	ld a, [wEventFlags + EVENT_PIT_BEAT_FIGHTER_3 / 8]
	and 1 << (EVENT_PIT_BEAT_FIGHTER_3 % 8)
	; fallthrough

FarmShowIf:
; show toggleable object c if a is nonzero, hide it if not
	and a
	ld b, FLAG_RESET ; shown
	jr nz, .act
	ld b, FLAG_SET ; hidden
.act
	ld hl, wToggleableObjectFlags
	predef FlagActionPredef
	ret

MACRO farm_flock_slot
; toggle, number of breeds retired before it appears, rank, verb text
; The ranks follow the thresholds in order, so however many slots are out,
; they show different breeds.
	db \1, \2, \3
	dw \4
ENDM

FarmFlockSlots:
	farm_flock_slot TOGGLE_FUJI_FARM_FLOCK_1,       1,  0, FarmVerbDustBathText
	farm_flock_slot TOGGLE_FUJI_FARM_FLOCK_2,       3,  2, FarmVerbGritText
	farm_flock_slot TOGGLE_FUJI_FARM_FLOCK_3,       6,  4, FarmVerbDozingText
	farm_flock_slot TOGGLE_FUJI_FARM_FLOCK_4,      10,  6, FarmVerbBugsText
	farm_flock_slot TOGGLE_FUJI_FARM_BARN_FLOCK_1,  2,  1, FarmVerbIgnoresYouText
	farm_flock_slot TOGGLE_FUJI_FARM_BARN_FLOCK_2,  4,  3, FarmVerbPreeningText
	farm_flock_slot TOGGLE_FUJI_FARM_BARN_FLOCK_3,  8,  5, FarmVerbCornText
	farm_flock_slot TOGGLE_FUJI_FARM_BARN_FLOCK_4, 13,  7, FarmVerbStrawText
	farm_flock_slot TOGGLE_FUJI_FARM_BARN_FLOCK_5, 18,  8, FarmVerbOneLegText
	farm_flock_slot TOGGLE_FUJI_FARM_BARN_FLOCK_6, 24,  9, FarmVerbNeverAgainText
	farm_flock_slot TOGGLE_FUJI_FARM_BARN_FLOCK_7, 30, 10, FarmVerbBestSpotText
	assert NUM_FARM_FLOCK_SLOTS == (@ - FarmFlockSlots) / 5

FarmFlockTalk:
; a = flock slot (0-10). Names one of your retired breeds and says what it's up to.
	ld hl, FarmFlockSlots + 2
	ld bc, 5
	call AddNTimes
	ld a, [hli] ; rank
	ld e, [hl]
	inc hl
	ld d, [hl]
	push de ; verb text
	ld b, a
	ld a, [wFarmRotation]
	add b
	push af
	call FarmCountRetiredBreeds
	ld b, a
	pop af
.mod
	cp b
	jr c, .gotIndex
	sub b
	jr .mod
.gotIndex
	call FarmGetRetiredBreed
	call PlayCry
	pop hl
	call PrintText
	jp TextScriptEnd

MACRO farm_verb
; the bird's name, then what it's up to
FarmVerb\1Text:
	text_far _FujiFarmFlockNameText
	text_far _FujiFarmFlock\1Text
	text_end
ENDM
	farm_verb DustBath
	farm_verb Grit
	farm_verb Dozing
	farm_verb Bugs
	farm_verb IgnoresYou
	farm_verb Preening
	farm_verb Corn
	farm_verb Straw
	farm_verb OneLeg
	farm_verb NeverAgain
	farm_verb BestSpot

FujiFarm_TextPointers:
	def_text_pointers
	dw_const FujiFarmFarmhandText,  TEXT_FUJIFARM_FARMHAND
	dw_const FujiFarmNewcomerText,  TEXT_FUJIFARM_NEWCOMER
	dw_const FujiFarmOldIronText,   TEXT_FUJIFARM_OLD_IRON
	dw_const FujiFarmScrapsText,    TEXT_FUJIFARM_SCRAPS
	dw_const FujiFarmRazorText,     TEXT_FUJIFARM_RAZOR
	dw_const FujiFarmPondHenText,   TEXT_FUJIFARM_POND_HEN
	dw_const FujiFarmSilkieText,    TEXT_FUJIFARM_SILKIE
	dw_const FujiFarmOldHenText,    TEXT_FUJIFARM_OLD_HEN
	dw_const FujiFarmFlock1Text,    TEXT_FUJIFARM_FLOCK_1
	dw_const FujiFarmFlock2Text,    TEXT_FUJIFARM_FLOCK_2
	dw_const FujiFarmFlock3Text,    TEXT_FUJIFARM_FLOCK_3
	dw_const FujiFarmFlock4Text,    TEXT_FUJIFARM_FLOCK_4
	dw_const FujiFarmSignText,      TEXT_FUJIFARM_SIGN

FujiFarmFarmhandText:
	text_asm
	ld hl, .ShutText
	CheckEvent EVENT_RESCUED_MR_FUJI
	jr z, .print
	ld hl, .OpenText
	call PrintText
	; a pen waits for OLD IRON, if you've heard of the Pit
	CheckEvent EVENT_PIT_INVITED
	jr z, .done
	CheckEvent EVENT_PIT_MAIN_EVENT_DONE
	jr nz, .done
	ld hl, .EmptyPenText
.print
	call PrintText
.done
	jp TextScriptEnd

.ShutText:
	text_far _FujiFarmFarmhandShutText
	text_end

.OpenText:
	text_far _FujiFarmFarmhandOpenText
	text_end

.EmptyPenText:
	text_far _FujiFarmFarmhandEmptyPenText
	text_end

FujiFarmNewcomerText:
	text_asm
	ld a, [wFarmNewcomerSpecies]
	call PlayCry
	ld hl, .Text
	call PrintText
	jp TextScriptEnd

.Text:
	text_far _FujiFarmNewcomerText
	text_end

FujiFarmOldIronText:
	text_asm
	ld a, ONIX ; SHAMONIX
	call PlayCry
	ld hl, .UnbeatenText ; you threw the fight, or lost it
	CheckEvent EVENT_PIT_BEAT_OLD_IRON
	jr z, .print
	ld hl, .BeatenText
.print
	call PrintText
	jp TextScriptEnd

.UnbeatenText:
	text_far _FujiFarmOldIronUnbeatenText
	text_end

.BeatenText:
	text_far _FujiFarmOldIronBeatenText
	text_end

FujiFarmScrapsText:
	text_far _FujiFarmScrapsText
	text_end

FujiFarmRazorText:
	text_far _FujiFarmRazorText
	text_end

FujiFarmPondHenText:
	text_far _FujiFarmPondHenText
	text_end

FujiFarmSilkieText:
	text_far _FujiFarmSilkieText
	text_end

FujiFarmOldHenText:
	text_far _FujiFarmOldHenText
	text_end

FujiFarmSignText:
	text_far _FujiFarmSignText
	text_end

FujiFarmFlock1Text:
	text_asm
	xor a
	jp FarmFlockTalk

FujiFarmFlock2Text:
	text_asm
	ld a, 1
	jp FarmFlockTalk

FujiFarmFlock3Text:
	text_asm
	ld a, 2
	jp FarmFlockTalk

FujiFarmFlock4Text:
	text_asm
	ld a, 3
	jp FarmFlockTalk
