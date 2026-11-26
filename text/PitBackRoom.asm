_GameCornerRunnerInviteText::
	text "Psst. Kid."

	para "You like a"
	line "gamble. I can"
	cont "tell."

	para "Slots are for"
	line "suckers. There's"
	cont "a better game."

	para "Last building on"
	line "this row. Knock"
	cont "twice."
	done

_GameCornerRunnerNextDoorText::
	text "Last building on"
	line "this row, kid."
	cont "Knock twice."
	done

_PitBackRoomDoormanMembersOnlyText::
	text "Members only."

	para "Beat it, kid."
	done

_PitBackRoomDoormanKnockTwiceText::
	text "..."

	para "Knocked twice,"
	line "huh? Fine."

	para "Bets go through"
	line "the window. And"
	cont "no trouble."
	done

_PitBackRoomDoormanNoTroubleText::
	text "No trouble in"
	line "here, kid."
	done

_PitBackRoomStairsGuardText::
	text "Downstairs is for"
	line "fighters."

	para "Not today, kid."
	done

_PitBackRoomLoserText::
	text "Lost the rent on"
	line "a sure thing."

	para "Sure things lose"
	line "here a lot."
	done

_PitBackRoomRegularText::
	text "The house sets"
	line "the odds, kid."

	para "The house never"
	line "goes home broke."
	done

_PitBackRoomBoardFavText::
	text "TONIGHT'S FIGHT:"
	line "@"
	text_ram wStringBuffer
	text "  @"
	text_ram wNameBuffer
	text_start
	prompt

_PitBackRoomBoardOutText::
	text "vs."
	line "@"
	text_ram wStringBuffer
	text "  @"
	text_ram wNameBuffer
	text_start
	done

_PitBackRoomClerkFavText::
	text "Tonight it's"
	line "@"
	text_ram wStringBuffer
	text ", a"
	cont "@"
	text_ram wNameBuffer
	text "..."
	prompt

_PitBackRoomClerkOutText::
	text "...against"
	line "@"
	text_ram wStringBuffer
	text ", a"
	cont "@"
	text_ram wNameBuffer
	text "!"
	prompt

_PitBackRoomClerkWhoText::
	text "Who's your money"
	line "on?"
	done

_PitBackRoomClerkHowMuchText::
	text "How much?"
	done

_PitBackRoomClerkCantAffordText::
	text "You ain't got it,"
	line "kid."
	done

_PitBackRoomClerkSuitYourselfText::
	text "Suit yourself."
	done

_PitBackRoomClerkYoureOnText::
	text "You're on."

	para "Shouts come up"
	line "the stairs..."
	prompt

_PitGoesForTheEyesText::
	text_ram wStringBuffer
	text " goes"
	line "for the eyes!"
	prompt

_PitSpursText::
	text_ram wStringBuffer
	text " slashes"
	line "with its spurs!"
	prompt

_PitDownAndUpText::
	text_ram wNameBuffer
	text " is down!"
	line "...no, it's up!"
	prompt

_PitDrivesBackText::
	text_ram wStringBuffer
	text " drives"
	line "@"
	text_ram wNameBuffer
	text " back!"
	prompt

_PitCrowdRoarsText::
	text "The crowd roars!"
	prompt

_PitBothDownText::
	text "Both birds go"
	line "down together!"

	para "Neither one gets"
	line "up."
	prompt

_PitFinishText::
	text_ram wStringBuffer
	text " lands"
	line "the last blow!"

	para "@"
	text_ram wNameBuffer
	text " is done."

	para "@"
	text_ram wStringBuffer
	text " wins!"
	prompt

_PitBackRoomClerkWonText::
	text "Nice call, kid."
	line "That's ¥@"
	text_bcd hMoney, 3 | LEADING_ZEROES | LEFT_ALIGN
	text "."
	done

_PitBackRoomClerkLostText::
	text "Tough luck, kid."
	done

_PitBackRoomClerkNoContestText::
	text "No contest. The"
	line "house keeps the"
	cont "bets."
	done
