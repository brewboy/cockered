DEF PIT_MAIN_EVENT EQU 3 ; wPitCurFighter for OLD IRON

ThePit_Script:
	call EnableAutoTextBoxDrawing
	ld hl, ThePit_ScriptPointers
	ld a, [wThePitCurScript]
	jp CallFunctionInTable

ThePit_ScriptPointers:
	def_script_pointers
	dw_const ThePitDefaultScript,    SCRIPT_THEPIT_DEFAULT
	dw_const ThePitAfterFightScript, SCRIPT_THEPIT_AFTER_FIGHT

ThePitDefaultScript:
	ret

ThePitAfterFightScript:
; Losing here doesn't black you out (see HandlePlayerBlackOut), so whether
; anyone in your party is still standing says who won.
	ld a, [wCurOpponent]
	and a
	ret nz
	xor a ; SCRIPT_THEPIT_DEFAULT
	ld [wThePitCurScript], a
	ld a, PAD_SELECT | PAD_START | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	callfar AnyPartyAlive
	ld a, d
	and a
	jr z, .lost
	ld a, [wPitCurFighter]
	cp PIT_MAIN_EVENT
	jr z, .beatOldIron
	; the undercard: the purse, and after the third fight the boss sends for you
	ld c, a
	call ThePitSetFighterBeaten
	ld a, TEXT_THEPIT_WON
	jr .show
.beatOldIron
	SetEvent EVENT_PIT_MAIN_EVENT_DONE
	SetEvent EVENT_PIT_BEAT_OLD_IRON
	ld a, TEXT_THEPIT_BEAT_OLD_IRON
	jr .show
.lost
	predef HealParty
	ld a, [wPitCurFighter]
	cp PIT_MAIN_EVENT
	ld a, TEXT_THEPIT_LOST
	jr nz, .show
	SetEvent EVENT_PIT_MAIN_EVENT_DONE
	ld a, TEXT_THEPIT_LOST_TO_OLD_IRON
.show
	ldh [hTextID], a
	call DisplayTextID
	xor a
	ld [wJoyIgnore], a
	ret

ThePitSetFighterBeaten:
; set EVENT_PIT_BEAT_FIGHTER_1 + c
	ld a, c
	and a
	jr nz, .not1
	SetEvent EVENT_PIT_BEAT_FIGHTER_1
	ret
.not1
	dec a
	jr nz, .not2
	SetEvent EVENT_PIT_BEAT_FIGHTER_2
	ret
.not2
	SetEvent EVENT_PIT_BEAT_FIGHTER_3
	ret

ThePit_TextPointers:
	def_text_pointers
	dw_const ThePitBikerText,               TEXT_THEPIT_BIKER
	dw_const ThePitRockerText,              TEXT_THEPIT_ROCKER
	dw_const ThePitBlackbeltText,           TEXT_THEPIT_BLACKBELT
	dw_const ThePitBookieText,              TEXT_THEPIT_BOOKIE
	dw_const ThePitBirdText,                TEXT_THEPIT_BIRD1
	dw_const ThePitBirdText,                TEXT_THEPIT_BIRD2
	dw_const ThePitBeautyText,              TEXT_THEPIT_BEAUTY
	dw_const ThePitMiddleAgedManText,       TEXT_THEPIT_MIDDLE_AGED_MAN
	dw_const ThePitBaldingGuyText,          TEXT_THEPIT_BALDING_GUY
	dw_const ThePitGamblerText,             TEXT_THEPIT_GAMBLER
	dw_const ThePitWonText,                 TEXT_THEPIT_WON
	dw_const ThePitLostText,                TEXT_THEPIT_LOST
	dw_const ThePitBeatOldIronText,         TEXT_THEPIT_BEAT_OLD_IRON
	dw_const ThePitLostToOldIronText,       TEXT_THEPIT_LOST_TO_OLD_IRON

; The undercard. Each fighter takes the ¥2000 entry and fights when it's his
; turn; the purse is paid after the fight (ThePitWonText).
; fighter number, his beaten flag, the one before's, class, team, texts
MACRO pit_fighter
	text_asm
	ld a, \1
	ld [wPitCurFighter], a
	CheckEvent \2
	ld hl, \9 ; after he's beaten
	jr nz, .print
	IF \1 > 0
		CheckEvent \3
		ld hl, ThePitNotYetText
		jr z, .print
	ENDC
	ld hl, \6 ; the offer
	ld de, \7 ; you win
	ld bc, \8 ; you lose
	ld a, \4
	ld [wPitBetSide], a ; spare while a text runs
	ld a, \5
	jp ThePitOfferFight
.print
	call PrintText
	jp TextScriptEnd
ENDM

ThePitBikerText:
	pit_fighter 0, EVENT_PIT_BEAT_FIGHTER_1, 0, OPP_BIKER, 16, \
		.OfferText, .YouWinText, .YouLoseText, .AfterText
.OfferText:
	text_far _ThePitBikerOfferText
	text_end
