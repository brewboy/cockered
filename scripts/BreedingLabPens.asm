BreedingLabPens_Script:
	call EnableAutoTextBoxDrawing
	ld hl, BreedingLabPensTrainerHeaders
	ld de, BreedingLabPens_ScriptPointers
	ld a, [wBreedingLabPensCurScript]
	call ExecuteCurMapScriptInTable
	ld [wBreedingLabPensCurScript], a
	ret

BreedingLabPens_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_BREEDINGLABPENS_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_BREEDINGLABPENS_START_BATTLE
	dw_const EndTrainerBattle,                      SCRIPT_BREEDINGLABPENS_END_BATTLE

BreedingLabPens_TextPointers:
	def_text_pointers
	dw_const BreedingLabPensBroilerText,  TEXT_BREEDINGLABPENS_BROILER
	dw_const BreedingLabPensCrowerText,   TEXT_BREEDINGLABPENS_CROWER
	dw_const BreedingLabPensMewpeepText,  TEXT_BREEDINGLABPENS_MEWPEEP
	dw_const BreedingLabPensLayerText,    TEXT_BREEDINGLABPENS_LAYER
	dw_const BreedingLabPensShowBirdText, TEXT_BREEDINGLABPENS_SHOW_BIRD
	dw_const BreedingLabPensDiaryOctText, TEXT_BREEDINGLABPENS_DIARY_OCT

BreedingLabPensTrainerHeaders:
	def_trainers 3 ; MEWPEEP is the third object
MewpeepTrainerHeader:
; like the legendary birds: one battle, then it's gone, caught or not
	trainer EVENT_BEAT_MEWPEEP, 0, BreedingLabPensMewpeepBattleText, BreedingLabPensMewpeepBattleText, BreedingLabPensMewpeepBattleText
	db -1 ; end

BreedingLabPensMewpeepText:
	text_asm
	ld hl, MewpeepTrainerHeader
	call TalkToTrainer
	ld a, [wCurMapScript]
	ld [wBreedingLabPensCurScript], a
	jp TextScriptEnd

BreedingLabPensMewpeepBattleText:
	text_far _BreedingLabPensMewpeepBattleText
	text_asm
	ld a, MEW
	call PlayCry
	call WaitForSoundToFinish
	jp TextScriptEnd

BreedingLabPensBroilerText:
	text_far _BreedingLabPensBroilerText
	text_end

BreedingLabPensCrowerText:
	text_far _BreedingLabPensCrowerText
	text_end

BreedingLabPensLayerText:
	text_far _BreedingLabPensLayerText
	text_end

BreedingLabPensShowBirdText:
	text_far _BreedingLabPensShowBirdText
	text_end

BreedingLabPensDiaryOctText:
	text_far _BreedingLabPensDiaryOctText
	text_end
