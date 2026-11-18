#!/usr/bin/env python3
"""Draw Rooster Edition back sprites (rear views) for the species listed in SPECIES.

Usage: tools/draw_rooster_backs.py [SRC_DIR]

Writes NNN_<breed>.png into SRC_DIR's back/gameboy/ (32x32, four shades),
back/colour/ (32x32 RGBA) and back/colour_x4/ (128x128 RGBA) folders, using the
file names from SRC_DIR/index.csv. SRC_DIR defaults to gfx/rooster_src.

Each bird is seen from behind, facing away towards the opponent at the top right,
and is cut off by the bottom of the frame like the original back sprites. Every
pixel gets a role with a colour; the Game Boy shade comes from the colour using
the same thresholds as the fronts, so the versions always match.
"""

import csv
import os
import sys

from PIL import Image

N = 32
OUTL = (26, 22, 30)  # outline colour used by the rest of the colour set
COMB = (214, 40, 40)
COMB_SHADE = (145, 26, 30)
BEAK = (238, 190, 70)
BEAK_SHADE = (161, 125, 53)


def shade(c):  # same shadow tint as the rest of the colour set
	return (int(c[0] * .68), int(c[1] * .66), int(c[2] * .76))


def light(c):
	return tuple(min(255, int(v + (255 - v) * .35)) for v in c)


def gb(c):
	"""Game Boy shade for a colour, matching how the fronts were converted."""
	if c == OUTL:
		return 0
	y = .299 * c[0] + .587 * c[1] + .114 * c[2]
	return 85 if y < 90 else 170 if y < 185 else 255


# Tail presets: (base width, tip width, [quadratic Bezier feathers from the rump outwards]).
TAILS = {
	# sickles rise from the back and arch over towards the viewer
	'sickle1': (3.6, 1.6, [((9, 23), (-1, 15), (1, 26)), ((10, 22), (2, 8), (3, 20)), ((11, 21), (7, 7), (7, 16))]),
	'sickle2': (4.2, 1.6, [((8, 23), (-4, 12), (0, 28)), ((9, 22), (-2, 2), (1, 20)), ((10, 21), (2, -3), (4, 14)),
		((12, 20), (8, -3), (8, 10))]),
	# hen-feathered: a short, broad fan with no sickles
	'fan1': (6.5, 2.0, [((9, 24), (5, 21), (3, 18)), ((10, 23), (7, 18), (6, 14)), ((11, 22), (10, 17), (10, 13))]),
	'fan2': (7.0, 2.0, [((9, 23), (4, 19), (2, 15)), ((10, 22), (6, 16), (5, 11)), ((11, 21), (10, 15), (10, 9))]),
	# upright, almost vertical tails that grow with each stage
	'upright1': (5.0, 2.0, [((8, 24), (5, 19), (5, 14)), ((10, 23), (8, 16), (9, 11)), ((12, 22), (11, 17), (13, 12))]),
	'upright2': (5.4, 2.0, [((8, 24), (4, 16), (5, 9)), ((10, 23), (7, 12), (9, 5)), ((12, 22), (11, 13), (13, 7))]),
	'upright3': (6.0, 2.0, [((8, 23), (2, 12), (4, 4)), ((10, 22), (6, 8), (9, 1)), ((12, 21), (11, 9), (14, 3)),
		((13, 21), (15, 13), (16, 8))]),
	# moulting: only a ragged stub is left
	'stub': (3.4, 2.0, [((9, 23), (7, 21), (6, 19)), ((10, 22), (9, 20), (9, 17))]),
}

WHITE = (245, 245, 240)
SILVER = (213, 211, 217)
GREEN_BLACK, GREEN_HI = (28, 34, 38), (43, 68, 70)
SKIN = (232, 172, 164)  # bare skin showing through a moult

# Per-species look. stage: 0 chick, 1 cockerel/hen, 2 rooster.
# body/hackle/wing/tail are base colours; lace adds the laced-feather pattern.
# Optional: tail_style (a TAILS key, default by stage), comb ('single', 'rose' or
# 'hen', a small single comb with small wattles), moult (bare patches, ragged tail,
# loose feathers), bare_neck (no hackle cape; `head` colours the feathered crown),
# frizzle (curled-back feathers on the body and wings).
SERAMA = dict(body=(193, 159, 108), hackle=(232, 150, 60), wing=(157, 99, 45), tail=GREEN_BLACK, tail_hi=GREEN_HI)
RIR = dict(body=(131, 41, 27), hackle=(180, 68, 30), wing=(102, 31, 22), tail=GREEN_BLACK, tail_hi=GREEN_HI)
ANDALUSIAN = dict(body=(76, 84, 118), hackle=(98, 110, 141), wing=(62, 74, 102), tail=(52, 62, 90),
	tail_hi=(98, 110, 141), lace=(42, 48, 77))
