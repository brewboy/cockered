#!/usr/bin/env python3
"""Draw the Mewtwo goose sprite (#150) for Rooster Edition.

Usage: tools/draw_rooster_goose.py [SRC_DIR]

Writes 150_lab_bred_goose.png into SRC_DIR's gameboy/ (56x56, four shades),
colour/ (56x56 RGBA) and colour_x4/ (224x224 RGBA) folders.
SRC_DIR defaults to gfx/rooster_src. Every pixel is tagged with a role, and
each role has both a Game Boy shade and a colour, so the versions always match.
"""

import math
import os
import struct
import sys
import zlib

W = H = 56
OUTL = (26, 22, 30)  # outline colour used by the rest of the colour set


def shade(c):  # same shadow tint as the rest of the colour set
	return (int(c[0] * .68), int(c[1] * .66), int(c[2] * .76))


BODY = (238, 238, 232)
# role: (Game Boy shade, colour)
ROLES = {
	'bg':           (255, None),
	'body':         (255, BODY),
	'body_shade':   (170, shade(BODY)),
	'wing':         (255, (230, 230, 226)),
	'wing_edge':    (85,  (124, 124, 136)),
	'wing_feather': (170, (196, 196, 200)),
	'beak':         (170, (240, 150, 60)),
	'nostril':      (85,  shade((240, 150, 60))),
	'leg':          (85,  (226, 124, 46)),
	'outline':      (0,   OUTL),
	'eye_socket':   (0,   (112, 44, 178)),
	'eye_core':     (255, (244, 216, 255)),
	'eye_glow':     (170, (196, 146, 252)),
	'stitch':       (85,  (110, 86, 100)),
	'stitch_cross': (0,   OUTL),
	'band':         (170, (250, 212, 60)),
	'band_edge':    (0,   OUTL),
	'cable':        (0,   (54, 56, 66)),
	'node':         (85,  (52, 196, 88)),
	'node_edge':    (0,   (20, 84, 40)),
	'node_core':    (255, (222, 255, 222)),
	'node_glow':    (170, (140, 240, 150)),
}

# part labels used to build the silhouette
BG, BODYP, WING, NECK, HEAD, BEAK, LEG, FOOT, TAIL = range(9)


