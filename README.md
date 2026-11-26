# Pokémon Red and Blue: Rooster Edition

A hack of the [pret disassembly][pret] of Pokémon Red and Blue in which every Pokémon is a chicken breed, called a COCK. Types and evolutions are unchanged: BULBACLUCK is a Serama chick and CHICKANDER a Rhode Island Red. The edition lines read "Rhode Island Red" and "Blue Wyandotte". The ROM runs in colour on a Game Boy Color, and still runs on the original Game Boy and Super Game Boy.

The full list of breeds, and notes on the art, maps and tools, are in [**CLAUDE.md**](CLAUDE.md).


## New areas

Four new areas follow a fighting bird's life, from the wild to the ring to retirement.

### Junglefowl Island

When you leave the S.S. Anne, a wave sweeps you off the Vermilion gangway and onto an island that isn't on any map. A castaway asks you to leave the wild red junglefowl alone, but you can catch them anyway, and they're strong. At the Roost, the flock's leader is a one-time level-30 DRAGONCOMB. Find three raft parts to sail home to Vermilion; you can't come back.

### The Pit (Celadon)

Behind the Game Corner, a back room takes bets on illegal bird fights: ¥1000, ¥5000 or ¥10000 a time, and the house always wins in the end. Pull the slots often enough and the bookie's runner invites you in. Downstairs you can fight three undercard birds for prize money, then the bookie offers you ¥50000 to lose to OLD IRON. Once Giovanni breaks up TEAM ROOST, the Pit reopens under a COCK RING banner.

### Fuji Farm (east of Lavender)

After you rescue MR. FUJI, walk east out of Lavender to his farm, where birds go when nobody wants them. You can retire party birds there for good. Every five different breeds earns a gift, and the barn fills with your retired birds. The ledger on the barn wall lists every breed you've retired. OLD IRON ends up here too, and the story he tells depends on what you did in the Pit.

### Breeding Lab (Route 20)

A private island at the west end of Route 20, near Cinnabar, reached by SURF. Inside, a scientist bred birds to order for whoever paid, and his diaries are signed "F." The pens hold the failed experiments and, in a glass case at the back, the original MEWPEEP: a one-time level-50 battle and the only way to get one.


## Building

This hack no longer matches the original ROMs' checksums. The upstream pret disassembly builds the following ROMs:

- Pokemon Red (UE) [S][!].gb `sha1: ea9bcae617fdf159b045185467ae58b2e4a48b9a`
- Pokemon Blue (UE) [S][!].gb `sha1: d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`
- BLUEMONS.GB (debug build) `sha1: 5b1456177671b79b263c614ea0e7cc9ac542e9c4`
- dmgapae0.e69.patch `sha1: 0fb5f743696adfe1dbb2e062111f08f9bc5a293a`
- dmgapee0.e68.patch `sha1: ed4be94dc29c64271942c87f2157bca9ca1019c7`

To set up the repository, see [**INSTALL.md**](INSTALL.md).


## See also

- [**Wiki**][wiki] (includes [tutorials][tutorials])
- [**Symbols**][symbols]
- [**Tools**][tools]

You can find the pret team on [Discord (pret, #pokered)](https://discord.gg/d5dubZ3).

For other pret projects, see [pret.github.io](https://pret.github.io/).

[wiki]: https://github.com/pret/pokered/wiki
[tutorials]: https://github.com/pret/pokered/wiki/Tutorials
[symbols]: https://github.com/pret/pokered/tree/symbols
[tools]: https://github.com/pret/gb-asm-tools
[ci]: https://github.com/pret/pokered/actions
[ci-badge]: https://github.com/pret/pokered/actions/workflows/main.yml/badge.svg
[pret]: https://github.com/pret/pokered
