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
import math
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
	# a showy round fan of nine feathers spread behind the bird
	'nine': (3.4, 2.4, [((9, 21), (9 + 6 * math.cos(math.radians(a)), 21 + 6 * math.sin(math.radians(a))),
		(9 + 12.5 * math.cos(math.radians(a)), 21 + 12.5 * math.sin(math.radians(a)))) for a in range(185, 296, 13)]),
	# rumpless: no tail at all
	'none': (0, 0, []),
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
# frizzle (curled-back feathers on the body and wings), tail_tip (colour at the
# end of each tail feather), silkie (pom-pom crest, walnut comb, tufty outline),
# beard (a muff under the beak instead of wattles), earlobe (colour of the lobe
# behind the eye), nest (sitting on a straw nest), crest (True for the hackle
# colour, or a colour) with crest_size and crest_spots, fluffy (tufty outline),
# comb 'walnut' or 'v' (small combs in front of a crest), trio (three chicks),
# comb 'pea' (low and small), skin (colour of comb, wattles and beak, for
# all-black birds), hackle_stripes (colour of stripes down the neck feathers),
# ear_tufts (feather tufts sticking out behind the face), heads (extra heads
# standing behind the first), head on a chick (colour of its head).
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
SILKIE = dict(silkie=True, crest=True, fluffy=True, comb='walnut', tail=(60, 62, 72), tail_hi=(119, 122, 125), tail_style='stub')
WHITE_SILKIE = dict(SILKIE, body=WHITE, hackle=WHITE, wing=SILVER)
BUFF_SILKIE = dict(SILKIE, body=(238, 198, 156), hackle=(245, 221, 196), wing=(207, 171, 141))
WELSUMMER = dict(body=(39, 26, 27), hackle=(214, 146, 64), wing=(172, 86, 40), tail=GREEN_BLACK, tail_hi=GREEN_HI)
RED_FRIZZLE = dict(body=(170, 56, 30), hackle=(214, 96, 40), wing=(130, 46, 27), tail=(113, 39, 24),
	tail_hi=(145, 63, 30), frizzle=True)
ROSECOMB = dict(body=(34, 34, 44), hackle=(30, 29, 40), wing=(23, 22, 33), tail=(24, 48, 44), tail_hi=(40, 77, 74),
	comb='rose', earlobe=WHITE)
POLISH = dict(body=(224, 176, 96), hackle=(224, 176, 96), wing=(195, 152, 86), tail=(195, 152, 86),
	tail_hi=(246, 236, 212), lace=(246, 236, 212), crest=True, comb='v')
HOUDAN = dict(body=(34, 34, 44), hackle=(34, 34, 44), wing=(23, 22, 33), tail=GREEN_BLACK, tail_hi=GREEN_HI,
	lace=WHITE, crest=True, crest_spots=WHITE, comb='v', beard=True)
COCHIN = dict(body=(155, 148, 186), hackle=(178, 172, 206), wing=(121, 113, 156), tail=(155, 148, 186),
	tail_hi=(178, 172, 206), comb='hen', fluffy=True)
NANKIN = dict(body=(186, 121, 56), hackle=(232, 160, 70), wing=(145, 92, 47), tail=GREEN_BLACK, tail_hi=GREEN_HI)
YELLOW_PEKIN = dict(body=(226, 182, 70), hackle=(242, 202, 86), wing=(211, 174, 78), tail=(211, 174, 78),
	tail_hi=(238, 211, 144), comb='hen', fluffy=True)
BLUE_PEKIN = dict(body=(92, 110, 146), hackle=(112, 132, 168), wing=(76, 87, 127), tail=(76, 87, 127),
	tail_hi=(112, 132, 168), comb='hen', fluffy=True)
ASIL = dict(body=(92, 34, 28), hackle=(152, 62, 30), wing=(120, 44, 30), tail=GREEN_BLACK, tail_hi=GREEN_HI, comb='pea')
RED_SUSSEX = dict(body=(139, 46, 27), hackle=(166, 60, 30), wing=(108, 35, 22), tail=GREEN_BLACK, tail_hi=GREEN_HI,
	hackle_stripes=(28, 28, 34))
