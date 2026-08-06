# xteink-screens

Sleep-screen wallpapers for the **Xteink X3** and **Xteink X4** e-readers, pre-dithered for
CrossPoint / CrossInk firmware so grayscale shading renders correctly on the panel instead of
blowing out to white.

## What's here

| Folder | Contents |
| --- | --- |
| [`Pokédex/x4`](Pokédex/x4) | All 151 original Kanto Pokémon as 480×800 data-sheet screens for the X4 |
| [`Pokédex/x3`](Pokédex/x3) | The same 151 screens at 528×792 for the X3 |

<p align="center">
  <img src="Pokédex/preview-x4.png" width="300" alt="X4 preview" />
  <img src="Pokédex/preview-x3.png" width="330" alt="X3 preview" />
</p>

> The BMPs look washed-out in a desktop image viewer — that is intentional. The panel's four
> ink states display far darker than their nominal palette values (perceived ≈15/30/80/210 vs
> 0/85/170/255), so the files pre-brighten to compensate, matching the quantization used by
> [crosspoint-pxc-converter](https://github.com/zgredex/crosspoint-pxc-converter) and the
> firmware's own dither path. Judge them on the device, not in Preview.

## Downloading a folder as a zip

GitHub can't zip a single folder from the web UI, so either:

1. **Releases (easiest):** grab `pokedex-x4.zip` or `pokedex-x3.zip` from the
   [latest release](../../releases/latest) — these are pre-zipped copies of each folder.
2. **download-directory:** paste a folder URL into <https://download-directory.github.io>, or use
   these direct links:
   - [Download Pokédex/x4 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Fxteink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fx4)
   - [Download Pokédex/x3 as zip](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fdmellok%2Fxteink-screens%2Ftree%2Fmain%2FPok%C3%A9dex%2Fx3)
3. **Whole repo:** Code → Download ZIP (includes both folders).

## Installing on the device

1. Copy the `.bmp` files you want onto the device (USB mass storage).
2. On the device, open a file in **Browse Files** — the built-in BMP viewer displays it.
3. Choose **set as sleep screen cover** from the viewer.

Files are 4-bit indexed BMPs (four-gray palette, top-down rows) — the exact layout the stock
BMP loader expects; no further conversion needed.

## Format details

- X4: 480×800 · X3: 528×792, both portrait
- 4 bpp indexed, palette `#000000 #555555 #AAAAAA #FFFFFF`, `biClrUsed=4`, negative-height (top-down) `BITMAPINFOHEADER`
- Floyd–Steinberg error diffusion, bin thresholds 30/50/140, error diffused against the panel's
  perceived levels 15/30/80/210 (CrossPoint `master` quantization profile)
- Rendered from a live [Tesserae](https://github.com/dmellok) canvas driven by
  [PokéAPI](https://pokeapi.co) data — sprites, stats, dex entries and habitats are the real
  Gen-I data set

Pokémon and Pokémon character names are trademarks of Nintendo. Sprite and dex data via PokéAPI;
this is a fan-made, non-commercial project.
