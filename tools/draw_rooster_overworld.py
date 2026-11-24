#!/usr/bin/env python3
"""Draw the overworld creature sprites and party-menu icons for Rooster Edition.

Usage: tools/draw_rooster_overworld.py [PREVIEW_DIR]

Every sprite is a hand-drawn pixel grid: o black, d dark grey, l light grey,
. white (see-through on sprites). Walking sprites have six 16x16 frames in the
game's order: down, up, side (facing left; the game mirrors it for right), then
the same three again for walking (or flapping/bobbing). Static sprites are a
single 16x16 frame. Party icons are the left half (8x16) of a symmetrical
16x16 picture in two frames; the game mirrors them.

Without arguments it writes gfx/sprites/{monster,bird,fairy,seel,snorlax,
fossil,goose,legend}.png and gfx/icons/{bug,plant,snake,quadruped}.png; run
`make` afterwards. With PREVIEW_DIR it only writes a preview sheet there, in
on-screen shades: sprites show 'l' as white, 'd' as light grey and '.' as
see-through (green on the sheet).
"""

import os
import sys

from PIL import Image, ImageDraw

SHADE = {'o': 0, 'd': 85, 'l': 170, '.': 255}


def legs(body, a, b):
	"""A 14-row body plus two leg rows."""
	return body + [a, b]


# --- shared leg rows -------------------------------------------------------
FRONT_STAND = ['.....o....o.....', '....oo....oo....']
FRONT_WALK = ['.....o....oo....', '....oo..........']
SIDE_STAND = ['......o..o......', '.....oo.oo......']
SIDE_WALK = ['.....o....o.....', '....oo....oo....']

# --- MONSTER: a standard rooster --------------------------------------------
ROOSTER_DOWN = [
	'......o.o.......',
	'.....ododdo.....',
	'.....oddddo..oo.',
	'....ollllllo.odo',
	'....olollolo.odo',
	'....ollddllo.odo',
	'.....oddddo..odo',
	'....oollllooodo.',
	'...olllllllllo..',
	'..ollllllllllo..',
	'..odllllllllldo.',
	'..oddllllllddo..',
	'...oddllllddo...',
	'....oooooooo....',
]
ROOSTER_UP = [
	'......o.o.......',
	'.....ododdo.....',
	'.....oddddo.....',
	'....ollllllo....',
	'....ollllllo....',
	'....ollllllo....',
	'.....ollllo.....',
	'....ooddddoo....',
	'...odddoddddo...',
	'..oddoddodddo...',
	'..ododdoddoddo..',
	'..odddooodddo...',
	'...odllllllo....',
	'....oooooooo....',
]
ROOSTER_SIDE = [
	'....oo.o........',
	'...oddodo.......',
	'...oddddo....oo.',
	'..ollllllo..oddo',
	'..ololllo..oddo.',
	'oodlllllo.oddo..',
	'.oollllo..odo...',
	'..odollo.oddo...',
	'...o.ollloddo...',
	'....olllllldo...',
	'...olllllllldo..',
	'...olldddllldo..',
	'....olllllllo...',
	'.....ooooooo....',
]
ROOSTER = [legs(ROOSTER_DOWN, *FRONT_STAND), legs(ROOSTER_UP, *FRONT_STAND), legs(ROOSTER_SIDE, *SIDE_STAND),
	legs(ROOSTER_DOWN, *FRONT_WALK), legs(ROOSTER_UP, *FRONT_WALK), legs(ROOSTER_SIDE, *SIDE_WALK)]

