#!/usr/bin/env python3
"""Draw the title-screen logo for Rooster Edition: COCK in the old logo's style.

Usage: tools/draw_rooster_logo.py [OUT]

Chunky bouncing letters with a light grey fill, a thick black outline and a
dark grey drop shadow down and to the left, on white. Writes a 128x56 four-shade
PNG (16x7 tiles, the size the title screen expects); OUT defaults to
gfx/title/pokemon_logo.png. Run `make` afterwards.
"""

import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

W, H = 128, 56
S = 8  # supersampling for smooth curves
BLACK, DARK, LIGHT, WHITE = 0, 85, 170, 255
OUTLINE = 2
SHADOW = (-3, 3)


def rrect(d, box, r, fill):
	d.rounded_rectangle([v * S for v in box], radius=r * S, fill=fill)


def poly(d, pts, fill):
	d.polygon([(x * S, y * S) for x, y in pts], fill=fill)


def letter_c(d, x0, y0, x1, y1):
	"""A fat C: a rounded block with a round hole and its mouth cut out on the right."""
	w, h = x1 - x0, y1 - y0
	rrect(d, (x0, y0, x1, y1), min(w, h) * .45, 255)
	t = w * .29  # stroke thickness
	rrect(d, (x0 + t, y0 + t * .95, x1 - t * .55, y1 - t * .95), (w - t * 1.55) * .45, 0)
	cy = (y0 + y1) / 2
	poly(d, ((x0 + w * .5, cy - h * .07), (x1 + 1, cy - h * .24), (x1 + 1, cy + h * .24), (x0 + w * .5, cy + h * .07)), 0)


def letter_o(d, x0, y0, x1, y1):
	w, h = x1 - x0, y1 - y0
	rrect(d, (x0, y0, x1, y1), min(w, h) * .45, 255)
	t = w * .31
	rrect(d, (x0 + t, y0 + t * .9, x1 - t, y1 - t * .9), (w - 2 * t) * .5, 0)


def letter_k(d, x0, y0, x1, y1):
	w, h = x1 - x0, y1 - y0
	stem = w * .38
	rrect(d, (x0, y0, x0 + stem, y1), 3, 255)
	mid = y0 + h * .52
	# upper arm, leaning out to the top right
	poly(d, ((x0 + stem - 1, mid - h * .14), (x1 - w * .3, y0), (x1, y0 + h * .06), (x0 + stem + w * .12, mid + h * .1)), 255)
	# lower leg, kicking out to the bottom right
	poly(d, ((x0 + stem - 1, mid - h * .06), (x0 + stem + w * .22, mid - h * .2), (x1, y1 - h * .08), (x1 - w * .32, y1)), 255)


def draw():
	fill = Image.new('L', (W * S, H * S), 0)
	d = ImageDraw.Draw(fill)
	# a little bounce, like the old logo: big first letter, the rest bobbing
	letter_c(d, 5, 5, 37, 47)
	letter_o(d, 37, 13, 65, 47)
	letter_c(d, 65, 9, 93, 45)
	letter_k(d, 94, 4, 124, 46)
	fill = fill.resize((W, H), Image.LANCZOS).point(lambda v: 255 if v >= 128 else 0)

	outline = fill.filter(ImageFilter.MaxFilter(2 * OUTLINE + 1))
	shadow = ImageChops.offset(outline, *SHADOW)
	img = Image.new('L', (W, H), WHITE)
	img.paste(DARK, mask=shadow)
	img.paste(BLACK, mask=outline)
	img.paste(LIGHT, mask=fill)
	# inner shading: a dark rim along the bottom edge of each letter's fill
	below = ImageChops.offset(fill, 0, -1)
	rim = ImageChops.subtract(fill, below)
	img.paste(DARK, mask=rim)
	return img


def main():
	out = sys.argv[1] if len(sys.argv) > 1 else 'gfx/title/pokemon_logo.png'
	draw().save(out)
	print(f'wrote {out}')


if __name__ == '__main__':
	main()
