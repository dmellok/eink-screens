#!/usr/bin/env python3
"""Refresh the small, offline rendering dataset from PokéAPI and its sprite repo."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
API = 'https://pokeapi.co/api/v2/'
SPRITES = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/'


def download(url):
    for attempt in range(4):
        try:
            return subprocess.check_output(['curl', '--silent', '--show-error', '--fail',
                                            '--location', '--max-time', '45', url])
        except Exception:
            if attempt == 3:
                raise
            time.sleep(attempt + 1)


def resource(path):
    return json.loads(download(API + path))


def generation(item):
    return int(item['generation']['url'].rstrip('/').split('/')[-1])


def historical(current, history, field):
    # Each record describes values through its last generation. Apply newest
    # first so the earliest record still applicable to Gen IV wins.
    for old in sorted(history, key=generation, reverse=True):
        if generation(old) >= 4:
            current = old[field]
    return current


def entry(item):
    species = resource('pokemon-species/' + item['pokemon_species']['name'] + '/')
    pokemon_url = next(v['pokemon']['url'] for v in species['varieties'] if v['is_default'])
    pokemon = json.loads(download(pokemon_url))
    number = species['id']
    sprite = ROOT / 'assets' / 'sprites' / f'{number:03}.png'
    if not sprite.exists():
        sprite.write_bytes(download(SPRITES + f'{number}.png'))
    stats = {s['stat']['name']: s['base_stat'] for s in pokemon['stats']}
    for old in sorted(pokemon.get('past_stats', []), key=generation, reverse=True):
        if generation(old) >= 4:
            stats.update({s['stat']['name']: s['base_stat'] for s in old['stats']})
    text = {}
    for version in ('diamond', 'pearl'):
        text[version] = ' '.join(next(t['flavor_text'] for t in species['flavor_text_entries']
                                     if t['language']['name'] == 'en' and t['version']['name'] == version).split())
    return dict(sinnoh=item['entry_number'], national=number, slug=species['name'],
                name=next(n['name'] for n in species['names'] if n['language']['name'] == 'en'),
                genus=next(g['genus'] for g in species['genera'] if g['language']['name'] == 'en'),
                height=pokemon['height'] / 10, weight=pokemon['weight'] / 10,
                catch_rate=species['capture_rate'], stats=stats, text=text,
                types=[t['type']['name'] for t in historical(pokemon['types'], pokemon['past_types'], 'types')],
                sprite_source=SPRITES + f'{number}.png')


def main():
    (ROOT / 'assets' / 'sprites').mkdir(parents=True, exist_ok=True)
    dex = resource('pokedex/original-sinnoh/')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        entries = list(pool.map(entry, dex['pokemon_entries']))
    entries.sort(key=lambda p: p['sinnoh'])
    assert len(entries) == 151
    (ROOT / 'data.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n')
    print(f'Cached {len(entries)} original Sinnoh entries and Diamond/Pearl sprites.')


if __name__ == '__main__':
    main()
