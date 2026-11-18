#!/usr/bin/env python3
"""Draw the opening cock fight for Rooster Edition.

Usage: tools/draw_rooster_intro.py [OUT_DIR]

The intro's fight is redrawn with roosters: CROWGAR (a Black Sumatra rooster,
seen from behind, big on the left) squares up to NIDOROOST (Red) or SILKYPUFF
(Blue), who faces it from the right.

CROWGAR has three 56x56 poses: standing, wings flared, lunging to peck.
The opponent has three 48x48 frames made from its front sprite: standing,
crouched to spring, and leaping with wings up and feet thrust forward.

With no OUT_DIR it installs the intro: gfx/intro/gengar.png (CROWGAR's unique
tiles, 8 to a row), gengar_1-3.tilemap, red_nidorino_1-3.png and
blue_jigglypuff_1-3.png (file names kept from the original), plus colour
references in gfx/rooster_src/intro/. Run `make` afterwards. With OUT_DIR it
writes a preview there instead: four-shade PNGs and _colour.png versions.
"""

import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_rooster_backs as rb  # noqa: E402

OUTL = rb.OUTL
SRC = 'gfx/rooster_src/colour'

# Black Sumatra: near-black with a green sheen; the sheen and the comb are pale
# enough to show as the light grey on a Game Boy.
BODY = (30, 32, 42)
HACKLE = (26, 28, 38)
WING = (22, 23, 33)
TAIL = (24, 48, 44)
SHEEN = (72, 120, 112)
HACKLE_HI = (96, 102, 124)
COMB = (205, 60, 85)
COMB_SHADE = (150, 40, 62)
BEAK = (160, 140, 100)


def fronds(c, feathers, w0=9, w1=2):
	"""The tail: a clump of broad, leafy sickle feathers with a sheen down each spine."""
	for k, pts in enumerate(feathers):
		c.stroke(f'tail{k}', pts, w0, w1, TAIL, hi=SHEEN)


def fan(c, name, root, tips, w0=9, w1=4):
	for k, tip in enumerate(tips):
		mid = ((root[0] + tip[0]) / 2 - 2, (root[1] + tip[1]) / 2)
		c.stroke(f'{name}{k}', (root, mid, tip), w0, w1, WING, hi=SHEEN)


def head(c, hx, hy):
	"""The head in profile, looking right at the foe: pea comb, red face, eye, beak, wattle."""
	c.ellipse('wattle', hx + 5, hy + 6.5, 2.2, 3, COMB, rim=False)
	c.stroke('beak', ((hx + 5, hy), (hx + 8, hy + 1), (hx + 11, hy + 2)), 3.6, 1.6, BEAK)
	c.ellipse('head', hx, hy, 7, 6.2, BODY, hi=False)
	c.ellipse('face', hx + 4, hy + 1, 3, 3, COMB_SHADE, rim=False, hi=False)
	c.ellipse('comb', hx, hy - 6, 4.2, 2.4, COMB, rim=False)
	for x, y in ((hx + 4, hy - 1), (hx + 5, hy - 1)):
		c.set(int(x), int(y), 'eye', (12, 12, 16))