# --- BIRD: a dark bantam that flaps (frames 4-6 are mid-flap) -----------------
BANTAM_DOWN = [
	'................',
	'.......o.o......',
	'......ododdo....',
	'......oddddo....',
	'.....ollllllo...',
	'.....olollolo...',
	'.....ollddllo...',
	'......odddo.....',
	'.....oddlddo....',
	'....oddllldddo..',
	'....oddlllddddo.',
	'....oddlllddo.o.',
	'.....oddddddo...',
	'......oooooo....',
	'.......o..o.....',
	'......oo..oo....',
]
BANTAM_UP = [
	'................',
	'.......o.o......',
	'......ododdo....',
	'......oddddo....',
	'.....odddddo....',
	'.....odddddo....',
	'......odddo.....',
	'.....oddddddo...',
	'....ododdodddo..',
	'...ododdoddoddo.',
	'...oddodddoddo..',
	'....oddddddddo..',
	'.....oddddddo...',
	'......oooooo....',
	'.......o..o.....',
	'......oo..oo....',
]
BANTAM_SIDE = [
	'................',
	'....o.o.........',
	'...ododdo.......',
	'...oddddo.....o.',
	'..ollllllo...odo',
	'..ololllo...oddo',
	'oodllllo...oddo.',
	'.ooolllo..oddo..',
	'...odlllooddo...',
	'....oddddddddo..',
	'...odddllldddo..',
	'...oddlllldddo..',
	'....oddddddo....',
	'.....oooooo.....',
	'.......o..o.....',
	'......oo.oo.....',
]
BANTAM_FLAP_DOWN = [
	'.......o.o......',
	'......ododdo....',
	'......oddddo....',
	'.....ollllllo...',
	'oo...olollolo..o',
	'odo..ollddllo.od',
	'oddo..odddo..odd',
	'oddddooddddoodd.',
	'.oddddddlldddddo',
	'..oddddlllddddo.',
	'...ooddlllddoo..',
	'.....oddddddo...',
	'......oooooo....',
	'.......o..o.....',
	'................',
	'................',
]
BANTAM_FLAP_UP = [
	'.......o.o......',
	'......ododdo....',
	'......oddddo....',
	'.....odddddo....',
	'oo...odddddo...o',
	'odo...odddo...od',
	'oddo.oddddddoodd',
	'odddoddoddoddod.',
	'.oddddoddoddddo.',
	'..oddddoddddddo.',
	'...ooddddddddo..',
	'.....oddddddo...',
	'......oooooo....',
	'.......o..o.....',
	'................',
	'................',
]
BANTAM_FLAP_SIDE = [
	'.......oo.......',
	'....o.oddo......',
	'...ododdddo.....',
	'...oddddddo...o.',
	'..ollllooddo.odo',
	'..ololllodddoddo',
	'oodllllooddddo..',
	'.ooolllo.ooddo..',
	'...odlllooddo...',
	'....oddddddddo..',
	'...odddllldddo..',
	'....odlllddo....',
	'.....oooooo.....',
	'.......o.o......',
	'................',
	'................',
]
BANTAM = [BANTAM_DOWN, BANTAM_UP, BANTAM_SIDE, BANTAM_FLAP_DOWN, BANTAM_FLAP_UP, BANTAM_FLAP_SIDE]

# --- FAIRY: a Silkie -- a small head with a pom-pom crest, dark face and beak,
# on a fluffy body with a raised tail puff, so it reads as a chicken -----------
SILKIE_DOWN = [
	'......oooo......',
	'.....o.l..o.....',
	'....o..l.l.o....',
	'....o.l....o....',
	'.....oddddo.....',
	'....ododdodo....',
	'.....odlldo.....',
	'......oddo......',
	'...oooo..oooo...',
	'..o..l....l..o..',
	'.o............o.',
	'.o..l......l..o.',
	'..o.l......l.o..',
	'...oolllllloo...',
]
SILKIE_UP = [
	'......oooo......',
	'.....o.l..o.....',
	'....o..l.l.o....',
	'....o.l....o....',
	'.....o..l.o.....',
	'......o..o......',
	'....oo.l..oo....',
	'...o..l..l..o...',
	'..o..l....l..o..',
	'.o....l..l....o.',
	'.o..l......l..o.',
	'..o...l..l...o..',
	'..ol........lo..',
	'...oolllllloo...',
]
SILKIE_SIDE = [
	'...oooo.........',
	'..o.l..o........',
	'.o..l.l.o.......',
	'..odddo.....oo..',
	'..ododo....o..o.',
	'olldddo...o.l..o',
	'..oddo....o....o',
	'...o..oooo..l..o',
	'..o..l.......lo.',
	'.o............o.',
	'.o..l......l..o.',
	'.o...........o..',
	'..o..l...l..o...',
	'...oolllllloo...',
]
def fill_white(frame):
	"""Sprites show index 1 ('l') as white and index 0 ('.') as see-through, so
	fill a white bird's enclosed '.' with 'l' and turn its 'l' fluff into 'd'
	(light grey on screen)."""
	g = [list(r.replace('l', 'd')) for r in frame]
	h, w = len(g), len(g[0])
	seen, stack = set(), [(x, y) for y in range(h) for x in range(w) if x in (0, w - 1) or y in (0, h - 1)]
	while stack:
		x, y = stack.pop()
		if not (0 <= x < w and 0 <= y < h) or (x, y) in seen or g[y][x] != '.':
			continue
		seen.add((x, y))
		stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
	return [''.join('l' if c == '.' and (x, y) not in seen else c for x, c in enumerate(r)) for y, r in enumerate(g)]


