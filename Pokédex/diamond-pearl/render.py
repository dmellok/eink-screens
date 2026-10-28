#!/usr/bin/env python3
"""Render offline Gen IV plates. Requires Pillow; no network used."""
import argparse
import json
from pathlib import Path
import struct

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
DEVICES = {
    'x4': (480, 800, 'bmp'), 'x3': (528, 792, 'bmp'),
    'reterminal-sticky': (480, 800, 'png4'),
    'kindle-6in': (600, 800, 'png'), 'kindle-pw2': (758, 1024, 'png'),
    'kindle-pw3': (1072, 1448, 'png'), 'kindle-pw': (1236, 1648, 'png'),
    'kindle-oasis-pw12': (1264, 1680, 'png'), 'kindle-scribe': (1860, 2480, 'png'),
}
STAT_NAMES = [('hp', 'HP'), ('attack', 'ATTACK'), ('defense', 'DEFENSE'),
              ('special-attack', 'SP. ATK'), ('special-defense', 'SP. DEF'), ('speed', 'SPEED')]


def bmp4(image, path):
    """Native 4-bpp, top-down BMP with exactly the four panel states."""
    width, height = image.size
    stride = ((width + 1) // 2 + 3) & ~3
    pixels = image.tobytes()
    body = bytearray()
    for y in range(height):
        row = pixels[y * width:(y + 1) * width]
        packed = bytearray((row[x] // 85) << 4 | (row[x + 1] // 85 if x + 1 < width else 0)
                           for x in range(0, width, 2))
        body.extend(packed + bytes(stride - len(packed)))
    offset = 14 + 40 + 16
    header = struct.pack('<2sIHHI', b'BM', offset + len(body), 0, 0, offset)
    info = struct.pack('<IiiHHIIiiII', 40, width, -height, 1, 4, 0, len(body), 2835, 2835, 4, 4)
    palette = b''.join(bytes([v, v, v, 0]) for v in (0, 85, 170, 255))
    path.write_bytes(header + info + palette + body)


def render(p, width, height, four=False):
    # Draw text and rules at native resolution; sprites always use integer zoom.
    scale = min(width / 480, height / 800)
    left = (width - 480 * scale) / 2
    top = (height - 800 * scale) / 2
    im = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(im)

    def xy(x, y):
        return round(left + x * scale), round(top + y * scale)

    def font(size, pixel=False):
        name = 'Silkscreen-Regular.ttf' if pixel else 'ShareTechMono-Regular.ttf'
        return ImageFont.truetype(str(ROOT / 'assets/fonts' / name), round(size * scale))

    def text(x, y, content, size=16, pixel=False, fill=0, anchor='lt'):
        draw.text(xy(x, y), content, font=font(size, pixel), fill=fill, anchor=anchor)

    def box(x, y, w, h, fill=None, outline=0, line=1, radius=0):
        bounds = [xy(x, y), xy(x + w, y + h)]
        draw.rounded_rectangle(bounds, radius=round(radius * scale), fill=fill, outline=outline,
                               width=max(1, round(line * scale)))

    def rule(y, x=24, end=456, fill=0):
        draw.line([xy(x, y), xy(end, y)], fill=fill, width=max(1, round(scale)))

    def paragraph(content, x, y, maxwidth, maxheight, size=18):
        for pts in range(size, 13, -1):
            f = font(pts)
            lines, current = [], ''
            for word in content.split():
                trial = f'{current} {word}'.strip()
                if draw.textlength(trial, font=f) > maxwidth * scale:
                    lines.append(current)
                    current = word
                else:
                    current = trial
            lines.append(current)
            if len(lines) * (pts + 3) <= maxheight:
                for row, line in enumerate(lines):
                    text(x, y + row * (pts + 3), line, pts)
                return
        raise ValueError(f'Text does not fit: {p["name"]}: {content}')

    def circle(x, y, diameter, fill, outline=0, line=1):
        draw.ellipse([xy(x, y), xy(x + diameter, y + diameter)], fill=fill,
                     outline=outline, width=max(1, round(line * scale)))

    def panel(x, y, w, h, radius=7):
        # Offset black edge and inner keyline recall the handheld game's windows.
        box(x + 3, y + 3, w, h, fill=0, radius=radius)
        box(x, y, w, h, fill=255, line=2, radius=radius)
        box(x + 4, y + 4, w - 8, h - 8, outline=170, radius=max(1, radius - 3))

    # Pokédex hardware: lens, status lamps, stepped seam and recessed LCD.
    box(8, 8, 464, 784, fill=255, line=2, radius=14)
    circle(22, 20, 44, 255, line=2)
    circle(28, 26, 32, 0)
    circle(33, 30, 11, 255, outline=255)
    circle(49, 47, 4, 170, outline=170)
    for i, shade in enumerate((0, 170, 255)):
        circle(78 + i * 17, 24, 9, shade)
    text(451, 22, 'POKEDEX', 24, True, anchor='rt')
    text(451, 49, 'SINNOH / DIAMOND + PEARL', 11, True, anchor='rt')
    draw.line([xy(9, 69), xy(113, 69), xy(126, 62), xy(167, 62)],
              fill=0, width=max(1, round(2 * scale)))
    box(22, 78, 436, 306, fill=85, outline=0, line=2, radius=12)
    box(29, 85, 422, 278, fill=255, outline=0, line=2, radius=7)
    box(34, 90, 412, 268, outline=170, radius=4)
    text(43, 98, f'No. {p["sinnoh"]:03}', 16, True)
    text(437, 100, f'NAT. {p["national"]:03}', 13, True, anchor='rt')
    circle(38, 371, 6, 255, outline=255)
    for i in range(4):
        box(364 + i * 19, 373, 14, 2, fill=255, outline=255)

    sprite = Image.open(ROOT / 'assets/sprites' / f'{p["national"]:03}.png').convert('RGBA')
    sprite = sprite.crop(sprite.getbbox())
    # Maximize within the display while preserving the original sprite grid.
    zoom = max(1, int(min(340 * scale / sprite.width, 178 * scale / sprite.height)))
    sprite = sprite.resize((sprite.width * zoom, sprite.height * zoom), Image.Resampling.NEAREST)
    white = Image.new('RGBA', sprite.size, 'white')
    white.alpha_composite(sprite)
    grey = white.convert('L')
    if four:
        # Nearest-neighbor scaling preserves flat clusters; no diffusion noise.
        grey = grey.point(lambda v: round(v / 85) * 85)
    cx, cy = xy(240, 210)
    im.paste(grey, (cx - grey.width // 2, cy - grey.height // 2))
    name_size = 28
    while draw.textlength(p['name'].upper(), font=font(name_size, True)) > 394 * scale:
        name_size -= 1
    text(240, 307, p['name'].upper(), name_size, True, anchor='mt')
    text(240, 340, p['genus'], 17, anchor='mt')
    types = p['types']
    badge_width = 112
    start = 240 - (len(types) * badge_width + (len(types) - 1) * 8) / 2
    for i, kind in enumerate(types):
        x = start + i * 120
        box(x + 2, 394, badge_width, 25, fill=170, outline=170, radius=5)
        box(x, 392, badge_width, 25, fill=0, radius=5)
        text(x + badge_width / 2, 398, kind.upper(), 13, True, 255, 'mt')

    panel(22, 430, 436, 133)
    text(34, 441, 'BASE STATS', 14, True)
    text(444, 441, f'TOTAL {sum(p["stats"][k] for k, _ in STAT_NAMES)}', 14, True, anchor='rt')
    rule(460, 34, 446)
    for i, (key, label) in enumerate(STAT_NAMES):
        y = 468 + 14 * i
        val = p['stats'][key]
        text(34, y, label, 12)
        for seg in range(15):
            box(120 + seg * 18, y + 2, 14, 7,
                fill=0 if seg < round(val / 255 * 15) else 255)
        text(444, y - 1, str(val), 14, anchor='rt')

    for i, (label, value) in enumerate((('HEIGHT', f'{p["height"]:g} m'),
                                        ('WEIGHT', f'{p["weight"]:g} kg'),
                                        ('CATCH', str(p['catch_rate'])))):
        x = 22 + 148 * i
        panel(x, 575, 140, 49, radius=6)
        text(x + 70, 583, label, 11, True, anchor='mt')
        text(x + 70, 600, value, 19, anchor='mt')

    panel(22, 637, 436, 128)
    # A white-backed legend interrupts the border like a Game Boy dialogue box.
    box(33, 631, 132, 14, fill=255, outline=255)
    text(38, 632, 'DEX ENTRIES', 12, True)
    for version, y, mark in (('diamond', 650, 'D'), ('pearl', 706, 'P')):
        box(34, y, 21, 21, fill=0, radius=4)
        text(44.5, y + 4, mark, 13, True, 255, 'mt')
        paragraph(p['text'][version], 64, y, 378, 51, 17)
    # Small navigation chevron is a game UI detail, outside the description area.
    draw.polygon([xy(438, 756), xy(444, 756), xy(441, 760)], fill=0)
    text(24, 777, 'GEN IV / 2006', 10, True)
    text(456, 777, f'SINNOH {p["sinnoh"]:03} / 151', 10, True, anchor='rt')
    if four:
        # Antialiased text also lands on exact native panel states.
        im = im.point(lambda v: round(v / 85) * 85)
    return im


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--devices', nargs='+', choices=DEVICES, default=list(DEVICES))
    parser.add_argument('--numbers', nargs='+', type=int, help='Sinnoh numbers, default all 151')
    args = parser.parse_args()
    entries = json.loads((ROOT / 'data.json').read_text())
    for device in args.devices:
        w, h, fmt = DEVICES[device]
        folder = ROOT / device
        folder.mkdir(exist_ok=True)
        for p in entries:
            if args.numbers and p['sinnoh'] not in args.numbers:
                continue
            plate = render(p, w, h, fmt in ('bmp', 'png4'))
            path = folder / f'{p["sinnoh"]:03}-{p["slug"]}.{"bmp" if fmt == "bmp" else "png"}'
            if fmt == 'bmp':
                bmp4(plate, path)
            else:
                plate.save(path, optimize=True)
        print(f'Rendered {device}: {w} x {h}', flush=True)
    # Preview uses the actual X4 rendering, including four-level quantization.
    picks = [1, 4, 7, 66, 149, 150]
    preview = Image.new('RGB', (480 * 3 + 24 * 4, 800 * 2 + 24 * 3), '#dedede')
    for i, number in enumerate(picks):
        preview.paste(render(entries[number - 1], 480, 800, True),
                      (24 + (i % 3) * 504, 24 + (i // 3) * 824))
    preview.save(ROOT / 'preview.png', optimize=True)


if __name__ == '__main__':
    main()
