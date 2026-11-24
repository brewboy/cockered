#!/usr/bin/env python3
"""Patch trainer battle pictures for Rooster Edition.

Usage: tools/draw_rooster_trainers.py [PREVIEW_DIR]

Each patch is a small pixel grid pasted at a fixed spot in a picture in
gfx/trainers/: o black, d dark grey, l light grey, . white, and a space keeps
the original pixel. Patches overwrite the same pixels every time, so running
the script again changes nothing. Run `make` afterwards.

- juggler.png (EGG JUGGLER): the four Poke Balls in the air become eggs.
- birdkeeper.png (FLOCK KEEPER): the bird on his hand becomes a hen, and its
  long tail is cleared.
- burglar.png (EGG THIEF): an egg peeks out of the top of his sack, another
  tumbles out behind him and a third lies splatted on the ground.

With PREVIEW_DIR it writes before/after previews there instead.
"""

import os
import sys

from PIL import Image

SHADE = {'o': 0, 'd': 85, 'l': 170, '.': 255}

EGG = [
	'..ooo..',
	'.o..lo.',
	'o....lo',
	'o...llo',
	'o..llld',
	'.olllo.',
	'..ooo..',
]
EGG_TILTED = [
	'...ooo.',
	'..o..lo',
	'.o...lo',
	'o...llo',
	'o..lldo',
	'ollldo.',
	'.ooo...',
]

# the hen, x 5-19 and y 1-18, toes resting on his fingers (row 19)
HEN = [
	'.....o.o.......',
	'....ododo......',
	'....odddo...o..',
	'...ollllo..odo.',
	'..oloolllo.oddo',
	'oodllllllooddo.',
	'.oodlllllodddo.',
	'...oddllllloddo',
	'...o.ollllllldo',
	'.....olllllllo.',
	'....ollllddddlo',
	'....olllddllddo',
	'....ollldlldddo',
	'....olllldddllo',
	'   ..olllllllo.',
	'   ...ooooooo..',
	'   ....o..o....',
	'   ...oo.oo....',
]

SACK_EGG = [
	'..oo..',
	'.o..o.',
	'o...lo',
	'o..llo',
	'o..llo',
	'olllo ',
]

# an egg tumbling out of the sack, with motion lines, and one splatted behind him
FALLING_EGG = [
	'.o.o...',
	'..o.o..',
	'.......',
	'..ooo..',
	'.o..lo.',
	'o...llo',
	'o..llld',
	'o.lllo.',
	'.ooo...',
]
SPLAT = [  # a broken half shell beside a puddle of white with the yolk
	'o.o.o......',
	'o...o......',
	'o..lo..o...',
	'.ooo.oo.oo.',
	'...oo....o.',
	'..o..ddd..o',
	'..o.ddddd.o',
	'...ooooooo.',
]

PATCHES = {
	'juggler': [(13, 1, EGG), (40, 0, EGG_TILTED), (6, 7, EGG_TILTED), (2, 17, EGG)],
	'birdkeeper': [(5, 1, HEN)],
	'burglar': [(42, 19, SACK_EGG), (49, 36, FALLING_EGG), (45, 47, SPLAT)],
}

# the old Poke Balls, cleared to white before the eggs go in (x0, y0, x1, y1)
CLEAR = {
	'juggler': [(13, 1, 19, 7), (40, 0, 47, 6), (6, 7, 12, 13), (2, 17, 8, 23)],
	'birdkeeper': [(0, 13, 9, 20), (5, 0, 19, 18)],  # the old bird and its tail
	'burglar': [],
}


def patch(img, name):
	img = img.convert('L')
	for x0, y0, x1, y1 in CLEAR[name]:
		for y in range(y0, y1 + 1):
			for x in range(x0, x1 + 1):
				img.putpixel((x, y), 255)
	for x0, y0, grid in PATCHES[name]:
		for y, row in enumerate(grid):
			for x, ch in enumerate(row):
				if ch != ' ':
					img.putpixel((x0 + x, y0 + y), SHADE[ch])
	return img


def main():
	out = sys.argv[1] if len(sys.argv) > 1 else None
	for name in PATCHES:
		path = f'gfx/trainers/{name}.png'
		before = Image.open(path).convert('L')
		after = patch(before, name)
		if out:
			os.makedirs(out, exist_ok=True)
			pair = Image.new('L', (before.width * 2 + 8, before.height), 200)
			pair.paste(before, (0, 0))
			pair.paste(after, (before.width + 8, 0))
			pair.resize((pair.width * 5, pair.height * 5), Image.NEAREST).save(os.path.join(out, name + '.png'))
			print('wrote', os.path.join(out, name + '.png'))
		else:
			after.save(path)
			print('wrote', path)


if __name__ == '__main__':
	main()
