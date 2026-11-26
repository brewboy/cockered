# Pokémon Red and Blue: Rooster Edition

A hack of the [pret disassembly][pret] of Pokémon Red and Blue in which every Pokémon is a chicken breed, called a COCK. Types and evolutions are unchanged: BULBACLUCK is a Serama chick and CHICKANDER a Rhode Island Red. The edition lines read "Rhode Island Red" and "Blue Wyandotte". The ROM runs in colour on a Game Boy Color, and still runs on the original Game Boy and Super Game Boy.

The full list of breeds, and notes on the art, maps and tools, are in [**CLAUDE.md**](CLAUDE.md).


## New areas

Four new places, for a fighting bird's life from the wild to the ring and beyond. Finding them is up to you.

- **Junglefowl Island:** somewhere no map shows, where the birds are still wild.
- **The Pit:** where the real money changes hands, if you know who to ask.
- **Fuji Farm:** where birds go when nobody wants them any more.
- **Breeding Lab:** where somebody tried to build a better bird.


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