SEBRIGHT = dict(body=WHITE, hackle=WHITE, wing=SILVER, tail=SILVER, tail_hi=WHITE, comb='rose')
DUTCH = dict(body=(23, 22, 33), hackle=(236, 160, 60), wing=(170, 70, 36), tail=(24, 48, 44), tail_hi=(40, 77, 74))
JAPANESE = dict(body=WHITE, hackle=WHITE, wing=SILVER, tail=GREEN_BLACK, tail_hi=GREEN_HI)
BLACK_RED = dict(body=(23, 22, 33), hackle=(226, 120, 40), wing=(160, 50, 30), tail=GREEN_BLACK, tail_hi=GREEN_HI)
MODERN_GAME = dict(body=SILVER, hackle=(232, 140, 50), wing=(196, 84, 40), tail=WHITE, tail_hi=SILVER)
NAKED_NECK = dict(body=(23, 22, 33), hackle=(196, 58, 50), head=(34, 34, 44), wing=(30, 29, 40), tail=GREEN_BLACK,
	tail_hi=GREEN_HI, bare_neck=True)
BUFF = dict(body=(214, 158, 74), hackle=(226, 172, 84), wing=(197, 148, 76), tail=(197, 148, 76),
	tail_hi=(236, 186, 96), comb='hen')
PEKIN = dict(body=(196, 162, 110), hackle=(212, 180, 126), wing=(185, 155, 114), tail=(185, 155, 114),
	tail_hi=(220, 199, 168), comb='hen')
WELSUMMER_HEN = dict(body=(144, 90, 52), hackle=(206, 152, 80), wing=(112, 68, 44), tail=(97, 59, 39),
	tail_hi=(140, 100, 60), comb='hen')

SPECIES = {
	1: dict(stage=0, body=(235, 203, 134)),
	2: dict(SERAMA, stage=1),
	3: dict(SERAMA, stage=2),
	4: dict(stage=0, body=(195, 128, 84)),
	5: dict(RIR, stage=1),
	6: dict(RIR, stage=2),
	7: dict(stage=0, body=(150, 164, 188)),
	8: dict(ANDALUSIAN, stage=1),
	9: dict(ANDALUSIAN, stage=2),
	10: dict(SEBRIGHT, stage=1, tail_style='fan1', lace=(166, 161, 182)),
	11: dict(SEBRIGHT, stage=1, tail_style='stub', moult=True),
	12: dict(SEBRIGHT, stage=2, tail_style='fan2', lace=(28, 28, 34), tail=WHITE, tail_hi=SILVER),
	13: dict(DUTCH, stage=1),
	14: dict(DUTCH, stage=1, tail_style='stub', moult=True),
	15: dict(DUTCH, stage=2),
	16: dict(JAPANESE, stage=1, tail_style='upright1'),
	17: dict(JAPANESE, stage=1, tail_style='upright2'),
	18: dict(JAPANESE, stage=2, tail_style='upright3'),
	19: dict(BLACK_RED, stage=1),
	20: dict(BLACK_RED, stage=2),
	21: dict(MODERN_GAME, stage=1, tail_style='fan1'),
	22: dict(MODERN_GAME, stage=2, tail_style='fan2'),
	23: dict(stage=0, body=(60, 58, 70)),
	24: dict(NAKED_NECK, stage=2),
	25: dict(BUFF, stage=1, tail_style='fan1'),
	26: dict(BUFF, stage=2, tail_style='fan2'),
	27: dict(PEKIN, stage=1, tail_style='fan1'),
	28: dict(PEKIN, stage=2, tail_style='fan2', frizzle=True),
	29: dict(WELSUMMER_HEN, stage=1, tail_style='fan1'),
	30: dict(WELSUMMER_HEN, stage=2, tail_style='fan2'),
}