LAVENDER_ARAUCANA = dict(body=(153, 148, 186), hackle=(176, 172, 206), wing=(119, 113, 156), tail=(119, 113, 156),
	tail_hi=(176, 172, 206), comb='pea', tail_style='none', ear_tufts=True)
CEMANI = dict(body=(34, 34, 44), hackle=(30, 30, 40), wing=(23, 22, 33), tail=(30, 29, 40), tail_hi=(44, 65, 72),
	skin=(54, 48, 62))
MALAY = dict(body=(96, 36, 28), hackle=(172, 86, 36), wing=(130, 54, 30), tail=GREEN_BLACK, tail_hi=GREEN_HI,
	comb='pea', tail_style='stub')
LEGHORN = dict(body=WHITE, hackle=WHITE, wing=SILVER, tail=WHITE, tail_hi=SILVER, earlobe=WHITE)
BLR_WYANDOTTE = dict(body=(153, 66, 41), hackle=(190, 92, 50), wing=(119, 50, 34), tail=(76, 84, 124),
	tail_hi=(112, 128, 164), lace=(76, 84, 124), comb='rose')
BARNEVELDER = dict(body=(108, 57, 32), hackle=(40, 36, 42), wing=(84, 43, 27), tail=GREEN_BLACK, tail_hi=GREEN_HI,
	lace=(28, 28, 34))
NEW_HAMPSHIRE = dict(body=(180, 91, 45), hackle=(226, 142, 62), wing=(140, 69, 38), tail=GREEN_BLACK, tail_hi=GREEN_HI)
JERSEY_GIANT = dict(body=(30, 34, 42), hackle=(26, 29, 38), wing=(20, 22, 31), tail=(24, 48, 44), tail_hi=(40, 77, 74))
MINORCA = dict(body=(34, 34, 44), hackle=(30, 29, 40), wing=(23, 22, 33), tail=(24, 48, 44), tail_hi=(40, 77, 74),
	earlobe=WHITE)