def crowgar(pose):
	rb.N = 56
	c = rb.Canvas()
	if pose == 0:  # standing tall, side-on to the foe
		fronds(c, [((15, 42), (2, 36), (-3, 32)), ((16, 39), (2, 26), (-1, 16)), ((17, 37), (8, 18), (6, 4)),
			((19, 36), (16, 18), (17, 6))])
		c.ellipse('body', 28, 48, 24, 15, BODY, hi=False)
		c.ellipse('wing', 24, 46, 13, 7, WING, hi=False)
		c.stroke('quill0', ((13, 46), (23, 44), (35, 47)), 1.4, 1, SHEEN)
		c.stroke('neck', ((35, 44), (36, 30), (41, 18)), 16, 11, HACKLE)
		c.stroke('rim', ((29, 41), (30, 30), (36, 20)), 1.6, 1.2, HACKLE_HI)
		head(c, 42, 15)
	elif pose == 1:  # wings flared high
		fronds(c, [((14, 43), (2, 38), (-3, 36)), ((15, 40), (0, 30), (-2, 22))])
		fan(c, 'far', (40, 38), ((53, 24), (55, 32), (54, 40)), 8, 3)
		# body, neck and head match the standing pose so the two share tiles
		c.ellipse('body', 28, 48, 24, 15, BODY, hi=False)
		c.ellipse('wing', 24, 46, 13, 7, WING, hi=False)
		c.stroke('quill0', ((13, 46), (23, 44), (35, 47)), 1.4, 1, SHEEN)
		c.stroke('neck', ((35, 44), (36, 30), (41, 18)), 16, 11, HACKLE)
		c.stroke('rim', ((29, 41), (30, 30), (36, 20)), 1.6, 1.2, HACKLE_HI)
		head(c, 42, 15)
		fan(c, 'near', (24, 34), ((4, 12), (10, 4), (19, 0), (28, 2)), 10, 6)
		c.ellipse('coverts', 24, 34, 8, 7, WING, hi=False)
		c.stroke('bar', ((17, 33), (23, 30), (30, 32)), 1.6, 1.2, SHEEN)
	else:  # lunging forward to peck, neck stretched, ruff flared
		fronds(c, [((14, 44), (2, 42), (-4, 42)), ((15, 42), (0, 34), (-4, 30)), ((16, 40), (6, 28), (2, 20))])
		c.ellipse('body', 25, 49, 24, 13, BODY, hi=False)
		c.ellipse('wing', 21, 46, 13, 6, WING, hi=False)
		c.stroke('quill0', ((10, 46), (20, 44), (32, 47)), 1.4, 1, SHEEN)
		for k, tip in enumerate(((36, 20), (42, 17), (48, 18), (32, 26), (54, 22))):
			c.stroke(f'ruff{k}', ((43, 31), ((43 + tip[0]) / 2, (31 + tip[1]) / 2), tip), 5, 1.5, HACKLE, hi=HACKLE_HI)
		c.stroke('neck', ((30, 44), (40, 36), (46, 30)), 15, 11, HACKLE)
		head(c, 48, 29)
	c.outline(inner=('quill0', 'rim', 'face', 'eye', 'bar'))
	img = Image.new('RGBA', (56, 56), (0, 0, 0, 0))
	for y in range(56):
		for x in range(56):
			if c.col[y][x]:
				img.putpixel((x, y), c.col[y][x] + (255,))
	return img


# The opponents: front sprite file, the colour of its legs and the wing colours
# for the leap.
OPPONENTS = {
	'nidoroost': dict(src='033_welsummer_young_rooster.png', wing=(172, 86, 40), wing_hi=(214, 146, 64)),
	'silkypuff': dict(src='039_silkie_non_bearded.png', wing=(161, 130, 118), wing_hi=(238, 198, 156)),
}
LEG = (238, 190, 70)
LEG_SHADE = (161, 125, 53)


def legs_top(im):
	"""First row of the legs: below the widest part, where the bird narrows to a few pixels."""
	a = im.split()[3]
	w = [sum(1 for x in range(im.width) if a.getpixel((x, y))) for y in range(im.height)]
	bottom = max(y for y in range(im.height) if w[y])
	y = bottom
	while y > 0 and (w[y - 1] <= 14 or y > bottom - 2):
		y -= 1
	return y