class Canvas:
	"""Parts are painted in order; each pixel remembers its part and colour."""

	def __init__(self):
		self.part = [[None] * N for _ in range(N)]
		self.col = [[None] * N for _ in range(N)]
		self.z = [[-1] * N for _ in range(N)]
		self.layer = 0

	def set(self, x, y, part, colour):
		if 0 <= x < N and 0 <= y < N:
			self.part[y][x], self.col[y][x], self.z[y][x] = part, colour, self.layer

	def ellipse(self, part, cx, cy, rx, ry, base, lace=None, rim=True, hi=True):
		"""Filled ellipse lit from the top left: light top, shaded bottom and rim."""
		self.layer += 1
		for y in range(N):
			for x in range(N):
				dx, dy = (x + .5 - cx) / rx, (y + .5 - cy) / ry
				d = dx * dx + dy * dy
				if d > 1:
					continue
				c = base
				if dy > .45 or (rim and d > .72 and dx > .3) or dx < -.82:
					c = shade(base)
				elif hi and dy < -.55 and dx < .3:
					c = light(base)
				if lace and (x + 2 * y) % 4 == 0 and (x // 2 + y) % 2 == 0 and c != light(base):
					c = lace
				self.set(x, y, part, c)

	def stroke(self, part, pts, w0, w1, colour, hi=None):
		"""Thick quadratic Bezier stroke tapering from w0 to w1, with an optional highlight spine."""
		self.layer += 1
		(ax, ay), (bx, by), (cx, cy) = pts
		steps = 60
		for i in range(steps + 1):
			t = i / steps
			x = (1 - t) ** 2 * ax + 2 * (1 - t) * t * bx + t * t * cx
			y = (1 - t) ** 2 * ay + 2 * (1 - t) * t * by + t * t * cy
			r = (w0 + (w1 - w0) * t) / 2
			for py in range(int(y - r - 1), int(y + r + 2)):
				for px in range(int(x - r - 1), int(x + r + 2)):
					if (px + .5 - x) ** 2 + (py + .5 - y) ** 2 <= r * r:
						self.set(px, py, part, colour)
		if hi:
			for i in range(8, steps - 6):
				t = i / steps
				x = (1 - t) ** 2 * ax + 2 * (1 - t) * t * bx + t * t * cx
				y = (1 - t) ** 2 * ay + 2 * (1 - t) * t * by + t * t * cy
				if self.part[int(y)][int(x)] == part:
					self.col[int(y)][int(x)] = hi

	def outline(self, inner=()):
		"""Black edge on every part pixel touching the background or a part painted beneath it.

		The frame edge counts as filled, so the bird is cut off cleanly at the bottom.
		Parts named in `inner` are not outlined against what lies beneath them.
		"""
		edge = []
		for y in range(N):
			for x in range(N):
				p = self.part[y][x]
				if p is None:
					continue
				for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
					if not (0 <= nx < N and 0 <= ny < N):
						continue
					q = self.part[ny][nx]
					if q is None or (q != p and p not in inner and self.z[ny][nx] < self.z[y][x]):
						edge.append((x, y))
						break
		for x, y in edge:
			self.col[y][x] = OUTL


def draw(spec):
	c = Canvas()
	st, body = spec['stage'], spec['body']
	lace = spec.get('lace')
	hackle = spec.get('hackle', body)

	if st == 0:  # chick: one fluffy ball, the head just a bump rising from it
		# head first, then the body over its lower half, both one part so the
		# silhouette is a single outline with no seam at the neck
		c.ellipse('body', 19, 11.5, 7.5, 7.5, body, rim=False)
		c.layer -= 1
		c.ellipse('body', 15.5, 24.5, 12.5, 11.5, body, hi=False)
		# stubby wings swept back towards the viewer: the near one on the left
		# flank, the far one just peeking out past the right side
		c.stroke('wing', ((8, 21), (5, 23), (3, 26.5)), 7, 2.4, body)
		c.stroke('wing', ((25.5, 21), (27.5, 23), (27.5, 26.5)), 5, 2, shade(body))
		c.outline()
		for y in range(N):
			for x in range(N):
				if c.part[y][x] == 'wing' and c.col[y][x] == body and y >= 24:
					c.col[y][x] = shade(body)
		# soft crease where the head rises out of the back
		for x, y in ((12, 16), (13, 17), (14, 17), (15, 18)):
			if c.col[y][x] != OUTL:
				c.col[y][x] = shade(body)
		# eye, and the beak poking past the outline on the right
		ey = 11
		ex = max(x for x in range(N) if c.part[ey][x]) - 2
		c.col[ey][ex] = (20, 20, 24)
		if gb(body) < 170:  # on a dark chick, ring the eye so it still reads
			for x, y in ((ex - 1, ey), (ex, ey - 1), (ex + 1, ey)):
				c.col[y][x] = light(light(body))
		bx = ex + 2
		for x, y, col in ((bx, ey + 1, BEAK), (bx + 1, ey + 1, BEAK), (bx, ey + 2, BEAK_SHADE),
				(bx + 1, ey, OUTL), (bx + 2, ey + 1, OUTL), (bx + 1, ey + 2, OUTL), (bx, ey + 3, OUTL)):
			c.set(x, y, 'beak', col)
		# a little wing nub and fluff at the rump
		for x, y in ((14, 29), (15, 30), (16, 29), (11, 31), (19, 31)):
			c.col[y][x] = shade(body)
		return c

	big = st == 2
	wing, tail, tail_hi = spec['wing'], spec['tail'], spec['tail_hi']

	# neck and head are one part, so the silhouette flows from the shoulders
	# up into the head with no seam; the neck leans forward towards the opponent
	if big:
		c.ellipse('body', 15.5, 25, 14, 11, body, lace)
		c.ellipse('wing', 8, 27.5, 6.5, 4.5, wing, lace, rim=False, hi=False)
		c.stroke('neck', ((17, 21), (18, 14), (21, 10)), 12, 8.5, hackle)
		hx, hy, hr = 22, 8.5, 5
		cape, cy = range(12, 25), 21
	else:
		c.ellipse('body', 15.5, 26, 13, 10, body, lace)
		c.ellipse('wing', 9, 28, 5.5, 4, wing, lace, rim=False, hi=False)
		c.stroke('neck', ((17.5, 22), (18.5, 16), (21, 12)), 10, 7.5, hackle)
		hx, hy, hr = 21.5, 10.5, 4.3
		cape, cy = range(13, 24), 22
	c.layer -= 1
	c.ellipse('neck', hx, hy, hr + .3, hr, hackle, rim=False, hi=False)

	style = spec.get('tail_style', 'sickle2' if big else 'sickle1')
	w0, w1, feathers = TAILS[style]
	for i, f in enumerate(feathers):
		c.stroke('tail', f, w0, w1, tail if i % 2 == 0 else shade(tail), tail_hi)
		c.layer -= 1  # all feathers are one part, outlined only on the outside
	c.layer += 1

	# hackle feathers fall over the shoulders in points
	c.layer += 1
	for x in (() if spec.get('bare_neck') else cape):
		depth = 2 if x % 2 == 0 else 1
		for y in range(cy - 1, cy + depth):
			if c.part[y][x] in ('body', 'wing'):
				c.set(x, y, 'fringe', hackle)
	# light down the back of the neck, shade down the front
	for y in range(N):
		for x in range(N):
			if c.part[y][x] == 'neck':
				left = x > 0 and c.part[y][x - 1] != 'neck'
				right = x < N - 1 and c.part[y][x + 1] != 'neck'
				c.col[y][x] = light(hackle) if left else shade(hackle) if right else hackle
				if spec.get('head') and (x + .5 - hx) ** 2 + (y + .5 - hy + 1.5) ** 2 <= hr * hr * .55:
					c.col[y][x] = spec['head']  # feathered crown above the bare neck
	if spec.get('frizzle'):
		# feathers curl back: short light flicks with a shadow under each
		for y in range(N - 1):
			for x in range(1, N):
				if c.part[y][x] in ('body', 'wing') and (x * 3 + y * 5) % 11 == 0:
					base = body if c.part[y][x] == 'body' else wing
					c.col[y][x] = light(base)
					if c.part[y + 1][x - 1] == c.part[y][x]:
						c.col[y + 1][x - 1] = shade(base)
	if spec.get('moult'):
		# bare skin showing through where feathers have dropped
		for px, py, r in ((11, 25, 2.2), (19, 29, 1.8), (6, 28, 1.5), (23, 24, 1.4), (16, 22, 1.2)):
			for y in range(N):
				for x in range(N):
					if c.part[y][x] in ('body', 'wing') and (x + .5 - px) ** 2 + (y + .5 - py) ** 2 <= r * r:
						c.col[y][x] = SKIN if y < py + r * .4 else shade(SKIN)
	c.outline(inner=('wing', 'fringe', 'neck'))
	# soft wing edge instead of a black outline
	for y in range(N):
		for x in range(N):
			if c.part[y][x] == 'wing' and c.col[y][x] != OUTL:
				if any(0 <= x + dx < N and 0 <= y + dy < N and c.part[y + dy][x + dx] == 'body'
						for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))):
					c.col[y][x] = shade(wing)

	# face details go on after the outline, each ringed outwards so small
	# features keep all their pixels
	ix, iy = round(hx - .5), round(hy - .5)
	top = min(y for y in range(N) if c.part[y][ix] == 'neck')
	if spec.get('comb') == 'rose':
		# rose comb: low and wide and bumpy, with a spike pointing back
		heights = [2, 2, 3, 2, 3, 2, 1] if big else [2, 3, 2, 2, 1]
		x0 = ix - len(heights) // 2 + 1
		comb = [(x0 + i, top - k, COMB_SHADE if k == 0 else COMB) for i, h in enumerate(heights) for k in range(h)]
		comb += [(x0 - 1, top - 1, COMB), (x0 - 2, top - 1, COMB), (x0 - 3, top - 2, COMB)]
	elif spec.get('comb') == 'hen':
		# a hen's single comb: small and low
		heights = [2, 3, 3, 3, 2, 1] if big else [1, 2, 2, 2, 1]
		x0 = ix - len(heights) // 2
		comb = [(x0 + i, top - k, COMB_SHADE if k == 0 else COMB) for i, h in enumerate(heights) for k in range(h)]
	else:
		# single comb in profile: a solid blade with spikes, tallest in the middle
		heights = [3, 5, 3, 6, 3, 6, 3, 5, 2] if big else [2, 3, 2, 4, 2, 3, 2]
		x0 = ix - len(heights) // 2
		comb = [(x0 + i, top - k, COMB_SHADE if k == 0 else COMB) for i, h in enumerate(heights) for k in range(h)]
	features(c, comb)
	ey = iy
	edge = max(x for x in range(N) if c.part[ey + 1][x] == 'neck')
	c.col[ey][edge - 3] = (20, 20, 24)
	c.col[ey][edge - 4] = light(hackle)
	n = 3 if big else 2
	beak = [(edge + i, ey + 1, BEAK) for i in range(n)] + [(edge + i, ey + 2, BEAK_SHADE) for i in range(n - 1)]
	features(c, beak)
	drop = 2 if spec.get('comb') == 'hen' else 3  # hens have small wattles
	w = [(edge - 1, ey + 3 + i, COMB) for i in range(drop)] + [(edge, ey + 3 + i, COMB) for i in range(n if drop == 3 else 1)]
	features(c, w)
	if spec.get('moult'):
		# a couple of loose feathers drifting away
		for fx, fy in ((2, 7), (6, 3)):
			features(c, [(fx, fy, hackle), (fx + 1, fy, hackle), (fx + 1, fy - 1, shade(hackle))])
	return c