SULTAN = dict(body=WHITE, hackle=WHITE, wing=SILVER, tail=WHITE, tail_hi=SILVER, crest=True, comb='v', beard=True)
MARANS = dict(body=(23, 22, 33), hackle=(196, 104, 44), wing=(30, 29, 40), tail=GREEN_BLACK, tail_hi=GREEN_HI)
HAMBURG = dict(body=(245, 245, 240), hackle=(213, 211, 217), wing=(213, 211, 217), tail=GREEN_BLACK, tail_hi=GREEN_HI,
	lace=(28, 34, 38), comb='rose', earlobe=WHITE)
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
	31: dict(WELSUMMER_HEN, stage=2, tail_style='fan2', nest=(214, 180, 96)),
	32: dict(WELSUMMER, stage=1, tail_style='fan1'),
	33: dict(WELSUMMER, stage=1),
	34: dict(WELSUMMER, stage=2),
	35: dict(WHITE_SILKIE, stage=1),
	36: dict(WHITE_SILKIE, stage=2, beard=True),
	37: dict(RED_FRIZZLE, stage=1, tail_style='fan1'),
	38: dict(RED_FRIZZLE, stage=2, tail_style='nine', tail_tip=(240, 214, 200)),
	39: dict(BUFF_SILKIE, stage=1),
	40: dict(BUFF_SILKIE, stage=2, beard=True),
	41: dict(ROSECOMB, stage=1),
	42: dict(ROSECOMB, stage=2),
	43: dict(stage=0, body=(232, 196, 124)),
	44: dict(POLISH, stage=1, tail_style='fan1', crest_size=.6),
	45: dict(POLISH, stage=2, crest_size=1.6),
	46: dict(HOUDAN, stage=1, crest_size=.4),
	47: dict(HOUDAN, stage=2, crest_size=1.8),
	48: dict(COCHIN, stage=1, tail_style='fan1'),
	49: dict(COCHIN, stage=2, tail_style='fan2'),
	50: dict(stage=0, body=(156, 106, 64)),
	51: dict(stage=0, body=(156, 106, 64), trio=True),
	52: dict(NANKIN, stage=1),
	53: dict(NANKIN, stage=2),
	54: dict(YELLOW_PEKIN, stage=1, tail_style='fan1'),
	55: dict(BLUE_PEKIN, stage=2, tail_style='fan2'),
	56: dict(stage=0, body=(190, 120, 70)),
	57: dict(ASIL, stage=2, tail_style='sickle1'),
	58: dict(stage=0, body=(196, 110, 60)),
	59: dict(RED_SUSSEX, stage=2),
	60: dict(stage=0, body=(190, 186, 216)),
	61: dict(LAVENDER_ARAUCANA, stage=1),
	62: dict(LAVENDER_ARAUCANA, stage=2),
	63: dict(stage=0, body=(40, 40, 50), skin=(54, 54, 66)),
	64: dict(CEMANI, stage=1),
	65: dict(CEMANI, stage=2),
	66: dict(stage=0, body=(196, 130, 76)),
	67: dict(MALAY, stage=1),
	68: dict(MALAY, stage=2),
	69: dict(stage=0, body=(246, 222, 120)),
	70: dict(LEGHORN, stage=1, tail_style='fan1'),
	71: dict(LEGHORN, stage=2),
	72: dict(stage=0, body=(170, 150, 170)),
	73: dict(BLR_WYANDOTTE, stage=2),
	74: dict(stage=0, body=(150, 104, 64)),
	75: dict(BARNEVELDER, stage=1),
	76: dict(BARNEVELDER, stage=2),
	77: dict(stage=0, body=(226, 160, 95)),
	78: dict(NEW_HAMPSHIRE, stage=2),
	79: dict(stage=0, body=(46, 48, 58)),
	80: dict(JERSEY_GIANT, stage=2),
	81: dict(stage=0, body=(226, 226, 230), head=(44, 44, 54)),
	82: dict(stage=0, body=(226, 226, 230), head=(44, 44, 54), trio=True),
	84: dict(MINORCA, stage=1, heads=2),
	85: dict(MINORCA, stage=2, heads=3),
	86: dict(SULTAN, stage=1, tail_style='fan1', crest_size=.4),
	87: dict(SULTAN, stage=2, crest_size=1.2),
	88: dict(stage=0, body=(44, 44, 54)),
	89: dict(MARANS, stage=2),
	90: dict(HAMBURG, stage=1),
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


def chick_shapes(c, body, dx, dy, sc, k):
	"""A chick: one fluffy ball, the head just a bump rising from it, placed at
	(dx, dy) and scaled by sc. Parts are suffixed with k so chicks can overlap."""
	X = lambda v: dx + v * sc
	Y = lambda v: dy + v * sc
	# head first, then the body over its lower half, both one part so the
	# silhouette is a single outline with no seam at the neck
	c.ellipse('body' + k, X(19), Y(11.5), 7.5 * sc, 7.5 * sc, body, rim=False)
	c.layer -= 1
	c.ellipse('body' + k, X(15.5), Y(24.5), 12.5 * sc, 11.5 * sc, body, hi=False)
	# stubby wings swept back towards the viewer: the near one on the left
	# flank, the far one just peeking out past the right side
	c.stroke('wing' + k, ((X(8), Y(21)), (X(5), Y(23)), (X(3), Y(26.5))), 7 * sc, 2.4 * sc, body)
	c.stroke('wing' + k, ((X(25.5), Y(21)), (X(27.5), Y(23)), (X(27.5), Y(26.5))), 5 * sc, 2 * sc, shade(body))


