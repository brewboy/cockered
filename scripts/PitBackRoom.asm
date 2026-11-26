INCLUDE "data/events/pit_fights.asm"

PitBackRoom_Script:
	call EnableAutoTextBoxDrawing
	ld hl, PitBackRoom_ScriptPointers
	ld a, [wPitBackRoomCurScript]
	jp CallFunctionInTable

PitBackRoom_ScriptPointers:
	def_script_pointers
	dw_const PitBackRoomDefaultScript,    SCRIPT_PITBACKROOM_DEFAULT
	dw_const PitBackRoomPushedOutScript,  SCRIPT_PITBACKROOM_PUSHED_OUT

PitBackRoomDefaultScript:
; the doorman checks you at the door: in if the runner sent you, out if not
	ld a, [wYCoord]
	cp 9
	ret nz
	CheckEvent EVENT_PIT_LET_IN
	ret nz
	CheckEvent EVENT_PIT_IS_RING_VENUE ; open to all now
	ret nz
	ld a, PAD_SELECT | PAD_START | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	xor a
	ldh [hJoyHeld], a
	ld a, PITBACKROOM_DOORMAN
	ldh [hSpriteIndex], a
	ld a, SPRITE_FACING_LEFT
	ldh [hSpriteFacingDirection], a
	call SetSpriteFacingDirectionAndDelay
	ld a, TEXT_PITBACKROOM_DOORMAN
	ldh [hTextID], a
	call DisplayTextID
	CheckEvent EVENT_PIT_LET_IN ; set by his text if you were invited
	jr z, .pushOut
	xor a
	ld [wJoyIgnore], a
	ret
.pushOut
	xor a
	ld [wJoyIgnore], a
	ld a, SPRITE_FACING_DOWN
	ld [wSpritePlayerStateData1FacingDirection], a
	ld a, 1
	ld [wSimulatedJoypadStatesIndex], a
	ld a, PAD_DOWN
	ld [wSimulatedJoypadStatesEnd], a
	call StartSimulatingJoypadStates
	ld a, SCRIPT_PITBACKROOM_PUSHED_OUT
	ld [wPitBackRoomCurScript], a
	ret

PitBackRoomPushedOutScript:
	ld a, [wSimulatedJoypadStatesIndex]
	and a
	ret nz
	xor a ; SCRIPT_PITBACKROOM_DEFAULT
	ld [wJoyIgnore], a
	ld [wPitBackRoomCurScript], a
	ret

PitBackRoom_TextPointers:
	def_text_pointers
	dw_const PitBackRoomClerkText,       TEXT_PITBACKROOM_CLERK
	dw_const PitBackRoomDoormanText,     TEXT_PITBACKROOM_DOORMAN
	dw_const PitBackRoomStairsGuardText, TEXT_PITBACKROOM_STAIRS_GUARD
	dw_const PitBackRoomLoserText,       TEXT_PITBACKROOM_LOSER
	dw_const PitBackRoomRegularText,     TEXT_PITBACKROOM_REGULAR
	dw_const PitBackRoomBoardText,       TEXT_PITBACKROOM_BOARD

PitBackRoomDoormanText:
	text_asm
	ld hl, .RingBadgeText
	CheckEvent EVENT_PIT_IS_RING_VENUE
	jr nz, .print
	ld hl, .NoTroubleText
	CheckEvent EVENT_PIT_LET_IN
	jr nz, .print
	ld hl, .MembersOnlyText
	CheckEvent EVENT_PIT_INVITED
	jr z, .print
	SetEvent EVENT_PIT_LET_IN
	ld hl, .KnockTwiceText
.print
	call PrintText
	jp TextScriptEnd

.MembersOnlyText:
	text_far _PitBackRoomDoormanMembersOnlyText
	text_end

.KnockTwiceText:
	text_far _PitBackRoomDoormanKnockTwiceText
	text_end

.NoTroubleText:
	text_far _PitBackRoomDoormanNoTroubleText
	text_end

.RingBadgeText:
	text_far _PitBackRoomDoormanRingBadgeText
	text_end

PitBackRoomStairsGuardText:
	text_far _PitBackRoomStairsGuardText
	text_end

