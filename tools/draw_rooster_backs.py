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


# Per-species look. stage: 0 chick, 1 cockerel, 2 rooster.
# body/hackle/wing/tail are base colours; lace adds the laced-feather pattern.
SPECIES = {
	1: dict(stage=0, body=(235, 203, 134)),
	2: dict(stage=1, body=(193, 159, 108), hackle=(232, 150, 60), wing=(157, 99, 45), tail=(28, 34, 38), tail_hi=(43, 68, 70)),
	3: dict(stage=2, body=(193, 159, 108), hackle=(232, 150, 60), wing=(157, 99, 45), tail=(28, 34, 38), tail_hi=(43, 68, 70)),
	4: dict(stage=0, body=(195, 128, 84)),
	5: dict(stage=1, body=(131, 41, 27), hackle=(180, 68, 30), wing=(102, 31, 22), tail=(28, 34, 38), tail_hi=(43, 68, 70)),
	6: dict(stage=2, body=(131, 41, 27), hackle=(180, 68, 30), wing=(102, 31, 22), tail=(28, 34, 38), tail_hi=(43, 68, 70)),
	7: dict(stage=0, body=(150, 164, 188)),
	8: dict(stage=1, body=(76, 84, 118), hackle=(98, 110, 141), wing=(62, 74, 102), tail=(52, 62, 90), tail_hi=(98, 110, 141), lace=(42, 48, 77)),
	9: dict(stage=2, body=(76, 84, 118), hackle=(98, 110, 141), wing=(62, 74, 102), tail=(52, 62, 90), tail_hi=(98, 110, 141), lace=(42, 48, 77)),
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

	# tail sickles rise from the back of the bird and arch over towards the viewer
	if big:
		feathers = [
			((8, 23), (-4, 12), (0, 28)),
			((9, 22), (-2, 2), (1, 20)),
			((10, 21), (2, -3), (4, 14)),
			((12, 20), (8, -3), (8, 10)),
		]
		w0 = 4.2
	else:
		feathers = [
			((9, 23), (-1, 15), (1, 26)),
			((10, 22), (2, 8), (3, 20)),
			((11, 21), (7, 7), (7, 16)),
		]
		w0 = 3.6
	for i, f in enumerate(feathers):
		c.stroke('tail', f, w0, 1.6, tail if i % 2 == 0 else shade(tail), tail_hi)
		c.layer -= 1  # all feathers are one part, outlined only on the outside
	c.layer += 1

	# hackle feathers fall over the shoulders in points
	c.layer += 1
	for x in cape:
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
	w = [(edge - 1, ey + 3 + i, COMB) for i in range(3)] + [(edge, ey + 3 + i, COMB) for i in range(n)]
	features(c, w)
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