def chick_details(c, body, dx, dy, sc, k, beak=BEAK, beak_shade=BEAK_SHADE, head=None):
	"""Shading, eye and beak for a chick drawn by chick_shapes, after outlining."""
	P = lambda x, y: (round(dx + x * sc), round(dy + y * sc))
	if head:  # a differently coloured head, like a Lakenvelder's
		for y in range(N):
			for x in range(N):
				if (c.part[y][x] == 'body' + k and c.col[y][x] != OUTL and y + .5 < dy + 17 * sc
						and (x + .5 - dx - 19 * sc) ** 2 + (y + .5 - dy - 11.5 * sc) ** 2 <= (7.5 * sc) ** 2):
					c.col[y][x] = light(head) if y + .5 < dy + 7 * sc else head
	for y in range(N):
		for x in range(N):
			if c.part[y][x] == 'wing' + k and c.col[y][x] == body and y >= dy + 24 * sc:
				c.col[y][x] = shade(body)
	# soft crease where the head rises out of the back
	for x, y in (P(12, 16), P(13, 17), P(14, 17), P(15, 18)):
		if 0 <= y < N and c.part[y][x] == 'body' + k and c.col[y][x] != OUTL:
			c.col[y][x] = shade(body)
	# eye, and the beak poking past the outline on the right
	ey = P(0, 11)[1]
	ex = max(x for x in range(N) if c.part[ey][x] == 'body' + k) - 2
	c.col[ey][ex] = (20, 20, 24)
	if gb(body) < 170:  # on a dark chick, ring the eye so it still reads
		for x, y in ((ex - 1, ey), (ex, ey - 1), (ex + 1, ey)):
			c.col[y][x] = light(light(body))
	bx = ex + 2
	for x, y, col in ((bx, ey + 1, beak), (bx + 1, ey + 1, beak), (bx, ey + 2, beak_shade),
			(bx + 1, ey, OUTL), (bx + 2, ey + 1, OUTL), (bx + 1, ey + 2, OUTL), (bx, ey + 3, OUTL)):
		c.set(x, y, 'beak', col)
	# fluff at the rump
	for x, y in (P(14, 29), P(15, 30), P(16, 29), P(11, 31), P(19, 31)):
		if 0 <= y < N and c.part[y][x] == 'body' + k and c.col[y][x] != OUTL:
			c.col[y][x] = shade(body)


HEAD_PARTS = ('neck', 'feature', 'ring', 'crest')


def draw(spec):
	"""Draw a bird; extra heads are copies of its head and neck, set back behind it."""
	c = draw_one(spec)
	for dx, dy in ((-7, 1), (-13, 3))[:spec.get('heads', 1) - 1]:
		h = draw_one(spec)
		for y in range(N):
			for x in range(N):
				if h.part[y][x] in HEAD_PARTS and 0 <= x + dx < N and 0 <= y + dy < N:
					tx, ty = x + dx, y + dy
					if c.part[ty][tx] in (None, 'tail'):
						c.part[ty][tx], c.col[ty][tx] = 'neck2', h.col[y][x]
		# the bird in front gets an edge where it overlaps the copy, which
		# then becomes part of the bird for the next copy back
		edge = [(x, y) for y in range(N) for x in range(N) if c.part[y][x] not in (None, 'neck2', 'tail')
			and any(0 <= x + ox < N and 0 <= y + oy < N and c.part[y + oy][x + ox] == 'neck2'
				for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)))]
		for x, y in edge:
			c.col[y][x] = OUTL
		for y in range(N):
			for x in range(N):
				if c.part[y][x] == 'neck2':
					c.part[y][x] = 'neck_back'
	return c


