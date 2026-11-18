; Game Boy Color support for Rooster Edition.
;
; On a GBC the game runs in colour mode and reuses the SGB palette commands:
; each PAL_SET packet picks four SuperPalettes for BG palettes 0-3, and each
; ATTR_BLK packet is turned into the BG attribute maps (VRAM bank 1) of both
; tilemaps. The DMG palette registers keep working as before: whenever rBGP,
; rOBP0 or rOBP1 change, the VBlank handler maps the four shades through them
; into the colour palettes, so every existing fade and flash still works.
; OBJ palettes 0 and 1 use the colours of BG palette 0 through OBP0 and OBP1.

; Scratch bytes for decoding ATTR_BLK data sets (HRAM is full, and the
; multiplication scratch space is free whenever this runs).
DEF hCGBInsidePal  EQUS "hMultiplicand"
DEF hCGBOutsidePal EQUS "hMultiplicand + 1"
DEF hCGBLinePal    EQUS "hMultiplicand + 2"
DEF hCGBRowClass   EQUS "hMultiplier"

; Set up colour mode: called by LoadSGB on a GBC.
CGBInit:
	ld hl, vBGMap0
	ld bc, 2 * TILEMAP_AREA ; both tilemaps
	ld d, 0
	call CGBFillAttributes
	ld hl, wCGBPalIDs
	xor a ; PAL_ROUTE
	ld [hli], a
	ld [hli], a
	ld [hli], a
	ld [hl], a
	; fall through

; Make the next VBlank rewrite the colour palettes.
CGBRefreshPalettes:
	ldh a, [rBGP]
	cpl
	ld [wCGBLastBGP], a
	ret

; Apply a PAL_SET packet at hl and an ATTR_BLK packet at de.
CGBApplyPackets:
	inc hl ; palette IDs are the low bytes of the four words after the header
	push de
	ld de, wCGBPalIDs
	ld c, 4
.palIDLoop
	ld a, [hli]
	ld [de], a
	inc de
	inc hl
	dec c
	jr nz, .palIDLoop
	call CGBRefreshPalettes
	pop hl
	inc hl ; hl = number of data sets
	ld c, 0 ; screen row
.rowLoop
	push hl
	push hl
	ld hl, wCGBAttrRow
	ld b, SCREEN_WIDTH
	xor a
.clearRow
	ld [hli], a
	dec b
	jr nz, .clearRow
	pop hl
	ld a, [hli]
	and a
	jr z, .rowDone
	ld b, a
.setLoop
	push bc
	call CGBApplyBlkSetToRow
	pop bc
	dec b
	jr nz, .setLoop
.rowDone
	; copy the row into both tilemaps' attributes
	push bc
	ld l, c
	ld h, 0
	add hl, hl
	add hl, hl
	add hl, hl
	add hl, hl
	add hl, hl ; * TILEMAP_WIDTH
	ld de, vBGMap0
	add hl, de
	push hl
	call CGBCopyAttrRow
	pop hl
	ld de, vBGMap1 - vBGMap0
	add hl, de
	call CGBCopyAttrRow
	pop bc
	pop hl
	inc c
	ld a, c
	cp SCREEN_HEIGHT
	jr nz, .rowLoop
	ret

; Apply one ATTR_BLK data set at hl to screen row c of wCGBAttrRow.
; Returns hl past the data set and keeps c.
CGBApplyBlkSetToRow:
	ld a, [hli] ; which regions are affected
	ld b, a
	ld a, [hli] ; palettes: inside, line << 2, outside << 4
	ld d, a
	; inside palette, or -1 if unchanged
	and %11
	bit 0, b
	jr nz, .gotInside
	ld a, -1
.gotInside
	ldh [hCGBInsidePal], a
	; outside palette, or -1 if unchanged
	ld a, d
	swap a
	and %11
	bit 2, b
	jr nz, .gotOutside
	ld a, -1
.gotOutside
	ldh [hCGBOutsidePal], a
	; the line uses its own palette, or else the inside's, or else the outside's
	ld a, d
	rrca
	rrca
	and %11
	bit 1, b
	jr nz, .gotLine
	ldh a, [hCGBInsidePal]
	bit 0, b
	jr nz, .gotLine
	ldh a, [hCGBOutsidePal]
.gotLine
	ldh [hCGBLinePal], a
	ld a, [hli]
	ld d, a ; x1
	ld a, [hli]
	ld e, a ; y1
	ld a, [hli]
	ld b, a ; x2
	ld a, [hli] ; y2
	push hl
	; row class: 0 outside the block, 1 its top or bottom line, 2 in between
	ld h, a
	ld l, 0
	ld a, c
	cp e
	jr c, .gotClass ; above
	ld a, h
	cp c
	jr c, .gotClass ; below
	inc l
	ld a, c
	cp e
	jr z, .gotClass
	cp h
	jr z, .gotClass
	inc l
.gotClass
	ld a, l
	ldh [hCGBRowClass], a
	ld hl, wCGBAttrRow
	ld e, 0 ; x
