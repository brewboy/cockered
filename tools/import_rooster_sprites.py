#!/usr/bin/env python3
"""Import Rooster Edition sprites into gfx/pokemon/front and gfx/pokemon/back.

Usage: tools/import_rooster_sprites.py SPRITE_DIR

SPRITE_DIR holds 56x56 grayscale PNGs named NNN_<breed>.png (Pokédex order).
Front sprites are cropped to the smallest bottom-centred 40/48/56 square that
fits them. Back sprites are derived from the fronts: mirrored to face right and
shrunk to 32x32. Run from the repository root.
"""

import glob
import os
import re
import struct
import sys
import zlib

SKIP = {83}  # Farfetch'd keeps its original sprites
OVERRIDE = {150: '150_lab_bred_goose.png'}  # Mewtwo is the goose
SHADES = (0, 85, 170, 255)  # black, dark, light, white


def read_png(path):
	data = open(path, 'rb').read()
	assert data[:8] == b'\x89PNG\r\n\x1a\n', path
	pos, idat = 8, b''
	while pos < len(data):
		length, = struct.unpack('>I', data[pos:pos + 4])
		kind, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + length]
		if kind == b'IHDR':
			w, h, depth, color = struct.unpack('>IIBB', body[:10])
			assert (depth, color) == (8, 0), f'{path}: expected 8-bit grayscale'
		elif kind == b'IDAT':
			idat += body
		pos += 12 + length
	raw, rows, prev = zlib.decompress(idat), [], [0] * w
	for y in range(h):
		f, line = raw[y * (w + 1)], list(raw[y * (w + 1) + 1:(y + 1) * (w + 1)])
		for x in range(w):
			a = line[x - 1] if x else 0
			b, c = prev[x], prev[x - 1] if x else 0
			if f == 1: line[x] = (line[x] + a) & 255
			elif f == 2: line[x] = (line[x] + b) & 255
			elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
			elif f == 4:
				p = a + b - c
				pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
				line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
		rows.append(line)
		prev = line
	# quantize to the four Game Boy shades (0 = black .. 3 = white)
	return [[min(range(4), key=lambda i: abs(SHADES[i] - v)) for v in r] for r in rows]


def write_png(path, rows):
	"""Write a 2-bit grayscale PNG, matching the repository's sprite PNGs."""
	w, h = len(rows[0]), len(rows)
	raw = b''
	for r in rows:
		packed = bytearray()
		for i in range(0, w, 4):
			byte = 0
			for v in r[i:i + 4]:
				byte = byte << 2 | v
			packed.append(byte << 2 * (4 - len(r[i:i + 4])))
		raw += b'\x00' + bytes(packed)
	chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d))
	with open(path, 'wb') as f:
		f.write(b'\x89PNG\r\n\x1a\n')
		f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 2, 0, 0, 0, 0)))
		f.write(chunk(b'IDAT', zlib.compress(raw, 9)))
		f.write(chunk(b'IEND', b''))


def bbox(rows):
	pts = [(x, y) for y, r in enumerate(rows) for x, v in enumerate(r) if v != 3]
	xs, ys = [p[0] for p in pts], [p[1] for p in pts]
	return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def front(rows):
	n = len(rows)
	x0, y0, x1, y1 = bbox(rows)
	for s in (40, 48, 56):
		left, top = (n - s) // 2, n - s
		if x0 >= left and x1 <= left + s and y0 >= top:
			return [r[left:left + s] for r in rows[top:]]
	return rows


def back(rows, size=32):
	x0, y0, x1, y1 = bbox(rows)
	bw, bh = x1 - x0, y1 - y0
	scale = min(size / bw, size / bh, 1)
	tw, th = max(1, round(bw * scale)), max(1, round(bh * scale))
	ox, oy = (size - tw) // 2, size - th
	out = [[3] * size for _ in range(size)]
	for ty in range(th):
		for tx in range(tw):
			# area-weighted coverage of each shade in the source footprint
			sx0, sx1 = x0 + tx * bw / tw, x0 + (tx + 1) * bw / tw
			sy0, sy1 = y0 + ty * bh / th, y0 + (ty + 1) * bh / th
			weight = [0.0] * 4
			for sy in range(int(sy0), min(int(sy1 + 0.999), y1)):
				for sx in range(int(sx0), min(int(sx1 + 0.999), x1)):
					a = (min(sx + 1, sx1) - max(sx, sx0)) * (min(sy + 1, sy1) - max(sy, sy0))
					if a > 0:
						weight[rows[sy][sx]] += a
			total = sum(weight) or 1
			if weight[0] / total >= 0.4:
				v = 0  # keep outlines
			else:
				avg = sum(i * w for i, w in enumerate(weight)) / total
				v = min(3, max(0, round(avg)))
			# mirror so the bird faces right, towards the opponent
			out[oy + ty][ox + tw - 1 - tx] = v
	return out


def species_files():
	"""Front pic basenames in Pokédex order, from the base stats data."""
	includes = re.findall(r'INCLUDE "(data/pokemon/base_stats/\w+\.asm)"', open('data/pokemon/base_stats.asm').read())
	includes.append('data/pokemon/base_stats/mew.asm')
	names = []
	for inc in includes:
		m = re.search(r'INCBIN "gfx/pokemon/front/([\w.]+)\.pic"', open(inc).read())
		names.append(m.group(1))
	assert len(names) == 151, len(names)
	return names


def main():
	src = sys.argv[1]
	for dex, name in enumerate(species_files(), 1):
		if dex in SKIP:
			continue
		path = os.path.join(src, OVERRIDE[dex]) if dex in OVERRIDE else glob.glob(os.path.join(src, f'{dex:03}_*.png'))[0]
		rows = read_png(path)
		f = front(rows)
		write_png(f'gfx/pokemon/front/{name}.png', f)
		write_png(f'gfx/pokemon/back/{name}b.png', back(rows))
		print(f'{dex:03} {name:<12} front {len(f)}x{len(f)}  <- {os.path.basename(path)}')


if __name__ == '__main__':
	main()