def features(c, cells):
	"""Paint small details, then outline them outwards into empty space."""
	c.layer += 1
	for x, y, col in cells:
		c.set(x, y, 'feature', col)
	for x, y, _ in cells:
		for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
			if 0 <= nx < N and 0 <= ny < N and c.part[ny][nx] is None:
				c.set(nx, ny, 'ring', OUTL)


def save(c, base, name):
	gbimg = Image.new('L', (N, N), 255)
	col = Image.new('RGBA', (N, N), (0, 0, 0, 0))
	for y in range(N):
		for x in range(N):
			if c.col[y][x] is not None:
				gbimg.putpixel((x, y), gb(c.col[y][x]))
				col.putpixel((x, y), c.col[y][x] + (255,))
	for sub, img in (('gameboy', gbimg), ('colour', col), ('colour_x4', col.resize((N * 4, N * 4), Image.NEAREST))):
		d = os.path.join(base, 'back', sub)
		os.makedirs(d, exist_ok=True)
		img.save(os.path.join(d, name))


def main():
	src = sys.argv[1] if len(sys.argv) > 1 else 'gfx/rooster_src'
	files = {int(r['number']): r['file'] for r in csv.DictReader(open(os.path.join(src, 'index.csv')))}
	for dex, spec in sorted(SPECIES.items()):
		save(draw(spec), src, files[dex])
		print(f'{dex:03} back <- {files[dex]}')


if __name__ == '__main__':
	main()