PitBackRoomLoserText:
	pit_era_text .Text, .RingText
.Text:
	text_far _PitBackRoomLoserText
	text_end
.RingText:
	text_far _PitBackRoomLoserRingText
	text_end

PitBackRoomRegularText:
	pit_era_text .Text, .RingText
.Text:
	text_far _PitBackRoomRegularText
	text_end
.RingText:
	text_far _PitBackRoomRegularRingText
	text_end

PitBackRoomBoardText:
; the chalkboard: tonight's fight and the odds
	text_asm
	call PitSetUpFight
	ld hl, .SanctionedText
	CheckEvent EVENT_PIT_IS_RING_VENUE
	call nz, PrintText
	xor a
	call PitLoadBoardLine
	ld hl, .FavText
	call PrintText
	ld a, 1
	call PitLoadBoardLine
	ld hl, .OutText
	call PrintText
	jp TextScriptEnd

.SanctionedText:
	text_far _PitBackRoomBoardSanctionedText
	text_end

.FavText:
	text_far _PitBackRoomBoardFavText
	text_end

.OutText:
	text_far _PitBackRoomBoardOutText
	text_end

PitBackRoomClerkText:
; the betting window
	text_asm
	CheckEvent EVENT_PIT_IS_RING_VENUE
	jr nz, .open
	CheckEvent EVENT_PIT_BEAT_OLD_IRON
	jr z, .open
	ld hl, .MoneyNoGoodText
	call PrintText
	jp TextScriptEnd
.open
	call SaveScreenTilesToBuffer2
	call PitSetUpFight
	xor a
	call PitLoadSide
	ld hl, .FavText
	call PrintText
	ld a, 1
	call PitLoadSide
	ld hl, .OutText
	call PrintText

	ld hl, .WhoText
	call PrintText
	call PitShowMoney
	call PitBirdMenu
	jp c, .cancel
	ld [wPitBetSide], a

	call LoadScreenTilesFromBuffer2
	ld hl, .HowMuchText
	call PrintText
	call PitShowMoney
	call PitStakeMenu
	jp c, .cancel
	ld [wPitBetStake], a
	call LoadScreenTilesFromBuffer2
	call PitStakeToHMoney
	call HasEnoughMoney
	jr nc, .takeBet
	ld hl, .CantAffordText
	call PrintText
	jp TextScriptEnd

.takeBet
	ld hl, hMoney + 2
	ld de, wPlayerMoney + 2
	ld c, 3
	predef SubBCDPredef
	ld a, SFX_PURCHASE
	call PlaySoundWaitForCurrent
	call WaitForSoundToFinish
	call PitShowMoney
	ld hl, .YoureOnText
	call PrintText

	call PitRunFight
	ld hl, wPitFight ; next time, the next fight on the card
	inc [hl]
	ld a, [wPitResult]
	and a
	jr z, .noContest
	dec a
	ld b, a
	ld a, [wPitBetSide]
	cp b
	jr nz, .lost
	; won: odds payout, stake included
	ld c, a
	ld b, 0
	ld hl, wPitOdds
	add hl, bc
	ld a, [hl]
	call PitPayoutToHMoney
	ld hl, hMoney + 2
	ld de, wPlayerMoney + 2
	ld c, 3
	predef AddBCDPredef
	ld a, SFX_PURCHASE
	call PlaySoundWaitForCurrent
	call WaitForSoundToFinish
	call PitShowMoney
	ld hl, .WonText
	call PrintText
	jp TextScriptEnd

.lost
	ld hl, .LostText
	call PrintText
	jp TextScriptEnd

.noContest
	ld hl, .NoContestText
	call PrintText
	jp TextScriptEnd

.cancel
	call LoadScreenTilesFromBuffer2
	ld hl, .SuitYourselfText
	call PrintText
	jp TextScriptEnd

.MoneyNoGoodText:
	text_far _PitBackRoomClerkMoneyNoGoodText
	text_end

.FavText:
	text_far _PitBackRoomClerkFavText
	text_end

.OutText:
	text_far _PitBackRoomClerkOutText
	text_end

.WhoText:
	text_far _PitBackRoomClerkWhoText
	text_end

