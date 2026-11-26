_FujiFarmSignText::
	text "FUJI FARM"
	line "A home for COCK"
	cont "nobody wants."
	done

_FujiFarmFarmhandShutText::
	text "Farm's shut while"
	line "MR.FUJI's away."

	para "He went up COCK"
	line "TOWER and hasn't"
	cont "come back down."
	done

_FujiFarmFarmhandOpenText::
	text "MR.FUJI's back!"
	line "Farm's open."

	para "Birds that can't"
	line "fight come here."

	para "Beats where they"
	line "end up otherwise."
	done

_FujiFarmFarmhandEmptyPenText::
	text "See that empty"
	line "pen? A big one's"
	cont "coming from"
	cont "CELADON, they say."
	done

_FujiFarmNewcomerText::
	text_ram wFarmNewcomerName
	text " is"
	line "settling in."

	para "It looks happier"
	line "already."
	done

_FujiFarmOldIronUnbeatenText::
	text "It's OLD IRON!"
	line "One wing hangs"
	cont "crooked."

	para "He won six more"
	line "after you. Then a"
	cont "kid's bird broke"
	cont "his wing."

	para "They dumped him"
	line "here that night."
	done

_FujiFarmOldIronBeatenText::
	text "It's OLD IRON!"
	line "He's gone grey"
	cont "round the comb."

	para "Lost one fight in"
	line "his life. They"
	cont "dumped him here"
	cont "that same night."

	para "He looks at you."
	line "He remembers."
	done

_FujiFarmScrapsText::
	text "A tag on its leg"
	line "says SCRAPS."

	para "0 WINS"
	line "9 LOSSES"

	para "Nobody ever bet"
	line "on it. It doesn't"
	cont "seem to mind."
	done

_FujiFarmRazorText::
	text "A tag on its leg"
	line "says RAZOR."

	para "It lost an eye in"
	line "the PIT. It still"
	cont "struts like it"
	cont "won."
	done

_FujiFarmPondHenText::
	text "A hen is floating"
	line "on the pond."

	para "Nobody told her"
	line "hens can't swim."
	done

_FujiFarmSilkieText::
	text "A blind SILKYPUFF"
	line "sits in the"
	cont "flowers."

	para "It was a show"
	line "bird, until it"
	cont "couldn't see the"
	cont "judges."
	done

_FujiFarmOldHenText::
	text "An old hen. She"
	line "stopped laying"
	cont "last spring."

	para "Most farms would"
	line "have eaten her."
	done

_FujiFarmFlockNameText::
	text "A retired"
	line "@"
	text_ram wNameBuffer
	text "."

	para "@"
	text_end

_FujiFarmFlockDustBathText::
	text "It's having a"
	line "dust bath."
	done

_FujiFarmFlockGritText::
	text "It's pecking at"
	line "grit."
	done

_FujiFarmFlockDozingText::
	text "It's dozing in"
	line "the sun."
	done

_FujiFarmFlockBugsText::
	text "It's scratching"
	line "for bugs."
	done

_FujiFarmFlockIgnoresYouText::
	text "It ignores you"
	line "completely."
	done

_FujiFarmFlockPreeningText::
	text "It's preening a"
	line "scruffy wing."
	done

_FujiFarmFlockCornText::
	text "It eyes you, then"
	line "goes back to its"
	cont "corn."
	done

_FujiFarmFlockStrawText::
	text "It's settled into"
	line "the straw."
	done

_FujiFarmFlockOneLegText::
	text "It's asleep on"
	line "one leg."
	done

_FujiFarmFlockNeverAgainText::
	text "It won't fight"
	line "again. Ever."
	done

_FujiFarmFlockBestSpotText::
	text "It's got the best"
	line "spot in the barn."
	done

_FujiFarmBarnPrimefowlText::
	text "A PRIMEFOWL on a"
	line "nest of straw."

	para "A man in a karate"
	line "suit dropped it"
	cont "off. Said it was"
	cont "finished."
	done

_FujiFarmBarnPhotoText::
	text "An old photo is"
	line "pinned up. A"
	cont "young man in a"
	cont "lab coat holds a"
	cont "goose."

	para "On the back:"
	line "F. CINNABAR LAB"
	done

_FujiFarmBarnLedgerBlankText::
	text "The LEDGER of"
	line "retired breeds."

	para "It's blank."
	done

_FujiFarmBarnLedgerCountText::
	text "The LEDGER of"
	line "retired breeds."

	para "Breeds: @"
	text_decimal wNumSetBits, 1, 3
	text ""
	prompt

_FujiFarmBarnLedgerNextGiftText::
	text "Next gift at @"
	text_decimal wNameBuffer, 1, 3
	text "."
	prompt

_FujiFarmBarnLedgerReadItText::
	text "Read through it?"
	done

_FujiFarmHouseFarmerIntroText::
	text "MR.FUJI's farm."
	line "I run it for him."

	para "Birds come here"
	line "when they're too"
	cont "old, too slow, or"
	cont "lost too often."

	para "Nobody else wants"
	line "them."
	prompt

_FujiFarmHouseFarmerRetireOfferText::
	text "Have you a bird"
	line "to retire? It'd"
	cont "stay here for"
	cont "good."
	done

_FujiFarmHouseFarmerComeBackText::
	text "Come back soon."
	done

_FujiFarmHouseFarmerLastBirdText::
	text "That's your only"
	line "bird! Keep it."
	done

_FujiFarmHouseFarmerWhichBirdText::
	text "Which bird?"
	done

_FujiFarmHouseFarmerChangedMindText::
	text "Changed your mind?"
	line "That's fine."
	done

_FujiFarmHouseFarmerKnowsHMText::
	text "It still knows an"
	line "HM. It's got work"
	cont "to do yet."
	done

_FujiFarmHouseFarmerSureText::
	text "Retire @"
	text_ram wNameBuffer
	text "?"
	line "It'll never fight"
	cont "again."
	done

_FujiFarmHouseFarmerWanderedOffText::
	text_ram wFarmNewcomerName
	text_start
	line "wandered off to"
	cont "the yard."
	prompt

_FujiFarmHouseFarmerNewBreedText::
	text "That's a new breed"
	line "for the LEDGER!"
	prompt

_FujiFarmHouseFarmerAtTheGateText::
	text "It'll wait by the"
	line "gate for a while."
	done

_FujiFarmHouseFarmerGiftText::
	text "That's another 5"
	line "breeds retired!"

	para "MR.FUJI left this"
	line "for you."
	prompt

_FujiFarmHouseFarmerReceivedText::
	text "<PLAYER> received"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_FujiFarmHouseFarmerBagFullText::
	text "Your bag's full."
	line "Come back for it."
	done

_FujiFarmHouseNestText::
	text "A big nest of"
	line "straw. Your birds"
	cont "pile in for a"
	cont "rest."
	prompt

_FujiFarmHouseNestBetterText::
	text "They look much"
	line "better!"
	done