def draw():
	lab = [[BG] * W for _ in range(H)]

	def put(x, y, v):
		if 0 <= x < W and 0 <= y < H: lab[y][x] = v

	def ellipse(cx, cy, rx, ry, v, rot=0):
		c, s = math.cos(rot), math.sin(rot)
		for y in range(H):
			for x in range(W):
				dx, dy = x + .5 - cx, y + .5 - cy
				u, w = dx * c + dy * s, -dx * s + dy * c
				if (u / rx) ** 2 + (w / ry) ** 2 <= 1: lab[y][x] = v

	def poly(pts, v):
		for y in range(H):
			for x in range(W):
				px, py = x + .5, y + .5
				inside = False
				for i in range(len(pts)):
					(x1, y1), (x2, y2) = pts[i], pts[i - 1]
					if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
						inside = not inside
				if inside: lab[y][x] = v

	def bez(p0, p1, p2, t):
		return tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t * t * c for a, b, c in zip(p0, p1, p2))

	# silhouette: tail, body, S-curved neck, head, beak, wing, legs and webbed feet
	poly([(40, 30), (51, 25), (52, 30), (46, 37)], TAIL)
	ellipse(32, 37, 15, 8.5, BODYP, rot=-0.12)
	N0, N1, N2 = (22, 35), (11, 27), (15, 13)
	for i in range(60):
		x, y = bez(N0, N1, N2, i / 59)
		r = 4.6 - 1.2 * (i / 59)
		ellipse(x, y, r, r, NECK)
	ellipse(15.5, 10.5, 5.5, 4.5, HEAD)
	poly([(11, 9), (3, 11.5), (4, 13), (11, 14)], BEAK)
	ellipse(33, 34, 10.5, 5, WING, rot=-0.15)
	for lx in (27, 34):
		for y in range(43, 52):
			for x in range(lx - 1, lx + 2): put(x, y, LEG)
		poly([(lx + 1.5, 50), (lx - 5, 54), (lx + 2.5, 54)], FOOT)

	base = {BG: 'bg', BODYP: 'body', WING: 'wing', NECK: 'body', HEAD: 'body', BEAK: 'beak', LEG: 'leg', FOOT: 'leg', TAIL: 'body'}
	role = [[base[lab[y][x]] for x in range(W)] for y in range(H)]

	def L(x, y): return lab[y][x] if 0 <= x < W and 0 <= y < H else BG

	def set_(x, y, r):
		if 0 <= x < W and 0 <= y < H: role[y][x] = r

	# pale grey-white shading: belly underside, tail underside, back of neck
	for y in range(H):
		for x in range(W):
			p = lab[y][x]
			if p == BODYP and y >= 39: role[y][x] = 'body_shade'
			if p == TAIL and y >= 31: role[y][x] = 'body_shade'
			if p == NECK and L(x + 3, y) == BG and y < 30 and L(x + 2, y) == BG: role[y][x] = 'body_shade'
	# wing: dark edge, feather rows
	for y in range(H):
		for x in range(W):
			if lab[y][x] == WING:
				if any(L(x + dx, y + dy) != WING for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
					role[y][x] = 'wing_edge'
				elif (x + y // 2) % 5 == 0 and y > 32:
					role[y][x] = 'wing_feather'
	# outline every edge touching the background, plus the beak/head seam
	for y in range(H):
		for x in range(W):
			p = lab[y][x]
			if p == BG: continue
			nb = [L(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
			if BG in nb or (p == BEAK and HEAD in nb): set_(x, y, 'outline')
	for x in (6, 7, 8): set_(x, 12, 'nostril')
	# glowing eye: socket ring, bright core, glow speckles
	for dx, dy in ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)): set_(13 + dx, 8 + dy, 'eye_socket')
	set_(14, 9, 'eye_core')
	for x, y in ((12, 7), (16, 7), (12, 11), (16, 11), (11, 9), (17, 9)): set_(x, y, 'eye_glow')
	# stitched seam down the middle of the neck
	seam = [tuple(round(v) for v in bez(N0, N1, N2, 0.3 + 0.5 * t / 14)) for t in range(15)]
	for i, (x, y) in enumerate((x - 1, y) for x, y in seam):
		set_(x, y, 'stitch')
		if i % 3 == 1: set_(x - 1, y, 'stitch_cross'); set_(x + 1, y, 'stitch_cross')
	# lab band on the front ankle
	for x in range(25, 30): set_(x, 47, 'band_edge'); set_(x, 49, 'band_edge')
	for x in range(26, 29): set_(x, 48, 'band')
	set_(25, 48, 'band_edge'); set_(29, 48, 'band_edge')
	# cable from the back of the head to a glowing node
	for i in range(80):
		x, y = (round(v) for v in bez((20, 8), (25, 0), (31, 4), i / 79))
		set_(x, y, 'cable')
	nx, ny = 33, 6
	for y in range(ny - 2, ny + 3):
		for x in range(nx - 2, nx + 3):
			d = (x - nx) ** 2 + (y - ny) ** 2
			if d <= 5: set_(x, y, 'node_edge' if d >= 3 else 'node')
	set_(nx, ny, 'node_core')
	for x, y in ((nx, ny - 4), (nx, ny + 4), (nx - 4, ny), (nx + 4, ny), (nx + 3, ny - 3), (nx - 3, ny + 3), (nx + 3, ny + 3)):
		set_(x, y, 'node_glow')
	return role


def write_png(path, rows, color):
	"""color=False: 8-bit grayscale rows. color=True: RGBA tuples."""
	w, h = len(rows[0]), len(rows)
	if color:
		raw = b''.join(b'\x00' + b''.join(bytes(p) for p in r) for r in rows)
		ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
	else:
		raw = b''.join(b'\x00' + bytes(r) for r in rows)
		ihdr = struct.pack('>IIBBBBB', w, h, 8, 0, 0, 0, 0)
	chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d))
	with open(path, 'wb') as f:
		f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


def main():
	src = sys.argv[1] if len(sys.argv) > 1 else 'gfx/rooster_src'
	role = draw()
	name = '150_lab_bred_goose.png'
	grey = [[ROLES[r][0] for r in row] for row in role]
	colour = [[ROLES[r][1] + (255,) if ROLES[r][1] else (0, 0, 0, 0) for r in row] for row in role]
	x4 = [[p for p in row for _ in range(4)] for row in colour for _ in range(4)]
	for sub, rows, is_colour in (('gameboy', grey, False), ('colour', colour, True), ('colour_x4', x4, True)):
		os.makedirs(os.path.join(src, sub), exist_ok=True)
		write_png(os.path.join(src, sub, name), rows, is_colour)
		print(os.path.join(src, sub, name))


if __name__ == '__main__':
	main()