.HowMuchText:
	text_far _PitBackRoomClerkHowMuchText
	text_end

.CantAffordText:
	text_far _PitBackRoomClerkCantAffordText
	text_end

.SuitYourselfText:
	text_far _PitBackRoomClerkSuitYourselfText
	text_end

.YoureOnText:
	text_far _PitBackRoomClerkYoureOnText
	text_end

.WonText:
	text_far _PitBackRoomClerkWonText
	text_end

.LostText:
	text_far _PitBackRoomClerkLostText
	text_end

.NoContestText:
	text_far _PitBackRoomClerkNoContestText
	text_end

PitShowMoney:
	ld a, MONEY_BOX
	ld [wTextBoxID], a
	jp DisplayTextBoxID

PitSetUpFight:
; load the fight at wPitFight on the card into wPitBirds, wPitOdds and
; wPitFavChance
	ld a, [wPitFight]
	and NUM_PIT_FIGHTS - 1
	ld [wPitFight], a
	ld c, a
	add a
	add c
	ld c, a
	ld b, 0
	ld hl, PitCard
	add hl, bc
	ld a, [hli]
	ld [wPitBirds], a
	ld a, [hli]
	ld [wPitBirds + 1], a
	ld a, [hl]
	ld c, a
	add a
	add c
	ld c, a
	ld b, 0
	ld hl, PitOddsTypes
	add hl, bc
	ld a, [hli]
	ld [wPitOdds], a
	ld a, [hli]
	ld [wPitOdds + 1], a
	ld a, [hl]
	ld [wPitFavChance], a
	ret

PitSideBird:
; a = side (0 favourite, 1 outsider) -> a = bird
	ld c, a
	ld b, 0
	ld hl, wPitBirds
	add hl, bc
	ld a, [hl]
	ret

PitCopyBirdName:
; copy bird a's name to de
	ld l, a
	ld h, 0
	add hl, hl
	add hl, hl
	add hl, hl
	ld bc, PitBirdNames
	add hl, bc
	ld bc, PIT_BIRD_NAME_LENGTH
	jp CopyData

PitBirdSpecies:
; a = bird -> a = its species
	ld c, a
	ld b, 0
	ld hl, PitBirdSpeciesTable
	add hl, bc
	ld a, [hl]
	ret

PitLoadSide:
; side a's name to wStringBuffer and its breed to wNameBuffer
	call PitSideBird
	push af
	ld de, wStringBuffer
	call PitCopyBirdName
	pop af
	call PitBirdSpecies
	ld [wNamedObjectIndex], a
	jp GetMonName

PitLoadBoardLine:
; side a's name to wStringBuffer and its odds to wNameBuffer
	push af
	call PitSideBird
	ld de, wStringBuffer
	call PitCopyBirdName
	pop af
	ld de, wNameBuffer
	; fallthrough

PitCopyOdds:
; copy side a's odds to de
	push de
	ld c, a
	ld b, 0
	ld hl, wPitOdds
	add hl, bc
	ld a, [hl]
	ld l, a
	ld h, 0
	add hl, hl
	add hl, hl
	add hl, hl
	ld bc, PitOddsStrings
	add hl, bc
	pop de
	ld bc, PIT_ODDS_LENGTH
	jp CopyData

PitStartMenu:
; draw a menu box at hl (b rows, c columns inside), items from row d
	push de
	push bc
	push hl
	xor a
	ld [wCurrentMenuItem], a
	ld [wLastMenuItem], a
	ld a, PAD_A | PAD_B
	ld [wMenuWatchedKeys], a
	ld a, 1
	ld [wTopMenuItemX], a
	ld hl, wStatusFlags5
	set BIT_NO_TEXT_DELAY, [hl]
	pop hl
	pop bc
	call TextBoxBorder
	pop de
	ld a, d
	ld [wTopMenuItemY], a
	ret

PitFinishMenu:
; returns the chosen item in a, or carry if B or the last item (CANCEL)
	call UpdateSprites ; puts sprites behind the box
	ld hl, wStatusFlags5
	res BIT_NO_TEXT_DELAY, [hl]
	call HandleMenuInput
	bit B_PAD_B, a
	jr nz, .cancel
	ld a, [wMaxMenuItem]
	ld b, a
	ld a, [wCurrentMenuItem]
	cp b
	jr z, .cancel
	and a
	ret