def place(im, dy=0):
	"""Centre the bird at the bottom of a 48x48 frame."""
	bb = im.getbbox()
	bird = im.crop(bb)
	out = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
	out.alpha_composite(bird, ((48 - bird.width) // 2, 48 - bird.height + dy))
	return out


def opponent(name, frame):
	o = OPPONENTS[name]
	im = Image.open(os.path.join(SRC, o['src'])).convert('RGBA')
	top = legs_top(im)
	bottom = im.getbbox()[3]
	if frame == 0:
		return place(im)
	if frame == 1:  # crouch: legs folded up, body dropped
		k = min(4, max(0, bottom - top - 4))
		out = Image.new('RGBA', im.size, (0, 0, 0, 0))
		out.alpha_composite(im.crop((0, 0, im.width, top + 1)), (0, k))
		out.alpha_composite(im.crop((0, top + 1 + k, im.width, im.height)), (0, top + 1 + k))
		out.alpha_composite(im.crop((0, top + 1 + k, im.width, top + 2 + k)), (0, top + 1 + k))
		return place(out)
	# leap: legs off, wings up behind the back, feet thrust forward (left) with spurs
	bb = im.getbbox()
	body = im.crop((0, 0, im.width, top))
	rb.N = 56
	c = rb.Canvas()
	cx = (bb[0] + bb[2]) / 2
	back = bb[2] - (bb[2] - bb[0]) * .35
	mid = top - (top - bb[1]) * .45
	for k, (tx, ty) in enumerate(((back - 2, bb[1] - 3), (back + 5, bb[1] - 1), (back + 10, bb[1] + 4))):
		c.stroke(f'wing{k}', ((back - 6, mid), (back - 2, mid - 6), (tx, ty)), 7, 3, o['wing'], hi=o['wing_hi'])
	for k, lx in enumerate((cx - 2, cx + 3)):
		knee = (lx + 2, top + 5)
		foot = (lx - 7, top + 4 + k)
		c.stroke(f'leg{k}', ((lx, top - 1), knee, foot), 3, 2.6, LEG)
		c.stroke(f'toe{k}', (foot, (foot[0] - 2, foot[1] - 1), (foot[0] - 4, foot[1] - 1)), 2.4, 1.6, LEG_SHADE)
		c.stroke(f'spur{k}', ((lx - 1, top + 4), (lx, top + 6), (lx + 1, top + 7)), 1.8, 1, LEG_SHADE)
	c.outline()
	out = Image.new('RGBA', im.size, (0, 0, 0, 0))
	for y in range(56):
		for x in range(56):
			if c.col[y][x]:
				out.putpixel((x, y), c.col[y][x] + (255,))
	out.alpha_composite(body)
	# the body covers the wing roots; keep the outline where body meets background
	return place(out)


def to_gb(im, bg=255):
	g = Image.new('L', im.size, bg)
	for y in range(im.height):
		for x in range(im.width):
			p = im.getpixel((x, y))
			if p[3]:
				g.putpixel((x, y), rb.gb(p[:3]))
	return g


def frames():
	out = {f'crowgar_{i + 1}': crowgar(i) for i in range(3)}
	for name in OPPONENTS:
		for i in range(3):
			out[f'{name}_{i + 1}'] = opponent(name, i)
	return out


# CROWGAR's tiles share the background tile area with the Game Freak tiles the
# intro loads after them, so the three poses together get at most this many.
MAX_BACK_TILES = 108
OPPONENT_FILES = {'nidoroost': 'red_nidorino', 'silkypuff': 'blue_jigglypuff'}


def tiles_and_maps(poses):
	"""Unique 8x8 tiles for the poses (tile 0 blank, tile 1 solid black, which the
	intro also uses for its black bars) and a 7x7 tile map for each pose."""
	blank, black = (255,) * 64, (0,) * 64
	tiles = [blank, black]
	maps = []
	for im in poses:
		ids = []
		for ty in range(7):
			for tx in range(7):
				t = tuple(im.getpixel((tx * 8 + x, ty * 8 + y)) for y in range(8) for x in range(8))
				if t not in tiles:
					tiles.append(t)
				ids.append(tiles.index(t))
		maps.append(bytes(ids))
	return tiles, maps


def sheet(tiles, cols=8):
	rows = -(-len(tiles) // cols)
	img = Image.new('L', (cols * 8, rows * 8), 255)
	for i, t in enumerate(tiles):
		for j, v in enumerate(t):
			img.putpixel(((i % cols) * 8 + j % 8, (i // cols) * 8 + j // 8), v)
	return img, rows * cols


def install(fr):
	"""Write the game's intro graphics into gfx/intro and colour references into gfx/rooster_src/intro."""
	ref = 'gfx/rooster_src/intro'
	os.makedirs(ref, exist_ok=True)
	for name, im in fr.items():
		im.save(os.path.join(ref, f'{name}.png'))
	tiles, maps = tiles_and_maps([to_gb(fr[f'crowgar_{i + 1}']) for i in range(3)])
	img, total = sheet(tiles)
	assert total <= MAX_BACK_TILES, f'CROWGAR needs {total} tiles, only {MAX_BACK_TILES} fit'
	img.save('gfx/intro/gengar.png')
	for i, m in enumerate(maps):
		open(f'gfx/intro/gengar_{i + 1}.tilemap', 'wb').write(m)
	for name, base in OPPONENT_FILES.items():
		for i in range(3):
			to_gb(fr[f'{name}_{i + 1}']).save(f'gfx/intro/{base}_{i + 1}.png')
	print(f'installed the intro: CROWGAR uses {len(tiles)} tiles ({total} with padding)')


def main():
	fr = frames()
	if len(sys.argv) > 1:  # preview into a folder
		out_dir = sys.argv[1]
		os.makedirs(out_dir, exist_ok=True)
		for name, im in fr.items():
			im.save(os.path.join(out_dir, f'{name}_colour.png'))
			to_gb(im).save(os.path.join(out_dir, f'{name}.png'))
		print('wrote', out_dir)
	else:
		install(fr)


if __name__ == '__main__':
	main()
