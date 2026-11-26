; The Pit's birds, its card of fights and the betting window's sums.

DEF PIT_BIRD_NAME_LENGTH EQU 8
DEF PIT_ODDS_LENGTH EQU 8
DEF PIT_NO_CONTEST_CHANCE EQU 16 ; out of 256: both birds down, the house keeps every bet

	const_def
	const PIT_RAZOR
	const PIT_BUSTER
	const PIT_DUKE
	const PIT_SPIKE
	const PIT_BRUISER
	const PIT_SCRAPS
	const PIT_SMOKEY
	const PIT_LUCKY
	const PIT_TANK
	const PIT_PEPPER
	const PIT_JACKPOT
	const PIT_PINCH
DEF NUM_PIT_BIRDS EQU const_value

PitBirdNames:
	table_width PIT_BIRD_NAME_LENGTH
	db "RAZOR@@@"
	db "BUSTER@@"
	db "DUKE@@@@"
	db "SPIKE@@@"
	db "BRUISER@"
	db "SCRAPS@@"
	db "SMOKEY@@"
	db "LUCKY@@@"
	db "TANK@@@@"
	db "PEPPER@@"
	db "JACKPOT@"
	db "PINCH@@@"
	assert_table_length NUM_PIT_BIRDS

PitBirdSpeciesTable:
	table_width 1
	db ONIX       ; SHAMONIX
	db GROWLITHE  ; CROWLITHE
	db PRIMEAPE   ; PRIMEFOWL
	db FEAROW     ; FEATHEROW
	db MACHAMP    ; MACHROOST
	db RATTATA    ; BANTATTA
	db HAUNTER    ; HAUNTCROW
	db MACHOKE    ; MACHOOK
	db TAUROS     ; TAUROOST
	db CHARMELEON ; CLUCKELEON
	db HITMONLEE  ; HITMONSPUR
	db PINSIR     ; PINSPUR
	assert_table_length NUM_PIT_BIRDS

	const_def
	const PIT_ODDS_EVENS
	const PIT_ODDS_1_TO_2
	const PIT_ODDS_3_TO_2
	const PIT_ODDS_1_TO_4
	const PIT_ODDS_4_TO_1
DEF NUM_PIT_ODDS EQU const_value

PitOddsStrings:
	table_width PIT_ODDS_LENGTH
	db "EVENS@@@"
	db "1 to 2@@"
	db "3 to 2@@"
	db "1 to 4@@"
	db "4 to 1@@"
	assert_table_length NUM_PIT_ODDS

; Each kind of fight: the favourite's odds, the outsider's, and the
; favourite's chance of winning out of 256. With the no-contest chance on
; top, every bet loses about a tenth on average: the house always wins.
	const_def
	const PIT_EVEN_FIGHT
	const PIT_FAVOURITE_FIGHT
	const PIT_LONG_SHOT_FIGHT
DEF NUM_PIT_FIGHT_KINDS EQU const_value

PitOddsTypes:
	table_width 3
	db PIT_ODDS_EVENS,  PIT_ODDS_EVENS,  128
	db PIT_ODDS_1_TO_2, PIT_ODDS_3_TO_2, 160
	db PIT_ODDS_1_TO_4, PIT_ODDS_4_TO_1, 205
	assert_table_length NUM_PIT_FIGHT_KINDS

; tonight's card, in order and then round again: favourite, outsider, kind
PitCard:
	table_width 3
	db PIT_RAZOR,   PIT_BUSTER, PIT_FAVOURITE_FIGHT
	db PIT_DUKE,    PIT_SPIKE,  PIT_EVEN_FIGHT
	db PIT_BRUISER, PIT_SCRAPS, PIT_LONG_SHOT_FIGHT
	db PIT_SMOKEY,  PIT_LUCKY,  PIT_FAVOURITE_FIGHT
	db PIT_TANK,    PIT_PEPPER, PIT_EVEN_FIGHT
	db PIT_JACKPOT, PIT_PINCH,  PIT_FAVOURITE_FIGHT
	db PIT_RAZOR,   PIT_SCRAPS, PIT_LONG_SHOT_FIGHT
	db PIT_BUSTER,  PIT_DUKE,   PIT_EVEN_FIGHT
	assert_table_length 8
DEF NUM_PIT_FIGHTS EQU 8 ; a power of two
	assert NUM_PIT_FIGHTS & (NUM_PIT_FIGHTS - 1) == 0

DEF NUM_PIT_STAKES EQU 3

PitStakesString:
	db   "¥1000"
	next "¥5000"
	next "¥10000"
	next "CANCEL@"

PitCancelString:
	db "CANCEL@"

; 3-byte BCD
PitStakes:
	table_width 3
	db $00, $10, $00 ; ¥1000
	db $00, $50, $00 ; ¥5000
	db $01, $00, $00 ; ¥10000
	assert_table_length NUM_PIT_STAKES

; what a winning bet gets back, stake included, for each odds and stake
PitPayouts:
	table_width 3 * NUM_PIT_STAKES
	db $00, $20, $00,  $01, $00, $00,  $02, $00, $00 ; EVENS:  x2
	db $00, $15, $00,  $00, $75, $00,  $01, $50, $00 ; 1 to 2: x1.5
	db $00, $25, $00,  $01, $25, $00,  $02, $50, $00 ; 3 to 2: x2.5
	db $00, $12, $50,  $00, $62, $50,  $01, $25, $00 ; 1 to 4: x1.25
	db $00, $50, $00,  $02, $50, $00,  $05, $00, $00 ; 4 to 1: x5
	assert_table_length NUM_PIT_ODDS