.cellLoop
	ldh a, [hCGBRowClass]
	and a
	jr z, .outside
	ld a, e
	cp d
	jr c, .outside ; left of the block
	jr z, .line
	ld a, b
	cp e
	jr c, .outside ; right of the block
	jr z, .line
	ldh a, [hCGBRowClass]
	dec a
	jr z, .line
	ldh a, [hCGBInsidePal]
	jr .apply
.line
	ldh a, [hCGBLinePal]
	jr .apply
.outside
	ldh a, [hCGBOutsidePal]
.apply
	cp -1
	jr z, .next
	ld [hl], a
.next
	inc hl
	inc e
	ld a, e
	cp SCREEN_WIDTH
	jr nz, .cellLoop
	pop hl
	ret

; Copy wCGBAttrRow to the attributes at hl.
CGBCopyAttrRow:
	ld de, wCGBAttrRow
	ld c, SCREEN_WIDTH
.loop
	ld a, [de]
	inc de
	ld b, a
	call CGBWriteAttribute
	dec c
	jr nz, .loop
	ret

; Fill bc attribute bytes at hl with d.
CGBFillAttributes:
	push bc
	ld b, d
	call CGBWriteAttribute
	pop bc
	dec bc
	ld a, b
	or c
	jr nz, CGBFillAttributes
	ret

; Write b to [hl] in VRAM bank 1 and advance hl, whether or not the LCD is on.
; Interrupts are held off for the write so the VBlank handler never runs while
; bank 1 is mapped in.
CGBWriteAttribute:
	di
.wait
	ldh a, [rSTAT]
	and STAT_BUSY ; mode 2 or 3; reads as 0 when the LCD is off
	jr nz, .wait
	ld a, 1
	ldh [rVBK], a
	ld [hl], b
	inc hl
	xor a
	ldh [rVBK], a
	reti ; ei + ret

; Called from VBlank on a GBC, after OAM has been prepared.
CGBVBlank::
	call CGBFixShadowOAM
	ld hl, wCGBLastBGP
	ldh a, [rBGP]
	cp [hl]
	jr nz, .update
	inc hl
	ldh a, [rOBP0]
	cp [hl]
	jr nz, .update
	inc hl
	ldh a, [rOBP1]
	cp [hl]
	ret z
.update
	ld hl, wCGBLastBGP
	ldh a, [rBGP]
	ld [hli], a
	ldh a, [rOBP0]
	ld [hli], a
	ldh a, [rOBP1]
	ld [hl], a
	; BG palettes 0-3, each through BGP
	ld a, BGPI_AUTOINC
	ldh [rBGPI], a
	ld de, wCGBPalIDs
	ld b, 4
.bgLoop
	push bc
	ld a, [de]
	inc de
	push de
	call CGBPalAddress
	ld a, [wCGBLastBGP]
	ld d, a
	ld c, LOW(rBGPD)
	call CGBWritePal
	pop de
	pop bc
	dec b
	jr nz, .bgLoop
	; OBJ palettes 0 and 1: BG palette 0's colours through OBP0 and OBP1
	ld a, OBPI_AUTOINC
	ldh [rOBPI], a
	ld a, [wCGBPalIDs]
	call CGBPalAddress
	ld c, LOW(rOBPD)
	ld a, [wCGBLastOBP0]
	ld d, a
	push hl
	call CGBWritePal
	pop hl
	ld a, [wCGBLastOBP1]
	ld d, a
	; fall through

; Write the palette at hl to the port at c, mapping shades 0-3 through d.
CGBWritePal:
	ld e, 4
.loop
	push hl
	ld a, d
	and %11
	add a
	add l
	ld l, a
	jr nc, .noCarry
	inc h
.noCarry
.wait
	ldh a, [rSTAT]
	and STAT_BUSY ; palette RAM is locked while the PPU draws
	jr nz, .wait
	ld a, [hli]
	ldh [c], a
	ld a, [hl]
	ldh [c], a
	pop hl
	srl d
	srl d
	dec e
	jr nz, .loop
	ret

; hl = SuperPalettes entry a
CGBPalAddress:
	ld l, a
	ld h, 0
	add hl, hl
	add hl, hl
	add hl, hl
	ld de, SuperPalettes
	add hl, de
	ret

; In colour mode OAM attribute bits 0-2 pick the OBJ palette and bit 3 the
; VRAM bank, but the game keeps its own flags there. Clear them, and turn the
; DMG palette bit into OBJ palette 1. Takes effect from the next OAM DMA.
CGBFixShadowOAM:
	ld hl, wShadowOAM + OAMA_FLAGS
	ld de, OBJ_SIZE
	ld b, OAM_COUNT
.loop
	ld a, [hl]
	and %11110000
	bit B_OAM_PAL1, a
	jr z, .gotPal
	inc a
.gotPal
	ld [hl], a
	add hl, de
	dec b
	jr nz, .loop
	ret
