; The Breeding Lab, on an islet at the west end of Route 20: where MEWPEEP's
; line was bred into fighters for whoever paid. Its diaries, like the
; Pokemon Mansion's, are signed "F."

BreedingLab_Script:
	call BreedingLabSyncScientist
	call EnableAutoTextBoxDrawing
	ld hl, BreedingLabTrainerHeaders
	ld de, BreedingLab_ScriptPointers
	ld a, [wBreedingLabCurScript]
	call ExecuteCurMapScriptInTable
	ld [wBreedingLabCurScript], a
	ret

BreedingLabSyncScientist:
; He fights for TEAM ROOST's money; once Giovanni gives it up, he just talks.
	ld hl, wCurrentMapScriptFlags
	bit BIT_CUR_MAP_LOADED_1, [hl]
	res BIT_CUR_MAP_LOADED_1, [hl]
	ret z
	ld a, [wEventFlags + EVENT_BEAT_VIRIDIAN_GYM_GIOVANNI / 8]
	and 1 << (EVENT_BEAT_VIRIDIAN_GYM_GIOVANNI % 8)
	push af
	ld c, TOGGLE_BREEDING_LAB_RING_SCIENTIST
	call FarmShowIf
	pop af
	xor 1 << (EVENT_BEAT_VIRIDIAN_GYM_GIOVANNI % 8)
	ld c, TOGGLE_BREEDING_LAB_SCIENTIST
	jp FarmShowIf

BreedingLab_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_BREEDINGLAB_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_BREEDINGLAB_START_BATTLE
	dw_const EndTrainerBattle,                      SCRIPT_BREEDINGLAB_END_BATTLE

BreedingLab_TextPointers:
	def_text_pointers
	dw_const BreedingLabRingScientistText, TEXT_BREEDINGLAB_RING_SCIENTIST
	dw_const BreedingLabScientistText,     TEXT_BREEDINGLAB_SCIENTIST
	dw_const BreedingLabChartText,         TEXT_BREEDINGLAB_CHART
	dw_const BreedingLabDiaryNovText,      TEXT_BREEDINGLAB_DIARY_NOV
	dw_const BreedingLabDiaryJanText,      TEXT_BREEDINGLAB_DIARY_JAN

BreedingLabTrainerHeaders:
	def_trainers 2 ; he is the second object
BreedingLabTrainerHeader0:
	trainer EVENT_BEAT_BREEDING_LAB_SCIENTIST, 4, BreedingLabScientistBattleText, BreedingLabScientistEndBattleText, BreedingLabScientistAfterBattleText
	db -1 ; end

BreedingLabScientistText:
	text_asm
	ld hl, BreedingLabTrainerHeader0
	call TalkToTrainer
	jp TextScriptEnd

BreedingLabScientistBattleText:
	text_far _BreedingLabScientistBattleText
	text_end

BreedingLabScientistEndBattleText:
	text_far _BreedingLabScientistEndBattleText
	text_end

BreedingLabScientistAfterBattleText:
	text_far _BreedingLabScientistAfterBattleText
	text_end

BreedingLabRingScientistText:
	text_far _BreedingLabRingScientistText
	text_end

BreedingLabChartText:
	text_asm
	ld hl, .RoostText
	CheckEvent EVENT_BEAT_VIRIDIAN_GYM_GIOVANNI
	jr z, .print
	ld hl, .RingText
.print
	call PrintText
	jp TextScriptEnd

.RoostText:
	text_far _BreedingLabChartRoostText
	text_end

.RingText:
	text_far _BreedingLabChartRingText
	text_end

BreedingLabDiaryNovText:
	text_far _BreedingLabDiaryNovText
	text_end

BreedingLabDiaryJanText:
	text_far _BreedingLabDiaryJanText
	text_end