.cancel
	scf
	ret

PitBirdMenu:
	hlcoord 0, 5
	lb bc, 5, 16
	ld d, 6
	call PitStartMenu
	ld a, 2
	ld [wMaxMenuItem], a
	xor a
	call PitLoadBoardLine
	hlcoord 2, 6
	ld de, wStringBuffer
	call PlaceString
	hlcoord 11, 6
	ld de, wNameBuffer
	call PlaceString
	ld a, 1
	call PitLoadBoardLine
	hlcoord 2, 8
	ld de, wStringBuffer
	call PlaceString
	hlcoord 11, 8
	ld de, wNameBuffer
	call PlaceString
	hlcoord 2, 10
	ld de, PitCancelString
	call PlaceString
	jp PitFinishMenu

PitStakeMenu:
	hlcoord 0, 3
	lb bc, 7, 8
	ld d, 4
	call PitStartMenu
	ld a, NUM_PIT_STAKES
	ld [wMaxMenuItem], a
	hlcoord 2, 4
	ld de, PitStakesString
	call PlaceString
	jp PitFinishMenu

PitStakeToHMoney:
	ld a, [wPitBetStake]
	ld c, a
	add a
	add c
	ld c, a
	ld b, 0
	ld hl, PitStakes
	add hl, bc
	ld de, hMoney
	ld bc, 3
	jp CopyData

PitPayoutToHMoney:
; a = odds; what a winning bet at wPitBetStake gets back
	ld c, a
	add a
	add c
	ld c, a
	ld a, [wPitBetStake]
	add c
	ld c, a
	add a
	add c
	ld c, a
	ld b, 0
	ld hl, PitPayouts
	add hl, bc
	ld de, hMoney
	ld bc, 3
	jp CopyData

PitRunFight:
; settle the fight first, then tell it as the shouts come up the stairs
	call Random
	cp PIT_NO_CONTEST_CHANCE
	ld b, 0
	jr c, .settled
	call Random
	ld c, a
	ld a, [wPitFavChance]
	ld b, a
	ld a, c
	cp b
	ld b, 1
	jr c, .settled
	inc b
.settled
	ld a, b
	ld [wPitResult], a

	call Random
	and 1
	push af
	call PitExchange
	ld hl, PitCrowdRoarsText
	call PrintText
	pop af
	xor 1
	call PitExchange

	ld a, [wPitResult]
	and a
	jr nz, .finish
	ld hl, PitBothDownText
	jp PrintText
.finish
	dec a
	call PitLoadAttacker
	ld hl, PitFinishText
	jp PrintText

PitLoadAttacker:
; side a's name to wStringBuffer, the other's to wNameBuffer, and a's cry
	push af
	call PitSideBird
	ld de, wStringBuffer
	call PitCopyBirdName
	pop af
	push af
	xor 1
	call PitSideBird
	ld de, wNameBuffer
	call PitCopyBirdName
	pop af
	call PitSideBird
	call PitBirdSpecies
	jp PlayCry

PitExchange:
	call PitLoadAttacker
	call Random
	and %11
	add a
	ld c, a
	ld b, 0
	ld hl, PitBlowTexts
	add hl, bc
	ld a, [hli]
	ld h, [hl]
	ld l, a
	jp PrintText

PitBlowTexts:
	dw PitGoesForTheEyesText
	dw PitSpursText
	dw PitDownAndUpText
	dw PitDrivesBackText

PitGoesForTheEyesText:
	text_far _PitGoesForTheEyesText
	text_end

PitSpursText:
	text_far _PitSpursText
	text_end

PitDownAndUpText:
	text_far _PitDownAndUpText
	text_end

PitDrivesBackText:
	text_far _PitDrivesBackText
	text_end

PitCrowdRoarsText:
	text_far _PitCrowdRoarsText
	text_end

PitBothDownText:
	text_far _PitBothDownText
	text_end

PitFinishText:
	text_far _PitFinishText
	text_end

