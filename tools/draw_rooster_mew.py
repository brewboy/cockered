#!/usr/bin/env python3
"""Draw the Mew chick front sprite (#151) for Rooster Edition.

Usage: tools/draw_rooster_mew.py [SRC_DIR]

The tiny pink Serama chick floats like Mew: its body is lifted off the ground
with its toes tucked up, two little wings flare out, and a long thin tail curls
up behind it, ending in a round tuft, with a few sparkles around it. Writes 151_tiny_pink_serama_chick.png
into SRC_DIR's gameboy/ (56x56, four shades), colour/ (56x56 RGBA) and
colour_x4/ (224x224 RGBA) folders. SRC_DIR defaults to gfx/rooster_src.
"""

import math
import os
import sys

from PIL import Image

W = H = 56
NAME = '151_tiny_pink_serama_chick.png'
OUTL = (26, 22, 30)
PALETTE = {
	'o': OUTL,
	'#': (244, 186, 198),  # body
	's': (208, 157, 176),  # soft shade
	'd': (165, 122, 150),  # shade
	'D': (141, 103, 133),  # deep shade
	'l': (248, 214, 221),  # highlight
	'b': (238, 190, 70),   # beak / toes
	'B': (161, 125, 53),   # beak shade
	'e': (20, 20, 24),     # eye
}

# The hand-drawn chick, without its legs and feet, facing left.
BODY = [
	'........oooo...............',
	'......oollldo..............',
	'.....oll####do.............',
	'....ol#######do............',
	'...ol########ddo...........',
	'...o###e#####ddo...........',
	'..oob##e#####ddo...........',
	'.oBbb########ddoo..........',
	'..oob#######dddldooo....o..',
	'....oddd##ddddd##lddo..odo.',
	'....oddddddddd#####ddoolo..',
	'.....oodddddd######dddl#o..',
	'.......o########ss##dd##o..',
	'......ol######sssssDdd#do..',
	'......o######sssssssDddo...',
	'......od#####sssssssDddo...',
	'......odd####DDsssDDDdo....',
	'.......odd####DDDDDDddo....',
	'.......odddddddddddddo.....',
	'........odddddddddddo......',
	'.........ooddddddddo.......',
	'...........oddddddoo.......',
	'............oooooo.........',
]
BX, BY = 12, 20  # where the body's grid sits: lifted well off the ground


def gb(c):
	"""Game Boy shade, as for the rest of the colour set."""
	if c == OUTL:
		return 0
	y = .299 * c[0] + .587 * c[1] + .114 * c[2]
	return 85 if y < 90 else 170 if y < 185 else 255


class Sprite:
	def __init__(self):
		self.col = {}

	def stroke(self, pts, w0, w1, colour, steps=80):
		"""Pixels of a tapering cubic Bezier stroke, painted only where empty."""
		(ax, ay), (bx, by), (cx, cy), (dx, dy) = pts
		cells = {}
		for i in range(steps + 1):
			t = i / steps
			u = 1 - t
			x = u ** 3 * ax + 3 * u * u * t * bx + 3 * u * t * t * cx + t ** 3 * dx
			y = u ** 3 * ay + 3 * u * u * t * by + 3 * u * t * t * cy + t ** 3 * dy
			r = (w0 + (w1 - w0) * t) / 2
			for py in range(int(y - r - 1), int(y + r + 2)):
				for px in range(int(x - r - 1), int(x + r + 2)):
					if (px + .5 - x) ** 2 + (py + .5 - y) ** 2 <= r * r:
						cells[(px, py)] = colour(t, px, py) if callable(colour) else colour
		return cells

	def blob(self, cx, cy, r, colour):
		return {(x, y): colour(x, y) for y in range(int(cy - r - 1), int(cy + r + 2))
			for x in range(int(cx - r - 1), int(cx + r + 2)) if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r}

	def paint(self, cells, over=False):
		"""Add a part with its own outline; behind what is there unless `over`."""
		cells = {p: c for p, c in cells.items() if 0 <= p[0] < W and 0 <= p[1] < H}
		ring = {(x + dx, y + dy) for x, y in cells for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))} - set(cells)
		for p in ring:
			if 0 <= p[0] < W and 0 <= p[1] < H and (over or p not in self.col):
				self.col[p] = OUTL
		for p, c in cells.items():
			if over or p not in self.col:
				self.col[p] = c


def draw():
	s = Sprite()
	pink, soft, shade, deep, hi = (PALETTE[k] for k in '#sdDl')
	# the body first: everything else tucks in behind it, except the near wing
	for j, row in enumerate(BODY):
		for i, ch in enumerate(row):
			if ch != '.':
				s.col[(BX + i, BY + j)] = PALETTE[ch]

	# the near wing, flared up and back with three rounded feather tips
	wing = {}
	for k, (tx, ty) in enumerate(((39, 21), (41.5, 24), (42, 27.5))):
		tip = s.stroke(((33, 31), (35, 29), (tx - 2, ty + 1.5), (tx, ty)), 3.6, 2.4,
			lambda t, x, y, k=k: hi if t > .78 and k == 0 else pink if t > .55 else soft)
		wing.update({p: c for p, c in tip.items() if p not in wing})
	s.paint(wing, over=True)
	# feather creases between the tips
	for x, y in ((38, 24), (39, 26)):
		if s.col.get((x, y)) not in (None, OUTL):
			s.col[(x, y)] = shade

	# the far wing peeks over the back, smaller and in shadow
	far = {}
	for tx, ty in ((32, 17), (35, 19)):
		far.update(s.stroke(((30, 27), (30, 23), (tx - 1, ty + 2), (tx, ty)), 3.4, 2.2,
			lambda t, x, y: soft if t > .6 else shade))
	s.paint(far)

	# Mew's tail: long and thin, curling up from the rump to a round tuft
	tail = s.stroke(((34, 34), (50, 36), (53, 20), (47, 11)), 2.2, 2, lambda t, x, y: soft if t < .25 else pink)
	tail.update(s.blob(46.5, 9, 2.8, lambda x, y: hi if x + y < 54 else pink if x + y < 57 else soft))
	s.paint(tail)

	# toes tucked up under the body, dangling a little
	toes = {(25, 43): PALETTE['b'], (26, 43): PALETTE['B'], (29, 43): PALETTE['b'], (30, 43): PALETTE['B']}
	s.paint(toes)

	# a few sparkles twinkling around it: soft pink arms round a bright heart,
	# so they show on the Game Boy too
	for cx, cy, big in ((12, 14, True), (22, 8, False), (6, 34, False), (40, 48, True), (54, 40, False)):
		sparkle = {(cx, cy): hi}
		for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
			sparkle[(cx + dx, cy + dy)] = soft
			if big:
				sparkle[(cx + 2 * dx, cy + 2 * dy)] = soft
		for p, c in sparkle.items():
			if p not in s.col:
				s.col[p] = c
	return s


def main():
	src = sys.argv[1] if len(sys.argv) > 1 else 'gfx/rooster_src'
	s = draw()
	colour = Image.new('RGBA', (W, H), (0, 0, 0, 0))
	grey = Image.new('L', (W, H), 255)
	for (x, y), c in s.col.items():
		colour.putpixel((x, y), c + (255,))
		grey.putpixel((x, y), gb(c))
	for sub, img in (('gameboy', grey), ('colour', colour), ('colour_x4', colour.resize((W * 4, H * 4), Image.NEAREST))):
		os.makedirs(os.path.join(src, sub), exist_ok=True)
		img.save(os.path.join(src, sub, NAME))
	print(f'wrote {NAME}')


if __name__ == '__main__':
	main()
