JunglefowlHut_Script:
	call EnableAutoTextBoxDrawing
; After a blackout on the island you wake up in here. A blackout leaves
; wLastMap pointing elsewhere, so point it back at the island (for the
; palette) and tell the player how they got here.
	CheckAndResetEvent EVENT_CASTAWAY_CARRIED_YOU
	ret z
	ld a, JUNGLEFOWL_ISLAND
	ld [wLastMap], a
	ld b, SET_PAL_OVERWORLD
	call RunPaletteCommand
	ld a, TEXT_JUNGLEFOWLHUT_CARRIED_YOU
	ldh [hTextID], a
	jp DisplayTextID

JunglefowlHut_TextPointers:
	def_text_pointers
	dw_const JunglefowlHutCastawayText,   TEXT_JUNGLEFOWLHUT_CASTAWAY
	dw_const JunglefowlHutShelfText,      TEXT_JUNGLEFOWLHUT_SHELF
	dw_const JunglefowlHutCarriedYouText, TEXT_JUNGLEFOWLHUT_CARRIED_YOU

JunglefowlHutCastawayText:
	text_asm
	CheckEvent EVENT_CASTAWAY_HEARD_ABOUT_RING
	jr nz, .heardAboutRing
	ld hl, .WhatsARingText
	call PrintText
	SetEvent EVENT_CASTAWAY_HEARD_ABOUT_RING
	call .GiveSailIfReady ; you may already have the other two parts
	jr .offerBalls
.heardAboutRing
	call .GiveSailIfReady
	jr nz, .offerBalls
	CheckEvent EVENT_CASTAWAY_SAW_YOU_CATCH
	jr nz, .hint
	call .CaughtAJunglefowl
	jr z, .hint
	SetEvent EVENT_CASTAWAY_SAW_YOU_CATCH
	ld hl, .SawYouInTheGrassText
	call PrintText
	jr .offerBalls
.hint
	ld hl, .NeedARaftText
	CheckEvent EVENT_GOT_SAIL
	jr z, .printHint
	ld hl, .GoToTheJettyText
.printHint
	call PrintText
.offerBalls
	CheckEvent EVENT_GOT_CASTAWAY_BALLS
	jr nz, .rest
	ld hl, .TakeTheseText
	call PrintText
	lb bc, POKE_BALL, 5
	call GiveItem
	jr nc, .bagFull
	SetEvent EVENT_GOT_CASTAWAY_BALLS
	ld hl, .GotBallsText
	call PrintText
	jr .rest
.bagFull
	ld hl, .BagFullText
	call PrintText
.rest
; no COCK CENTER out here, so he puts you up every time
	ld hl, .LieDownText
	call PrintText
	call GBFadeOutToWhite
	call ReloadMapData
	predef HealParty
	ld a, MUSIC_PKMN_HEALED
	ld [wNewSoundID], a
	call PlaySound
.waitForJingle
	ld a, [wChannelSoundIDs]
	cp MUSIC_PKMN_HEALED
	jr z, .waitForJingle
	ld a, [wMapMusicSoundID]
	ld [wNewSoundID], a
	call PlaySound
	call GBFadeInFromWhite
	ld hl, .BetterText
	call PrintText
	jp TextScriptEnd

.GiveSailIfReady:
; nz if he handed over the SAIL just now
	CheckEvent EVENT_GOT_SAIL
	jr nz, .noSail
	CheckEvent EVENT_GOT_DRIFTWOOD
	jr z, .noSail
	CheckEvent EVENT_GOT_VINE_ROPE
	jr z, .noSail
	ld hl, .TakeTheSailText
	call PrintText
	SetEvent EVENT_GOT_SAIL
	or 1
	ret
.noSail
	xor a
	ret

.CaughtAJunglefowl:
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

.WhatsARingText:
	text_far _JunglefowlHutWhatsARingText
	text_end

.TakeTheSailText:
	text_far _JunglefowlHutTakeTheSailText
	sound_get_item_1
	text_far _JunglefowlHutTieItTogetherText
	text_end

.SawYouInTheGrassText:
	text_far _JunglefowlHutSawYouInTheGrassText
	text_end

.NeedARaftText:
	text_far _JunglefowlHutNeedARaftText
	text_end

.GoToTheJettyText:
	text_far _JunglefowlHutGoToTheJettyText
	text_end

.TakeTheseText:
	text_far _JunglefowlHutTakeTheseText
	text_end

.GotBallsText:
	text_far _JunglefowlHutGotBallsText
	sound_get_item_1
	text_far _JunglefowlHutRoundThingsText
	text_end

.BagFullText:
	text_far _JunglefowlHutBagFullText
	text_end

.LieDownText:
	text_far _JunglefowlHutLieDownText
	text_end

.BetterText:
	text_far _JunglefowlHutBetterText
	text_end

JunglefowlHutShelfText:
	text_far _JunglefowlHutShelfText
	text_end

JunglefowlHutCarriedYouText:
	text_far _JunglefowlHutCarriedYouText
	text_end