SILKIE = [legs(SILKIE_DOWN, *FRONT_STAND), legs(SILKIE_UP, *FRONT_STAND), legs(SILKIE_SIDE, *SIDE_STAND),
	legs(SILKIE_DOWN, *FRONT_WALK), legs(SILKIE_UP, *FRONT_WALK), legs(SILKIE_SIDE, *SIDE_WALK)]
SILKIE = [fill_white(f) for f in SILKIE]

# --- SEEL: a hen floating on the water (also the surfing sprite) -------------
FLOAT_DOWN = [
	'................',
	'................',
	'.......o.o......',
	'......ododdo....',
	'......oddddo....',
	'.....ollllllo...',
	'.....olollolo...',
	'.....ollddllo...',
	'......odddo.....',
	'..l.oolllllloo.l',
	'.l.olllllllllo.l',
	'.l.olllllllllo..',
	'.l..oolllllloo.l',
	'..l...oooooo..l.',
	'...ll........ll.',
	'................',
]
FLOAT_UP = [
	'................',
	'................',
	'.......o.o......',
	'......ododdo....',
	'......oddddo....',
	'.....ollllllo...',
	'.....ollllllo...',
	'.....ollllllo...',
	'......ollllo....',
	'..l.ooddddddoo.l',
	'.l.odddoddoddo.l',
	'.l.oddoddoddo...',
	'.l..ooddddddoo.l',
	'..l...oooooo..l.',
	'...ll........ll.',
	'................',
]
FLOAT_SIDE = [
	'................',
	'................',
	'....o.o.........',
	'...ododdo.......',
	'...oddddo.......',
	'..ollllllo....oo',
	'..ololllo....odo',
	'oodllllo....oddo',
	'.ooolllo...oddo.',
	'...olllloooddo..',
	'..ollllllllldo.l',
	'.l.olllddlllo.l.',
	'l...ooooooooo..l',
	'.l...........ll.',
	'..lll....llll...',
	'................',
]


def bob(frame):
	"""The bobbing frame: the hen sits a pixel lower and the ripples spread."""
	f = ['................'] + frame[:-1]
	return f[:13] + ['.l............l.', 'l.ll........ll.l', '................']


SEEL = [FLOAT_DOWN, FLOAT_UP, FLOAT_SIDE, bob(FLOAT_DOWN), bob(FLOAT_UP), bob(FLOAT_SIDE)]

# --- SNORLAX: SNOROOSTER, a giant Brahma asleep on the path (one frame) -------
SNORLAX = [[
	'...........dddd.',
	'....o.o......d..',
	'...ododdo...d...',
	'...oddddo..dddd.',
	'..ollllllo...oo.',
	'..oddlllllo.oddo',
	'oodlllllllloddo.',
	'.oolllllllllldo.',
	'.olllllllllllldo',
	'olllllllllllllo.',
	'olldddllllddllo.',
	'olldllddlldddlo.',
	'.olllllllllllo..',
	'.odldldooldldo..',
	'..ooooo..ooooo..',
	'................',
]]

# --- FOSSIL: a cracked fossil egg (one frame), drawn from an ellipse ----------


