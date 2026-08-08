# eink-screens

Sleep-screen wallpapers for e-ink readers, rendered at each panel's native geometry.

## Devices

| Device | Panel | Format |
| --- | --- | --- |
| Xteink X4 | 480×800, 4-level grey | 4-bit BMP, dither baked in |
| Xteink X3 | 528×792, 4-level grey | 4-bit BMP, dither baked in |
| Kindle Paperwhite (11th gen) | 1236×1648, 16-level grey | 8-bit greyscale PNG |
| Kindle Oasis / Paperwhite (12th gen) | 1264×1680, 16-level grey | 8-bit greyscale PNG |
| Kindle Paperwhite (1st/2nd gen) | 758×1024, 16-level grey | 8-bit greyscale PNG |
| Kindle (basic, 6") and similar | 600×800, 16-level grey | 8-bit greyscale PNG |
| Kobo Libra Colour | 1264×1680, Kaleido 3 colour | **colour** PNG |

The Xteink files are pre-dithered because CrossInk/CrossPoint maps a BMP whose palette is exactly
the four native grey levels (`#000/#555/#AAA/#FFF`) **1:1 to panel states** — no re-quantization,
no dithering (`Bitmap.cpp` nativePalette path). Plain greyscale BMPs instead get hard-thresholded
at 45/70/140 with no error diffusion, which blows highlights out to white. The Kindle files are
*not* pre-dithered: that panel has 16 levels and renders greyscale PNGs perfectly well on its own.

## What's here

| Folder | Contents |
| --- | --- |
| [`Pokédex/x4`](Pokédex/x4) | All 151 original Kanto Pokémon as 480×800 data-sheet screens for the X4 |
| [`Pokédex/x3`](Pokédex/x3) | The same 151 screens at 528×792 for the X3 |
| [`Pokédex/kindle-pw`](Pokédex/kindle-pw) | The same 151 at 1236×1648, expanded for the Paperwhite (see below) |
| [`Pokédex/kindle-oasis-pw12`](Pokédex/kindle-oasis-pw12) | The same expanded layout at 1264×1680 (Oasis, 12th-gen Paperwhite) |
| [`Pokédex/kindle-pw2`](Pokédex/kindle-pw2) | The same expanded layout at 758×1024 (1st/2nd-gen Paperwhite) |
| [`Pokédex/kobo-libra-colour`](Pokédex/kobo-libra-colour) | 1264×1680 **in colour**, red Pokédex shell, for the Kobo Libra Colour |
| [`Pokédex/kindle-6in`](Pokédex/kindle-6in) | 600×800, reduced layout for small 6" panels (see below) |
| [`Constellations/x4`](Constellations/x4) | All 88 IAU constellations as 480×800 star-chart plates for the X4 |
| [`Constellations/x3`](Constellations/x3) | The same 88 plates at 528×792 for the X3 |
| [`Magic/x4`](Magic/x4) | 104 iconic Magic: The Gathering cards as 480×800 card facsimiles for the X4 |
| [`Magic/x3`](Magic/x3) | The same 104 cards at 528×792 for the X3 |
| [`SCP/x4`](SCP/x4) | Top 100 SCP Foundation articles as 480×800 file plates for the X4 |
| [`SCP/x3`](SCP/x3) | The same 100 plates at 528×792 for the X3 |

<p align="center">
  <img src="Pokédex/preview-x4.png" width="300" alt="X4 preview" />
  <img src="Pokédex/preview-x3.png" width="330" alt="X3 preview" />
</p>
<p align="center">
  <img src="Pokédex/preview-kindle-pw.png" width="640" alt="Kindle Paperwhite Pokédex plates" />
</p>
<p align="center">
  <img src="Pokédex/preview-kobo-libra-colour.png" width="640" alt="Kobo Libra Colour Pokédex plates" />
</p>
<p align="center">
  <img src="Constellations/preview-x4.png" width="640" alt="Constellation plates" />
</p>
<p align="center">
  <img src="Magic/preview-x4.png" width="640" alt="Magic card plates" />
</p>
<p align="center">
  <img src="SCP/preview-x4.png" width="640" alt="SCP file plates" />
</p>

### The Paperwhite Pokédex is a different layout

It is not the X3/X4 sheet upscaled. The Paperwhite has roughly 5× the pixels, so the extra room
carries extra data rather than larger type — the type is scaled about 2×, not 2.6×, because at
300 ppi a straight pixel-for-pixel scale would leave the glyphs physically enormous. Added over
the Xteink version: the evolution chain with sprites and conditions, the Red/Blue level-up
learnset, breeding data (egg groups, hatch cycles, gender ratio, EV yield), habitat, growth rate,
base friendship, and a computed type-matchup panel.

That matchup panel uses the **Generation I** type chart, not the modern one, to match the Kanto
roster and the Red/Blue learnset beside it. It is derived from PokéAPI's `past_damage_relations`
rather than transcribed, so Ghost deals 0 to Psychic, and Bug and Poison hit each other for 2×.

The same expanded layout is also rendered at 1264×1680 and 758×1024. **600×800 is different**:
that panel is too small to carry the dense panels legibly, so `kindle-6in` uses the compact
layout from the Xteink sets instead. It keeps the sprite, base stats, height/weight/experience/
catch rate and the dex entry, and drops the learnset, type matchup, breeding block and evolution
chain. Everything on it is readable at 167 ppi, which the shrunken full layout was not.

### The Kobo set is in colour

`kobo-libra-colour` is the only colour set here. The Libra Colour's Kaleido 3 panel renders
colour at 150 ppi but black and white at the full 300 ppi, and desaturates noticeably, so colour
is used on large blocks — the red Pokédex shell, type badges in their official type colours, stat
bars in the primary type colour, and matchup chips coded red for weaknesses, green for
resistances and grey for immunity. Body text stays black on white, where the panel keeps it
crisp. Sprites are full colour rather than the greyscale treatment the mono sets use.

## Downloading a folder as a zip

GitHub can't zip a single folder from the web UI, so either:

1. **Releases (easiest):** every set is pre-zipped on the [releases page](../../releases).
   The Pokédex lives in one place, [Pokédex v2.0](../../releases/tag/pokedex-v2.0), with a zip
   per panel size; the other sets have a release each
   (`constellations-*`, `magic-*`, `scp-*`).
2. **download-directory:** paste a folder URL into <https://download-directory.github.io>, or use
   these direct links:
   - [Download Pokédex/x4 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fx4)
   - [Download Pokédex/x3 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fx3)
   - [Download Pokédex/kindle-pw as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fkindle-pw)
   - [Download Pokédex/kindle-oasis-pw12 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fkindle-oasis-pw12)
   - [Download Pokédex/kindle-pw2 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fkindle-pw2)
   - [Download Pokédex/kindle-6in as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fkindle-6in)
   - [Download Pokédex/kobo-libra-colour as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fkobo-libra-colour)
   - [Download Constellations/x4 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FConstellations%2Fx4)
   - [Download Constellations/x3 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FConstellations%2Fx3)
   - [Download Magic/x4 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FMagic%2Fx4)
   - [Download Magic/x3 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FMagic%2Fx3)
   - [Download SCP/x4 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FSCP%2Fx4)
   - [Download SCP/x3 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Feink-screens%2Ftree%2Fmain%2FSCP%2Fx3)
3. **Whole repo:** Code → Download ZIP (includes every folder).

## Installing on the device

### Xteink X3 / X4

1. Copy the `.bmp` files you want onto the device (USB mass storage).
2. On the device, open a file in **Browse Files** — the built-in BMP viewer displays it.
3. Choose **set as sleep screen cover** from the viewer.

Files are 4-bit indexed BMPs (four-gray palette, top-down rows) — the exact layout the stock
BMP loader expects; no further conversion needed.

### Kindle Paperwhite

Replacing the Kindle's sleep screen requires a **jailbroken** device — there is no stock way to
set a custom screensaver. With a jailbreak and a screensaver hack installed, copy the `.png`
files into the hack's screensaver folder.

On a stock Kindle these still work as ordinary images: side-load them into `documents/`, or bind
them into a PDF or CBZ and page through the set. They just won't become the lockscreen.

### KOReader (Kobo, Kindle, and others)

KOReader can show a random image from a folder as its sleep screen, which is the easiest way to
use these. Copy the PNGs to the device, then set **gear icon → Screen → Sleep screen** (called
*Screensaver* on older builds) to show a random image from a folder, and point it at that folder.

## Test cards

[`test-cards/`](test-cards) holds diagnostic BMPs for verifying the firmware's 4-level grayscale
sleep-screen pipeline: the top half is four solid vertical bands, one per native gray level
(palette-native 4-bit files, so the firmware maps them 1:1 with no dithering). A healthy unit
shows four distinct bands; if the two middle bands render black (or the panel wipes to white),
the multi-pass grayscale refresh is not running correctly — see
[crosspoint-reader#2879](https://github.com/crosspoint-reader/crosspoint-reader/issues/2879).

## Format details

### Xteink (BMP)

- X4: 480×800 · X3: 528×792, both portrait
- 4 bpp indexed, palette `#000000 #555555 #AAAAAA #FFFFFF`, `biClrUsed=4`, negative-height (top-down) `BITMAPINFOHEADER`
- Floyd–Steinberg error diffusion against the **nominal** levels 0/85/170/255 (thresholds
  43/128/213). Because the palette is native, the firmware maps each index straight to a panel
  state and its gray composite renders the two middle states at their proper visible levels —
  so no midtone pre-brightening is wanted. (An earlier revision of this file described
  pre-compensated levels 10/49/111/225; that approach blew out highlights and was dropped in
  331b60b, but the note was left behind. The committed BMPs have always used the nominal ramp.)

### Kindle Paperwhite (PNG)

- 1236×1648 (Paperwhite 11th gen), 1264×1680 (Oasis, Paperwhite 12th gen, Kobo Libra Colour),
  758×1024 (Paperwhite 1st/2nd gen) and 600×800 (basic 6" panels), all portrait.
- 8-bit greyscale PNG, no dithering applied — these panels have 16 levels and handle greyscale
  themselves. The Kobo Libra Colour set is RGB PNG.

Both are rendered from live [Tesserae](https://github.com/dmellok) canvases.

### Sources

- **Pokédex** — [PokéAPI](https://pokeapi.co): sprites, base stats, dex entries and habitats are
  the real Gen-I data set. Pokémon and Pokémon character names are trademarks of Nintendo; this is
  a fan-made, non-commercial project.
- **Constellations** — stars from the [HYG database](https://github.com/astronexus/HYG-Database)
  v4.1 (CC BY-SA) filtered to magnitude ≤6.5, Messier objects from its deep-sky companion
  catalogue, and stick figures plus IAU boundaries from
  [d3-celestial](https://github.com/ofrohn/d3-celestial) (BSD-3). Areas, culmination months and
  visibility limits are computed from that geometry, not copied — the spherical-polygon areas
  agree with the published IAU values (Orion 594.1, Crux 68.5, Hydra 1302.5 deg²).
- **Magic** — card data, art crops, set symbols and mana symbols from the
  [Scryfall API](https://scryfall.com/docs/api) (card data is CC0; card images and artwork remain
  © Wizards of the Coast and their respective artists). Each card is pinned to a specific
  printing so the original art is used — Christopher Rush's Black Lotus rather than a modern
  reprint. Every plate credits its illustrator. Magic: The Gathering is a trademark of Wizards of
  the Coast LLC; this is a fan-made, non-commercial project and is not affiliated with or
  endorsed by Wizards of the Coast or Scryfall.
- **SCP** — articles from the [SCP Wiki](https://scp-wiki.wikidot.com), all **CC BY-SA 3.0**.
  Ranking, tags and article text come from the [scp-data](https://scp-data.tedivm.com) dump;
  titles are scraped from the wiki's series indexes. Because the source is share-alike, the
  plates in [`SCP/`](SCP) are **also CC BY-SA 3.0** — see
  [`SCP/ATTRIBUTION.md`](SCP/ATTRIBUTION.md) for the full author list, per-image licences and
  the content exclusions. The Foundation emblem is from
  [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:SCP_Foundation_(emblem).svg)
  (CC BY-SA); the property icons are [Phosphor](https://phosphoricons.com) (MIT).

### What's on an SCP plate

Item number, object class with a Safe→Apollyon containment scale, up to four property icons
derived from the article's own wiki tags, a photographic record where one is available under an
open licence, and an extract from the containment procedures and description. Author and licence
are credited on every plate.

Redaction on the extract is **applied by this project, not copied from the source** — roughly
one word in ten, weighted toward figures, sites and proper nouns. Genuine `█` runs written by
article authors are preserved separately.

The set is the top 100 by community rating, with six entries skipped on content grounds and
backfilled from below the cut; the exclusions and reasons are listed in the attribution file.

### What's on a Magic plate

A facsimile of the card itself, proportioned for the panel: title bar with mana cost, art window,
type line with the set symbol, rules text box with reminder text italicised, and the illustrator
credit, set code and plate number along the bottom. Power/toughness or starting loyalty sits in
the corner box where the real card puts it.

Colour identity is carried by the **shape** of each mana symbol rather than its tone — five
colours don't fit into four grey levels, so the flame, droplet, skull, sun and tree glyphs do the
distinguishing, with the disc behind them shaded only light-to-dark. Rules text is auto-fitted per
card, since a Black Lotus and an Urza's Saga differ by a factor of sixty in word count.

### What's on a constellation plate

Stereographic projection centred on the constellation, north up and east left. Stars are sized by
magnitude; Messier objects use the conventional symbols. The oval top-right is an all-sky Hammer
projection locating the constellation against the celestial equator (solid) and the ecliptic
(dashed). The globe bottom-right shades the band of Earth latitudes from which the entire figure
clears the horizon at some point in the year — nothing on these plates is tied to one observing
site.