def draw_one(spec):
	c = Canvas()
	st, body = spec['stage'], spec['body']
	lace = spec.get('lace')
	hackle = spec.get('hackle', body)

	if st == 0:
		# one chick, or a huddle of three smaller ones (back two first)
		chicks = [(-1.5, 7, .62, 'a'), (12.5, 5, .62, 'b'), (5, 12.5, .66, 'c')] if spec.get('trio') else [(0, 0, 1, '')]
		for dx, dy, sc, k in chicks:
			chick_shapes(c, body, dx, dy, sc, k)
		c.outline()
		for dx, dy, sc, k in chicks:
			skin = spec.get('skin')
			chick_details(c, body, dx, dy, sc, k, skin or BEAK, shade(skin) if skin else BEAK_SHADE, spec.get('head'))
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
	if spec.get('crest'):
		# pom-pom crest swept back over the head, outlined so it stands out
		ccol = spec['crest'] if isinstance(spec['crest'], tuple) else hackle
		grow = spec.get('crest_size', 0)
		cx, cy0, r = hx - 1.5 - grow * .4, hy - 3.2 + grow * .3, hr + .2 + grow
		c.layer += 1
		for y in range(N):
			for x in range(N):
				d = ((x + .5 - cx) / r) ** 2 + ((y + .5 - cy0) / (r - .6)) ** 2
				# tufts: the edge wobbles in and out around the crest
				wob = .18 * math.cos(math.atan2(y + .5 - cy0, x + .5 - cx) * 7)
				if d <= 1 + wob:
					col = shade(ccol) if y + .5 > cy0 + r * .45 else light(ccol) if y < cy0 - 1 else ccol
					if spec.get('crest_spots') and x % 2 == 0 and (y + x // 2) % 3 == 0:
						col = spec['crest_spots']
					c.set(x, y, 'crest', col)
	if spec.get('fluffy'):
		# hair-like plumage: tufts poke out along the top of the body
		for x in range(3, 29, 3):
			top_y = min((y for y in range(N) if c.part[y][x] == 'body'), default=None)
			if top_y and c.part[top_y - 1][x] is None:
				c.set(x, top_y - 1, 'body', body)

	style = spec.get('tail_style', 'sickle2' if big else 'sickle1')
	w0, w1, feathers = TAILS[style]
	for i, f in enumerate(feathers):
		c.stroke('tail', f, w0, w1, tail if i % 2 == 0 else shade(tail), tail_hi)
		c.layer -= 1  # all feathers are one part, outlined only on the outside
	c.layer += 1
	if spec.get('tail_tip'):
		for f in feathers:
			ex, ey0 = f[2]
			for y in range(N):
				for x in range(N):
					if c.part[y][x] == 'tail' and (x + .5 - ex) ** 2 + (y + .5 - ey0) ** 2 <= 2.2:
						c.col[y][x] = spec['tail_tip']

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
	if spec.get('hackle_stripes'):
		# a dark stripe down the middle of each hackle feather
		for y in range(N):
			for x in range(N):
				if c.part[y][x] in ('neck', 'fringe') and y > hy + hr * .6 and (x - y // 2) % 3 == 0:
					c.col[y][x] = spec['hackle_stripes']
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
	if spec.get('nest'):
		straw = spec['nest']
		c.layer += 1
		for y in range(26, N):
			for x in range(N):
				if ((x + .5 - 15.5) / 16) ** 2 + ((y + .5 - 31) / 4.5) ** 2 <= 1:
					c.set(x, y, 'nest', shade(straw) if (x * 2 + y * 3) % 5 == 0 else light(straw) if y < 28 else straw)
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
	skin = spec.get('skin')
	CC, CS = (skin, shade(skin)) if skin else (COMB, COMB_SHADE)
	BC, BS = (skin, shade(skin)) if skin else (BEAK, BEAK_SHADE)
	ix, iy = round(hx - .5), round(hy - .5)
	top = min(y for y in range(N) if c.part[y][ix] == 'neck')
	if spec.get('comb') == 'rose':
		# rose comb: low and wide and bumpy, with a spike pointing back
		heights = [2, 2, 3, 2, 3, 2, 1] if big else [2, 3, 2, 2, 1]
		x0 = ix - len(heights) // 2 + 1
		comb = [(x0 + i, top - k, CS if k == 0 else CC) for i, h in enumerate(heights) for k in range(h)]
		comb += [(x0 - 1, top - 1, CC), (x0 - 2, top - 1, CC), (x0 - 3, top - 2, CC)]
	elif spec.get('comb') == 'walnut':
		# a Silkie's small dark walnut comb in front of the crest, and its dark face
		dark = (96, 44, 78)
		face = max(x for x in range(N) if c.part[iy][x] == 'neck')
		comb = [(face - 1, iy - 3, dark), (face, iy - 3, dark), (face - 1, iy - 2, shade(dark))]
		for x, y in ((face - 1, iy), (face - 2, iy + 1), (face - 1, iy + 1), (face - 3, iy)):
			c.col[y][x] = (70, 60, 84)
	elif spec.get('comb') == 'v':
		# a small V-shaped comb peeking out in front of the crest
		face = max(x for x in range(N) if c.part[iy][x] == 'neck')
		comb = [(face - 2, iy - 3, CC), (face - 2, iy - 4, CC), (face - 1, iy - 3, CS), (face, iy - 4, CC)]
	elif spec.get('comb') == 'pea':
		# a pea comb: three low ridges hugging the top of the head
		heights = [1, 2, 2, 2, 1] if big else [1, 2, 1, 1]
		x0 = ix - len(heights) // 2 + 1
		comb = [(x0 + i, top - k, CS if k == 0 else CC) for i, h in enumerate(heights) for k in range(h)]
	elif spec.get('comb') == 'hen':
		# a hen's single comb: small and low
		heights = [2, 3, 3, 3, 2, 1] if big else [1, 2, 2, 2, 1]
		x0 = ix - len(heights) // 2
		comb = [(x0 + i, top - k, CS if k == 0 else CC) for i, h in enumerate(heights) for k in range(h)]
	else:
		# single comb in profile: a solid blade with spikes, tallest in the middle
		heights = [3, 5, 3, 6, 3, 6, 3, 5, 2] if big else [2, 3, 2, 4, 2, 3, 2]
		x0 = ix - len(heights) // 2
		comb = [(x0 + i, top - k, CS if k == 0 else CC) for i, h in enumerate(heights) for k in range(h)]
	features(c, comb)
	ey = iy
	edge = max(x for x in range(N) if c.part[ey + 1][x] == 'neck')
	c.col[ey][edge - 3] = (20, 20, 24)
	c.col[ey][edge - 4] = light(hackle)
	n = 3 if big else 2
	beak = [(edge + i, ey + 1, BC) for i in range(n)] + [(edge + i, ey + 2, BS) for i in range(n - 1)]
	features(c, beak)
	if spec.get('beard'):
		# a fluffy muff under the beak instead of wattles
		muff = [(edge + dx, ey + 3 + dy, shade(hackle) if dy == 2 or dx == 1 else hackle)
			for dx in (-2, -1, 0, 1) for dy in (0, 1, 2) if (dx, dy) != (1, 2)]
		features(c, muff)
	elif spec.get('silkie'):
		pass  # wattles hidden in the fluff
	else:
		drop = 2 if spec.get('comb') == 'hen' else 3  # hens have small wattles
		w = [(edge - 1, ey + 3 + i, CC) for i in range(drop)] + [(edge, ey + 3 + i, CC) for i in range(n if drop == 3 else 1)]
		features(c, w)
	if spec.get('ear_tufts'):
		# tufts of feathers sprouting from behind the face and curling back
		dark = shade(spec['wing'])
		tuft = [(edge - 5, ey + 2, spec['wing']), (edge - 6, ey + 2, dark), (edge - 7, ey + 1, dark),
			(edge - 8, ey + 1, dark), (edge - 9, ey, dark), (edge - 6, ey + 3, dark), (edge - 7, ey + 3, spec['wing'])]
		for x, y, col in tuft:
			c.col[y][x] = col
	if spec.get('earlobe'):
		for x, y in ((edge - 4, ey + 2), (edge - 5, ey + 2), (edge - 4, ey + 3)):
			c.col[y][x] = spec['earlobe']
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