def fossil_egg():
	cx, cy, rx, ry = 7.5, 8.2, 5.2, 6.6
	inside = lambda x, y: ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1
	crack = {(6, 3), (7, 4), (6, 5), (7, 6), (8, 7), (7, 8), (8, 9), (9, 10), (8, 11)}
	rows = []
	for y in range(16):
		row = ''
		for x in range(16):
			if not inside(x, y):
				edge = any(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
				row += 'o' if edge else '.'
			elif (x, y) in crack:
				row += 'o'
			elif x + .5 - cx > rx * .45 or y + .5 - cy > ry * .55 or (x, y) in ((4, 9), (5, 12), (10, 5)):
				row += 'd'
			else:
				row += 'l'
		rows.append(row)
	return rows


FOSSIL = [fossil_egg()]

# --- GOOSE: MEWHONK in Cerulean Cave (one frame, facing down) ---------------
GOOSE = [fill_white([
	'......oooo......',
	'.....o....o.....',
	'.....od..do.....',
	'.....oddddo.....',
	'......oddo......',
	'......o..o......',
	'......o..o......',
	'......oddo......',
	'......o..o......',
	'....oo....oo....',
	'...o........o...',
	'..o..........o..',
	'..o..l....l..o..',
	'..ol........lo..',
	'...oolllllloo...',
	'....oddo.oddo...',
])]

# --- LEGEND: a long-tailed legendary rooster (Articuno, Zapdos, Moltres) -----
LEGEND_DOWN = [
	'.......o.o......',
	'......ododdo....',
	'......oddddo....',
	'.....ollllllo...',
	'.....olollolo...',
	'.....ollddllo...',
	'......odddo.....',
	'.o..oollllloo..o',
	'odo.ollllllllo.d',
	'oddolllllllllodd',
	'.oddllllllllldo.',
	'..oddllllllddo..',
	'...oddllllddo...',
	'....oooooooo....',
	'.....o....o.....',
	'....oo....oo....',
]
LEGEND_UP = [  # from behind: white head and back, wings at the sides, solid black tail
	'.......o.o......',
	'......ododdo....',
	'......oddddo....',
	'.....ollllllo...',
	'.....ollllllo...',
	'......ollllo....',
	'....oolllllloo..',
	'...odlllllllldo.',
	'..oddlllllllddo.',
	'..odddooooooddo.',
	'..oddoooooooodo.',
	'...ooooodooooo..',
	'..ooooodoooooo..',
	'.ooooodoooo.....',
	'.oooodooo.......',
	'..oooo..........',
]
LEGEND_SIDE = [
	'....oo.o........',
	'...oddodo.......',
	'...oddddo.......',
	'..ollllllo......',
	'..ololllo.......',
	'oodlllllo.......',
	'.oollllo........',
	'..odollo........',
	'...o.olllooo....',
	'....olllllddoooo',
	'...olllllllddddo',
	'...olldddlldooo.',
	'....olllllllo.oo',
	'.....ooooooo...o',
	'......o..o......',
	'.....oo.oo......',
]
LEGEND = [LEGEND_DOWN, LEGEND_UP, LEGEND_SIDE, LEGEND_DOWN, LEGEND_UP, LEGEND_SIDE]

# --- party icons: left halves (8x16), two frames each -------------------------
ICONS = {
	'bug': [  # a chick
		['........', '........', '........', '.....ooo', '....olll', '...ollll', '...ololl', '...ollld',
		 '....olld', '..oolllo', '.ollllll', '.ollllll', '.olllll.', '..olllll', '...ooooo', '....o...'],
		['........', '........', '.....ooo', '....olll', '...ollll', '...ololl', '...ollld', '....olld',
		 '..oolllo', '.ollllll', 'olllllll', '.olllll.', '..olllll', '...ooooo', '....o...', '...oo...'],
	],
	'plant': [  # a crested Polish chick
		['....o...', '..o.o.o.', '..ododdo', '.oddoddd', '.odddddd', '..oddooo', '...ollll', '...ololl',
		 '...ollld', '....olld', '..ooolll', '.ollllll', '.ollllll', '..oollll', '....oooo', '....o...'],
		['........', '....o...', '..o.o.o.', '..ododdo', '.oddoddd', '.odddddd', '..oddooo', '...ollll',
		 '...ololl', '...ollld', '..ooolld', '.olllll.', 'olllllll', '.ollllll', '..oooooo', '...oo...'],
	],
	'snake': [  # a naked-neck: long bare neck, ruff at the base
		['......oo', '.....odo', '.....oll', '....olol', '....olld', '.....old', '.....oll', '.....oll',
		 '....oddd', '...odddo', '..odllll', '.olllll.', '.olllll.', '..oolllo', '....oooo', '....o...'],
		['........', '......oo', '.....odo', '.....oll', '....olol', '....olld', '.....old', '.....oll',
		 '....oddd', '...odddo', '..odllll', '.olllll.', 'olllllll', '.ooollll', '....oooo', '...oo...'],
	],
	'quadruped': [  # a tall game bird: upright, long legs
		['......oo', '.....odd', '.....oll', '....olol', '....olld', '.....oll', '....olll', '...ollll',
		 '..olllll', '..oddlll', '..oddlll', '...oolll', '.....ooo', '.....o..', '.....o..', '....oo..'],
		['......oo', '.....odd', '.....oll', '....olol', '....olld', '.....oll', '....olll', '...ollll',
		 '..olllll', '..oddlll', '..oddlll', '...oolll', '.....ooo', '.....o..', '....o...', '...oo...'],
	],
}

def close_icon(half):
	"""Fill any see-through hole inside a mirrored icon with white."""
	full = [r + r[::-1] for r in half]
	h, w = len(full), 16
	seen, stack = set(), [(x, y) for y in range(h) for x in range(w) if x in (0, w - 1) or y in (0, h - 1)]
	while stack:
		x, y = stack.pop()
		if not (0 <= x < w and 0 <= y < h) or (x, y) in seen or full[y][x] != '.':
			continue
		seen.add((x, y))
		stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
	return [''.join('l' if c == '.' and (x, y) not in seen else c for x, c in enumerate(r[:8])) for y, r in enumerate(full)]


ICONS = {k: [close_icon(f) for f in v] for k, v in ICONS.items()}

SPRITES = {
	# name: (frames, file in gfx/sprites, what it stands for)
	'monster': (ROOSTER, 'monster.png', 'standard rooster'),
	'bird': (BANTAM, 'bird.png', 'flapping bantam'),
	'fairy': (SILKIE, 'fairy.png', 'fluffy Silkie'),
	'seel': (SEEL, 'seel.png', 'floating hen (surfing)'),
	'snorlax': (SNORLAX, 'snorlax.png', 'SNOROOSTER asleep'),
	'fossil': (FOSSIL, 'fossil.png', 'fossil egg'),
	'goose': (GOOSE, 'goose.png', 'MEWHONK (new)'),
	'legend': (LEGEND, 'legend.png', 'legendary long-tail (new)'),
}


def check(name, frame, w=16, h=16):
	assert len(frame) == h, (name, len(frame))
	for r, row in enumerate(frame):
		assert len(row) == w and set(row) <= set(SHADE), (name, r, row)


def frames_image(frames):
	img = Image.new('L', (16, 16 * len(frames)), 255)
	for i, f in enumerate(frames):
		for y, row in enumerate(f):
			for x, ch in enumerate(row):
				img.putpixel((x, i * 16 + y), SHADE[ch])
	return img


def icon_image(frames):
	img = Image.new('L', (8, 32), 255)
	for i, f in enumerate(frames):
		for y, row in enumerate(f):
			for x, ch in enumerate(row):
				img.putpixel((x, i * 16 + y), SHADE[ch])
	return img


def validate():
	for name, (frames, _, _) in SPRITES.items():
		for i, f in enumerate(frames):
			check(f'{name}[{i}]', f)
	for name, frames in ICONS.items():
		for i, f in enumerate(frames):
			check(f'icon {name}[{i}]', f, 8)


def preview(out_dir):
	"""A sheet of every sprite frame (and the right-facing mirror), plus the icons."""
	os.makedirs(out_dir, exist_ok=True)
	S, PAD = 5, 6
	rows = []
	for name, (frames, _, label) in SPRITES.items():
		cells = [frames_image([f]) for f in frames]
		if len(frames) == 6:
			cells.insert(3, frames_image([frames[2]]).transpose(Image.FLIP_LEFT_RIGHT))
			cells.append(frames_image([frames[5]]).transpose(Image.FLIP_LEFT_RIGHT))
		rows.append((label, cells))
	icon_cells = []
	for name, frames in ICONS.items():
		for f in frames:
			half = icon_image([f]).crop((0, 0, 8, 16))
			full = Image.new('L', (16, 16), 255)
			full.paste(half, (0, 0))
			full.paste(half.transpose(Image.FLIP_LEFT_RIGHT), (8, 0))
			icon_cells.append(full)
	rows.append(('party icons: chick, crested, naked-neck, tall game (2 frames each)', icon_cells))
	label_w = 150
	cell = 16 * S + PAD
	w = label_w + cell * max(len(c) for _, c in rows)
	h = len(rows) * (cell + PAD) + PAD
	sheet = Image.new('RGB', (w, h), (232, 240, 228))
	lut = {0: (16, 16, 16), 85: (168, 168, 168), 170: (255, 255, 255), 255: (150, 200, 120)}
	d = ImageDraw.Draw(sheet)
	for r, (label, cells) in enumerate(rows):
		y = PAD + r * (cell + PAD)
		d.text((6, y + cell // 2 - 6), label, fill=(0, 0, 0))
		for c, im in enumerate(cells):
			big = im.resize((16 * S, 16 * S), Image.NEAREST).convert('RGB')
			big.putdata([lut[p[0]] for p in big.getdata()])
			sheet.paste(big, (label_w + c * cell, y))
	sheet.save(os.path.join(out_dir, 'overworld_sheet.png'))
	print('wrote', os.path.join(out_dir, 'overworld_sheet.png'))


def install():
	for name, (frames, fname, _) in SPRITES.items():
		path = os.path.join('gfx/sprites', fname)
		frames_image(frames).save(path)
		print('wrote', path)
	for name, frames in ICONS.items():
		path = os.path.join('gfx/icons', name + '.png')
		icon_image(frames).save(path)
		print('wrote', path)


def main():
	validate()
	if len(sys.argv) > 1:
		preview(sys.argv[1])
	else:
		install()


if __name__ == '__main__':
	main()
