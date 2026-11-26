FujiFarmBarn_Script:
	ld a, 1 ; the farm sorts itself out when you step back outside
	ld [wFarmNeedsSync], a
	ld hl, wCurrentMapScriptFlags
	bit BIT_CUR_MAP_LOADED_1, [hl]
	res BIT_CUR_MAP_LOADED_1, [hl]
	call nz, FarmSyncResidents
	jp EnableAutoTextBoxDrawing

FujiFarmBarn_TextPointers:
	def_text_pointers
	dw_const FujiFarmBarnPrimefowlText, TEXT_FUJIFARMBARN_PRIMEFOWL
	dw_const FujiFarmBarnFlock1Text,    TEXT_FUJIFARMBARN_FLOCK_1
	dw_const FujiFarmBarnFlock2Text,    TEXT_FUJIFARMBARN_FLOCK_2
	dw_const FujiFarmBarnFlock3Text,    TEXT_FUJIFARMBARN_FLOCK_3
	dw_const FujiFarmBarnFlock4Text,    TEXT_FUJIFARMBARN_FLOCK_4
	dw_const FujiFarmBarnFlock5Text,    TEXT_FUJIFARMBARN_FLOCK_5
	dw_const FujiFarmBarnFlock6Text,    TEXT_FUJIFARMBARN_FLOCK_6
	dw_const FujiFarmBarnFlock7Text,    TEXT_FUJIFARMBARN_FLOCK_7
	dw_const FujiFarmBarnPhotoText,     TEXT_FUJIFARMBARN_PHOTO
	dw_const FujiFarmBarnLedgerText,    TEXT_FUJIFARMBARN_LEDGER

FujiFarmBarnPrimefowlText:
	text_asm
	ld a, PRIMEAPE ; PRIMEFOWL
	call PlayCry
	ld hl, .Text
	call PrintText
	jp TextScriptEnd

.Text:
	text_far _FujiFarmBarnPrimefowlText
	text_end

FujiFarmBarnFlock1Text:
	text_asm
	ld a, 4
	jp FarmFlockTalk

FujiFarmBarnFlock2Text:
	text_asm
	ld a, 5
	jp FarmFlockTalk

FujiFarmBarnFlock3Text:
	text_asm
	ld a, 6
	jp FarmFlockTalk

FujiFarmBarnFlock4Text:
	text_asm
	ld a, 7
	jp FarmFlockTalk

FujiFarmBarnFlock5Text:
	text_asm
	ld a, 8
	jp FarmFlockTalk

FujiFarmBarnFlock6Text:
	text_asm
	ld a, 9
	jp FarmFlockTalk

FujiFarmBarnFlock7Text:
	text_asm
	ld a, 10
	jp FarmFlockTalk

FujiFarmBarnPhotoText:
	text_far _FujiFarmBarnPhotoText
	text_end

FujiFarmBarnLedgerText:
; how many breeds you've retired, then the list; pick one to see its page
	text_asm
	call FarmCountRetiredBreeds
	and a
	ld hl, .BlankText
	jp z, .print
	ld hl, .CountText
	call PrintText
	ld a, [wFarmGiftsGiven]
	cp NUM_FARM_GIFTS
	jr nc, .readIt
	inc a
	ld b, a
	xor a
.times5
	add FARM_GIFT_EVERY
	dec b
	jr nz, .times5
	ld [wNameBuffer], a ; just somewhere to print it from
	ld hl, .NextGiftText
	call PrintText
.readIt
	ld hl, .ReadItText
	call PrintText
	call YesNoChoice
	ld a, [wCurrentMenuItem]
	and a
	jp nz, TextScriptEnd
	xor a
	ld [wListScrollOffset], a
	ld [wCurrentMenuItem], a
.list
	call .BuildList
	ld hl, wTileMapBackup2
	ld a, l
	ld [wListPointer], a
	ld a, h
	ld [wListPointer + 1], a
	xor a
	ld [wPrintItemPrices], a
	ld a, SPECIESLISTMENU
	ld [wListMenuID], a
	call DisplayListMenuID
	jp c, TextScriptEnd
	ld a, [wCurListMenuItem]
	ld [wPokedexNum], a
	ld hl, wStatusFlags5
	set BIT_NO_TEXT_DELAY, [hl]
	predef ShowPokedexData
	ld hl, wStatusFlags5
	res BIT_NO_TEXT_DELAY, [hl]
	call ReloadMapData
	jr .list

.print
	call PrintText
	jp TextScriptEnd

.BuildList:
; wTileMapBackup2 = the retired breeds as a list menu: count, species..., -1
	call FarmCountRetiredBreeds
	ld hl, wTileMapBackup2
	ld [hli], a
	ld b, a
	ld c, 0
.buildLoop
	push bc
	push hl
	ld a, c
	call FarmGetRetiredBreed
	pop hl
	pop bc
	ld [hli], a
	inc c
	ld a, c
	cp b
	jr c, .buildLoop
	ld [hl], -1
	ret

.BlankText:
	text_far _FujiFarmBarnLedgerBlankText
	text_end

.CountText:
	text_far _FujiFarmBarnLedgerCountText
	text_end

.NextGiftText:
	text_far _FujiFarmBarnLedgerNextGiftText
	text_end

.ReadItText:
	text_far _FujiFarmBarnLedgerReadItText
	text_end