.YouWinText:
	text_far _ThePitBikerYouWinText
	text_end
.YouLoseText:
	text_far _ThePitBikerYouLoseText
	text_end
.AfterText:
	text_far _ThePitBikerAfterText
	text_end

ThePitRockerText:
	pit_fighter 1, EVENT_PIT_BEAT_FIGHTER_2, EVENT_PIT_BEAT_FIGHTER_1, OPP_ROCKER, 3, \
		.OfferText, .YouWinText, .YouLoseText, .AfterText
.OfferText:
	text_far _ThePitRockerOfferText
	text_end
.YouWinText:
	text_far _ThePitRockerYouWinText
	text_end
.YouLoseText:
	text_far _ThePitRockerYouLoseText
	text_end
.AfterText:
	text_far _ThePitRockerAfterText
	text_end

ThePitBlackbeltText:
	pit_fighter 2, EVENT_PIT_BEAT_FIGHTER_3, EVENT_PIT_BEAT_FIGHTER_2, OPP_BLACKBELT, 10, \
		.OfferText, .YouWinText, .YouLoseText, .AfterText
.OfferText:
	text_far _ThePitBlackbeltOfferText
	text_end
.YouWinText:
	text_far _ThePitBlackbeltYouWinText
	text_end
.YouLoseText:
	text_far _ThePitBlackbeltYouLoseText
	text_end
.AfterText:
	text_far _ThePitBlackbeltAfterText
	text_end

ThePitOfferFight:
; hl = offer, de = text if you win, bc = text if you lose,
; [wPitBetSide] and a = the trainer to fight
	ld [wTrainerNo], a
	push bc
	push de
	call PrintText
	call YesNoChoice
	ld a, [wCurrentMenuItem]
	and a
	jr nz, .no
	ld hl, PitEntryFee
	ld de, hMoney
	ld bc, 3
	call CopyData
	call HasEnoughMoney
	jr c, .noMoney
	ld hl, hMoney + 2
	ld de, wPlayerMoney + 2
	ld c, 3
	predef SubBCDPredef
	ld a, SFX_PURCHASE
	call PlaySoundWaitForCurrent
	call WaitForSoundToFinish
	ld hl, ThePitIntoTheRingText
	call PrintText
	pop hl ; you win
	pop de ; you lose
	ld a, [wPitBetSide]
	jr ThePitStartFight

.no
	pop de
	pop bc
	ld hl, ThePitNoText
	call PrintText
	jp TextScriptEnd

.noMoney
	pop de
	pop bc
	ld hl, ThePitNoMoneyText
	call PrintText
	jp TextScriptEnd

ThePitStartFight:
; fight trainer a (team [wTrainerNo]) with end texts hl (you win), de (you lose)
	ld [wCurOpponent], a
	call SaveEndBattleTextPointers
	ldh a, [hSpriteIndex]
	ld [wSpriteIndex], a
	ld hl, wStatusFlags3
	set BIT_TALKED_TO_TRAINER, [hl]
	set BIT_PRINT_END_BATTLE_TEXT, [hl]
	ld a, SCRIPT_THEPIT_AFTER_FIGHT
	ld [wThePitCurScript], a
	jp TextScriptEnd

PitEntryFee:
	db $00, $20, $00 ; ¥2000

; the purse for each undercard fight, then OLD IRON's
PitPurses:
	db $00, $60, $00 ; ¥6000
	db $00, $70, $00 ; ¥7000
	db $00, $80, $00 ; ¥8000
	db $02, $00, $00 ; ¥20000

ThePitPayPurse:
	ld a, [wPitCurFighter]
	ld c, a
	add a
	add c
	ld c, a
	ld b, 0
	ld hl, PitPurses
	add hl, bc
	ld de, hMoney
	ld bc, 3
	call CopyData
	ld hl, hMoney + 2
	ld de, wPlayerMoney + 2
	ld c, 3
	predef AddBCDPredef
	ld a, SFX_PURCHASE
	call PlaySoundWaitForCurrent
	jp WaitForSoundToFinish

ThePitNotYetText:
	text_far _ThePitNotYetText
	text_end

ThePitNoText:
	text_far _ThePitNoText
	text_end

ThePitNoMoneyText:
	text_far _ThePitNoMoneyText
	text_end

ThePitIntoTheRingText:
	text_far _ThePitIntoTheRingText
	text_end

ThePitWonText:
	text_asm
	call ThePitPayPurse
	ld hl, .PurseText
	call PrintText
	ld a, [wPitCurFighter]
	cp 2
	jr nz, .done
	SetEvent EVENT_PIT_BOSS_SENT_FOR_YOU
	ld hl, .BossWantsYouText
	call PrintText
.done
	jp TextScriptEnd

.PurseText:
	text_far _ThePitPurseText
	text_end

.BossWantsYouText:
	text_far _ThePitBossWantsYouText
	text_end

ThePitLostText:
	text_far _ThePitLostText
	text_end

