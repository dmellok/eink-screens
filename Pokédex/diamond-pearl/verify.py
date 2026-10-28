#!/usr/bin/env python3
"""Check the complete roster, historical data, and every exported image."""
import json
import struct

from PIL import Image

from render import ROOT, DEVICES


def main():
    entries = json.loads((ROOT / 'data.json').read_text())
    assert [p['sinnoh'] for p in entries] == list(range(1, 152))
    assert len({p['national'] for p in entries}) == 151
    by_id = {p['national']: p for p in entries}
    # Guard against silently using modern types or post-Gen-IV stat buffs.
    assert by_id[35]['types'] == ['normal']  # Clefairy became Fairy in Gen VI.
    assert by_id[122]['types'] == ['psychic']
    assert by_id[25]['stats']['defense'] == 30
    assert by_id[25]['stats']['special-defense'] == 40
    assert by_id[395]['stats']['attack'] == 86  # Empoleon's later stat change.
    for p in entries:
        assert p['text']['diamond'] and p['text']['pearl']
        with Image.open(ROOT / 'assets/sprites' / f'{p["national"]:03}.png') as sprite:
            assert sprite.size == (80, 80)
    total = 0
    for device, (width, height, fmt) in DEVICES.items():
        folder = ROOT / device
        suffix = '.bmp' if fmt == 'bmp' else '.png'
        assert len(list(folder.glob('*' + suffix))) == 151, device
        for p in entries:
            path = folder / f'{p["sinnoh"]:03}-{p["slug"]}{suffix}'
            with Image.open(path) as image:
                image.load()
                assert image.size == (width, height), path
                if fmt in ('bmp', 'png4'):
                    assert {value for count, value in image.convert('L').getcolors(256)} <= {0, 85, 170, 255}, path
                else:
                    assert image.mode == 'L', path
            if fmt == 'bmp':
                raw = path.read_bytes()
                assert raw[:2] == b'BM'
                assert struct.unpack_from('<I', raw, 2)[0] == len(raw)
                assert struct.unpack_from('<I', raw, 10)[0] == 70
                assert struct.unpack_from('<ii', raw, 18) == (width, -height)
                assert struct.unpack_from('<H', raw, 28)[0] == 4
                assert struct.unpack_from('<I', raw, 46)[0] == 4
                assert raw[54:70] == b''.join(bytes([v, v, v, 0]) for v in (0, 85, 170, 255))
            total += 1
        print(f'PASS {device}: 151 files, native geometry and expected format', flush=True)
    print(f'PASS {total} plates, 151 source sprites, roster and historical data.')


if __name__ == '__main__':
    main()
