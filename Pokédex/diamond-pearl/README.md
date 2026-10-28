# Diamond / Pearl — Sinnoh Pokédex

151 e-ink plates in **original Diamond/Pearl Sinnoh order**, from Turtwig to
Manaphy. This is the original regional roster, rather than Platinum's expanded
210-entry roster or the 493-entry National Pokédex.

![Six sample plates](preview.png)

Each plate includes the original Diamond/Pearl pixel sprite, both regional and
National numbers, category, Gen IV typing and base stats, height, weight, catch
rate, and separate English Diamond and Pearl descriptions. The sprite is scaled
by an integer with nearest-neighbor sampling. No smoothing or dithering is applied
to the sprite pixels. The white background and simple rules keep the plate clear
on small monochrome displays. The retro Pokédex shell echoes the original Kanto
set with a lens and status lamps, a recessed sprite screen, rounded double-line
windows, offset shadows, and a Game Boy-style dialogue frame.

## Ready-to-use files

| Folder | Native size | Format |
| --- | --- | --- |
| [x4](x4) | 480 × 800 | Native four-grey, 4-bit BMP |
| [x3](x3) | 528 × 792 | Native four-grey, 4-bit BMP |
| [reterminal-sticky](reterminal-sticky) | 480 × 800 | Four-grey PNG |
| [kindle-6in](kindle-6in) | 600 × 800 | Greyscale PNG |
| [kindle-pw2](kindle-pw2) | 758 × 1024 | Greyscale PNG |
| [kindle-pw3](kindle-pw3) | 1072 × 1448 | Greyscale PNG |
| [kindle-pw](kindle-pw) | 1236 × 1648 | Greyscale PNG |
| [kindle-oasis-pw12](kindle-oasis-pw12) | 1264 × 1680 | Greyscale PNG |
| [kindle-scribe](kindle-scribe) | 1860 × 2480 | Greyscale PNG |

Filenames begin with the **Sinnoh** number: `001-turtwig.bmp` is National #387.
The X4 BMPs also work for the upright reTerminal Sticky's BMP reader firmware.
Installation follows the device instructions in the [main README](../../README.md#installing-on-the-device).
These exports have been checked in software; physical device appearance is not
yet verified. The larger panels use the same information layout, with text and
rules drawn at native resolution and sprites enlarged in whole-pixel steps.

## Rebuild offline

From the repository root, with Python 3.10+ and Pillow installed:

```sh
python3 -m pip install -r 'Pokédex/diamond-pearl/requirements.txt'
python3 'Pokédex/diamond-pearl/render.py'
python3 'Pokédex/diamond-pearl/verify.py'
```

To render only selected devices or regional entries:

```sh
python3 'Pokédex/diamond-pearl/render.py' --devices x4 x3 --numbers 1 4 7
```

`data.json`, the source sprites, and both fonts are stored locally, so rendering
needs no network and uses no system fonts. To refresh source data (requires curl
and internet access), run `python3 'Pokédex/diamond-pearl/fetch.py'`.
The fetcher uses `past_types` and `past_stats` to restore Gen IV values where
PokéAPI records a subsequent change. Hidden abilities and modern experience yields
are omitted. Only the default form and default front sprite are used.

## Sources and attribution

- Data: [PokéAPI v2](https://pokeapi.co/docs/v2),
  [`original-sinnoh`](https://pokeapi.co/api/v2/pokedex/original-sinnoh/).
- Sprites: [PokéAPI's Diamond/Pearl sprite archive](https://github.com/PokeAPI/sprites/tree/master/sprites/pokemon/versions/generation-iv/diamond-pearl).
  These are the original **colour** 80 × 80 game sprites, converted to greyscale
  for these plates; they are not a separately drawn black-and-white sprite set.
  `data.json` records the exact sprite URL for each entry.
- [Silkscreen](https://github.com/google/fonts/tree/main/ofl/silkscreen) by Jason
  Kottke and [Share Tech Mono](https://github.com/google/fonts/tree/main/ofl/sharetechmono)
  by Carrois Type Design, both SIL Open Font License 1.1. Fonts and license texts
  are bundled in `assets/fonts`.

Pokémon, character names, game sprites, and game descriptions remain the property
of their respective rights holders, including Nintendo, Game Freak, and Creatures.
This is an unofficial, non-commercial fan project. The fonts' OFL does not apply
to the Pokémon artwork or text.
