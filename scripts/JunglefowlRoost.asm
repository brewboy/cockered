JunglefowlRoost_Script:
	call EnableAutoTextBoxDrawing
	ld hl, JunglefowlRoostTrainerHeaders
	ld de, JunglefowlRoost_ScriptPointers
	ld a, [wJunglefowlRoostCurScript]
	call ExecuteCurMapScriptInTable
	ld [wJunglefowlRoostCurScript], a
	ret

JunglefowlRoost_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_JUNGLEFOWLROOST_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_JUNGLEFOWLROOST_START_BATTLE
	dw_const JunglefowlRoostEndBattleScript,        SCRIPT_JUNGLEFOWLROOST_END_BATTLE

JunglefowlRoostEndBattleScript:
; win, run or catch, the leader is gone afterwards (EndTrainerBattle hides it).
; Remember a catch: the castaway's goodbye depends on it. Running away and
; catching give the same wBattleResult, so look for one more COCK instead.
	ld a, [wIsInBattle]
	cp LOST_BATTLE
	jp z, EndTrainerBattle
	call JunglefowlRoostCountMons
	ld hl, wMonCountBeforeRoostLeader
	cp [hl]
	jp z, EndTrainerBattle
	SetEvent EVENT_CAUGHT_ROOST_LEADER
	jp EndTrainerBattle

JunglefowlRoostCountMons:
; a = party size + current box size
	ld a, [wBoxCount]
	ld b, a
	ld a, [wPartyCount]
	add b
	ret

JunglefowlRoost_TextPointers:
	def_text_pointers
	dw_const JunglefowlRoostLeaderText,   TEXT_JUNGLEFOWLROOST_LEADER
	dw_const JunglefowlRoostSleeperText,  TEXT_JUNGLEFOWLROOST_SLEEPER1
	dw_const JunglefowlRoostSleeperText,  TEXT_JUNGLEFOWLROOST_SLEEPER2
	dw_const JunglefowlRoostHenText,      TEXT_JUNGLEFOWLROOST_HEN
	dw_const JunglefowlRoostSleeperText,  TEXT_JUNGLEFOWLROOST_SLEEPER3

JunglefowlRoostTrainerHeaders:
	def_trainers 5 ; EVENT_BEAT_ROOST_LEADER's bit
LeaderTrainerHeader:
	trainer EVENT_BEAT_ROOST_LEADER, 0, JunglefowlRoostLeaderWakesText, JunglefowlRoostLeaderWakesText, JunglefowlRoostLeaderWakesText
	db -1 ; end

JunglefowlRoostLeaderText:
	text_asm
	call JunglefowlRoostCountMons
	ld [wMonCountBeforeRoostLeader], a
	ld hl, LeaderTrainerHeader
	call TalkToTrainer
	ld a, [wCurMapScript]
	ld [wJunglefowlRoostCurScript], a
	jp TextScriptEnd

JunglefowlRoostLeaderWakesText:
	text_far _JunglefowlRoostLeaderWakesText
	text_asm
	ld a, DRAGONAIR
	call PlayCry
	call WaitForSoundToFinish
	jp TextScriptEnd

JunglefowlRoostSleeperText:
	text_far _JunglefowlRoostSleeperText
	text_end

JunglefowlRoostHenText:
	text_far _JunglefowlRoostHenText
	text_end
