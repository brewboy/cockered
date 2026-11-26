FujiFarmHouse_Script:
	ld a, 1 ; the farm sorts itself out when you step back outside
	ld [wFarmNeedsSync], a
	jp EnableAutoTextBoxDrawing

FujiFarmHouse_TextPointers:
	def_text_pointers
	dw_const FujiFarmHouseFarmerText, TEXT_FUJIFARMHOUSE_FARMER
	dw_const FujiFarmHouseNestText,   TEXT_FUJIFARMHOUSE_NEST

FarmGifts:
; one for every FARM_GIFT_EVERY breeds retired
	db RARE_CANDY
	db PP_UP
	db NUGGET
	db MAX_REVIVE
	db MAX_ELIXER
	db HP_UP
	db PP_UP
	db RARE_CANDY
	db NUGGET
	db MASTER_BALL
	assert NUM_FARM_GIFTS == @ - FarmGifts

FujiFarmHouseFarmerText:
; retire a bird from your party: it stays on the farm for good
	text_asm
	call SaveScreenTilesToBuffer2
	CheckEvent EVENT_FUJI_FARM_MET_FARMER
	jr nz, .met
	SetEvent EVENT_FUJI_FARM_MET_FARMER
	ld hl, .IntroText
	call PrintText
.met
	call FarmGiveDueGifts
	ld hl, .RetireOfferText
	call PrintText
	call YesNoChoice
	ld a, [wCurrentMenuItem]
	and a
	ld hl, .ComeBackText
	jp nz, .done
	ld a, [wPartyCount]
	dec a
	ld hl, .LastBirdText
	jp z, .done
	ld hl, .WhichBirdText
	call PrintText
	xor a
	ld [wUpdateSpritesEnabled], a
	ld [wPartyMenuTypeOrMessageID], a
	ld [wMenuItemToSwap], a
	call DisplayPartyMenu
	push af
	call GBPalWhiteOutWithDelay3
	call RestoreScreenTilesAndReloadTilePatterns
	call LoadGBPal
	pop af
	ld hl, .ChangedMindText
	jp c, .done
	callfar KnowsHMMove
	ld hl, .KnowsHMText
	jp c, .done
	xor a
	ld [wPartyAndBillsPCSavedMenuItem], a
	ld a, [wWhichPokemon]
	ld hl, wPartyMonNicks
	call GetPartyMonName
	ld hl, .SureText
	call PrintText
	call YesNoChoice
	ld a, [wCurrentMenuItem]
	and a
	ld hl, .ChangedMindText
	jp nz, .done
; it waits by the gate, by name
	ld a, [wWhichPokemon]
	ld hl, wPartyMonNicks
	call GetPartyMonName
	ld hl, wNameBuffer
	ld de, wFarmNewcomerName
	ld bc, NAME_LENGTH
	call CopyData
	ld hl, wPartySpecies
	ld a, [wWhichPokemon]
	ld c, a
	ld b, 0
	add hl, bc
	ld a, [hl]
	ld [wFarmNewcomerSpecies], a
	xor a
	ld [wRemoveMonFromBox], a
	call RemovePokemon
	ld a, [wFarmNewcomerSpecies]
	call PlayCry
	ld hl, .WanderedOffText
	call PrintText
	ld a, [wFarmNewcomerSpecies]
	call FarmRecordBreed
	jr z, .notNew
	ld hl, .NewBreedText
	call PrintText
	call FarmGiveDueGifts
.notNew
	ld hl, .AtTheGateText
.done
	call PrintText
	jp TextScriptEnd

.IntroText:
	text_far _FujiFarmHouseFarmerIntroText
	text_end

.RetireOfferText:
	text_far _FujiFarmHouseFarmerRetireOfferText
	text_end

.ComeBackText:
	text_far _FujiFarmHouseFarmerComeBackText
	text_end

.LastBirdText:
	text_far _FujiFarmHouseFarmerLastBirdText
	text_end

.WhichBirdText:
	text_far _FujiFarmHouseFarmerWhichBirdText
	text_end

.ChangedMindText:
	text_far _FujiFarmHouseFarmerChangedMindText
	text_end

.KnowsHMText:
	text_far _FujiFarmHouseFarmerKnowsHMText
	text_end

.SureText:
	text_far _FujiFarmHouseFarmerSureText
	text_end

.WanderedOffText:
	text_far _FujiFarmHouseFarmerWanderedOffText
	text_end

.NewBreedText:
	text_far _FujiFarmHouseFarmerNewBreedText
	text_end

.AtTheGateText:
	text_far _FujiFarmHouseFarmerAtTheGateText
	text_end

FarmGiveDueGifts:
; hand over every gift you've earned and not had yet
	ld a, [wFarmGiftsGiven]
	cp NUM_FARM_GIFTS
	ret nc
	inc a
	ld b, a
	xor a
.times5
	add FARM_GIFT_EVERY
	dec b
	jr nz, .times5
	ld b, a
	push bc
	call FarmCountRetiredBreeds
	pop bc
	cp b
	ret c
	ld hl, .GiftText
	call PrintText
	ld a, [wFarmGiftsGiven]
	ld e, a
	ld d, 0
	ld hl, FarmGifts
	add hl, de
	ld b, [hl]
	ld c, 1
	call GiveItem
	jr nc, .bagFull
	ld hl, wFarmGiftsGiven
	inc [hl]
	ld hl, .ReceivedText
	call PrintText
	jr FarmGiveDueGifts
.bagFull
	ld hl, .BagFullText
	jp PrintText

.GiftText:
	text_far _FujiFarmHouseFarmerGiftText
	text_end

.ReceivedText:
	text_far _FujiFarmHouseFarmerReceivedText
	sound_get_item_1
	text_end

.BagFullText:
	text_far _FujiFarmHouseFarmerBagFullText
	text_end

FujiFarmHouseNestText:
; the farm's free rest, like the castaway's hut
	text_asm
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

.LieDownText:
	text_far _FujiFarmHouseNestText
	text_end

.BetterText:
	text_far _FujiFarmHouseNestBetterText
	text_end
