#!/usr/bin/env python3
"""Draw the edition line under the title logo for Rooster Edition.

Usage: tools/draw_rooster_version.py

Writes gfx/title/red_version.png ("Rhode Island Red") and
gfx/title/blue_version.png ("Blue Wyandotte"): 80x8 one-bit strips (10 tiles),
centred, in the same small bold font as the original "Red Version" text.
Capitals are 5 pixels tall (rows 2-6), lower case 4, and y drops to row 7.
Run `make` afterwards.
"""

from PIL import Image

GLYPHS = {
	# six rows each: row 2 (cap/ascender) to row 7 (descender)
	'R': ['####.', '##.##', '####.', '##.##', '##.##', '.....'],
	'B': ['####.', '##.##', '####.', '##.##', '####.', '.....'],
	'I': ['####', '.##.', '.##.', '.##.', '####', '....'],
	'W': ['##...##', '##...##', '##.#.##', '##.#.##', '.##.##.', '.......'],
	'a': ['....', '###.', '..##', '.###', '####', '....'],
	'd': ['..##', '..##', '.###', '##.#', '.###', '....'],
	'e': ['....', '.###', '##.#', '###.', '.###', '....'],
	'h': ['##..', '##..', '###.', '##.#', '##.#', '....'],
	'l': ['##', '##', '##', '##', '##', '..'],
	'n': ['....', '###.', '##.#', '##.#', '##.#', '....'],
	'o': ['.....', '.###.', '##.##', '##.##', '.###.', '.....'],
	's': ['....', '.###', '###.', '..##', '###.', '....'],
	't': ['.##.', '####', '.##.', '.##.', '..##', '....'],
	'u': ['....', '##.#', '##.#', '##.#', '.###', '....'],
	'y': ['....', '##.#', '##.#', '.###', '...#', '.##.'],
	' ': ['....', '....', '....', '....', '....', '....'],
}
W, H = 80, 8


def render(text):
	cols = []
	for i, ch in enumerate(text):
		g = GLYPHS[ch]
		if i and ch != ' ' and text[i - 1] != ' ':
			cols.append('.' * 6)  # one pixel between letters
		cols.extend(''.join(row[x] for row in g) for x in range(len(g[0])))
	assert len(cols) <= W, f'{text!r} is {len(cols)} pixels wide, only {W} fit'
	img = Image.new('1', (W, H), 1)
	x0 = (W - len(cols)) // 2
	for x, col in enumerate(cols):
		for r, v in enumerate(col):
			if v == '#':
				img.putpixel((x0 + x, 2 + r), 0)
	return img


def main():
	for name, text in (('red', 'Rhode Island Red'), ('blue', 'Blue Wyandotte')):
		path = f'gfx/title/{name}_version.png'
		render(text).save(path)
		print('wrote', path)


if __name__ == '__main__':
	main()