ThePitBeatOldIronText:
	text_asm
	ld hl, .DownText
	call PrintText
	call ThePitPayPurse
	ld hl, .PurseText
	call PrintText
	jp TextScriptEnd

.DownText:
	text_far _ThePitOldIronDownText
	text_end

.PurseText:
	text_far _ThePitBigPurseText
	text_end

ThePitLostToOldIronText:
	text_far _ThePitLostToOldIronText
	text_end

ThePitBookieText:
; after three wins, the main event: take ¥50000 to lose to OLD IRON, or fight
	text_asm
	CheckEvent EVENT_PIT_MAIN_EVENT_DONE
	jr z, .notDone
	CheckEvent EVENT_PIT_IS_RING_VENUE
	jr z, .notRingVenue
	ld hl, .OldFriendText ; even if you cost him a fortune
	call PrintText
	ld hl, .NoHardFeelingsText
	CheckEvent EVENT_PIT_BEAT_OLD_IRON
	jr nz, .print
	jp TextScriptEnd
.notRingVenue
	ld hl, .CostMeAFortuneText
	CheckEvent EVENT_PIT_BEAT_OLD_IRON
	jr nz, .print
	ld hl, .PleasureText
	CheckEvent EVENT_PIT_THREW_FIGHT
	jr nz, .print
	ld hl, .ShouldveTakenItText
	jr .print
.notDone
	ld hl, .WhoLetYouInText
	CheckEvent EVENT_PIT_IS_RING_VENUE
	jr z, .gotGreeting
	ld hl, .WelcomeToTheRingText
.gotGreeting
	CheckEvent EVENT_PIT_BOSS_SENT_FOR_YOU
	jr z, .print
	ld hl, .OfferText
	call PrintText
	call YesNoChoice
	ld a, [wCurrentMenuItem]
	and a
	jr nz, .refused
	; took it: the fight is thrown, and paid for
	ld hl, .ThrownText
	call PrintText
	ld a, ONIX ; OLD IRON
	call PlayCry
	ld hl, .BooText
	call PrintText
	ld hl, PitBribe
	ld de, hMoney
	ld bc, 3
	call CopyData
	ld hl, hMoney + 2
	ld de, wPlayerMoney + 2
	ld c, 3
	predef AddBCDPredef
	ld a, SFX_PURCHASE
	call PlaySoundWaitForCurrent
	call WaitForSoundToFinish
	SetEvent EVENT_PIT_MAIN_EVENT_DONE
	SetEvent EVENT_PIT_THREW_FIGHT
	ld hl, .PaidText
.print
	call PrintText
	jp TextScriptEnd

.refused
	ld hl, .YourFuneralText
	call PrintText
	ld a, PIT_MAIN_EVENT
	ld [wPitCurFighter], a
	ld a, 6
	ld [wTrainerNo], a
	ld hl, .YouWinText
	ld de, .YouLoseText
	ld a, OPP_GENTLEMAN
	jp ThePitStartFight

.WhoLetYouInText:
	text_far _ThePitBookieWhoLetYouInText
	text_end

.WelcomeToTheRingText:
	text_far _ThePitBookieWelcomeToTheRingText
	text_end

.OldFriendText:
	text_far _ThePitBookieOldFriendText
	text_end

.NoHardFeelingsText:
	text_far _ThePitBookieNoHardFeelingsText
	text_end

.OfferText:
	text_far _ThePitBookieOfferText
	text_end

.ThrownText:
	text_far _ThePitBookieThrownText
	text_end

.BooText:
	text_far _ThePitBookieBooText
	text_end

.PaidText:
	text_far _ThePitBookiePaidText
	text_end

.YourFuneralText:
	text_far _ThePitBookieYourFuneralText
	text_end

.YouWinText:
	text_far _ThePitOldIronYouWinText
	text_end

.YouLoseText:
	text_far _ThePitOldIronYouLoseText
	text_end

.PleasureText:
	text_far _ThePitBookiePleasureText
	text_end

.CostMeAFortuneText:
	text_far _ThePitBookieCostMeAFortuneText
	text_end

.ShouldveTakenItText:
	text_far _ThePitBookieShouldveTakenItText
	text_end

PitBribe:
	db $05, $00, $00 ; ¥50000

ThePitBirdText:
	text_far _ThePitBirdText
	text_end

ThePitBeautyText:
	text_far _ThePitBeautyText
	text_end

ThePitMiddleAgedManText:
	text_far _ThePitMiddleAgedManText
	text_end

ThePitBaldingGuyText:
	text_far _ThePitBaldingGuyText
	text_end

ThePitGamblerText:
	text_asm
	ld hl, .Text
	CheckEvent EVENT_PIT_MAIN_EVENT_DONE
	jr z, .print
	ld hl, .RetiredText
.print
	call PrintText
	jp TextScriptEnd
.Text:
	text_far _ThePitGamblerText
	text_end
.RetiredText:
	text_far _ThePitGamblerRetiredText
	text_end
