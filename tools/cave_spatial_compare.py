"""Compare air-adjacent ore sites by height and local tile in saved test worlds.

A tile is a spatial proxy, not a connected or player-accessible cave.
"""

import argparse
from collections import Counter
import json
from pathlib import Path

from tools.balance_batch import inspect_results, ratio
from tools.balance_followup import HEIGHT_BANDS, load_plan
from tools.vanilla_reference import DIRECTIONS, analyze, analyze_full_height


ROOT = Path(__file__).resolve().parents[1]


def compare_exposed_positions(vanilla, candidate):
    def positions(scan):
        return {(ore['x'], ore['y'], ore['z'])
                for ore in scan['ores'] + scan.get('upperDiamondOre', [])
                if 'minecraft:air' in ore['neighbours']}
    baseline = positions(vanilla)
    changed = positions(candidate)
    return {'vanilla': len(baseline), 'candidate': len(changed),
            'retained': len(baseline & changed), 'lost': len(baseline - changed),
            'added': len(changed - baseline)}


def measure_scan(scan, origin_x, origin_z, tile_size=64):
    if tile_size < 1:
        raise ValueError('tile size must be positive')
    ores = scan['ores'] + scan.get('upperDiamondOre', [])
    positions = {(ore['x'], ore['y'], ore['z']): ore for ore in ores}
    if len(positions) != len(ores):
        raise ValueError('duplicate ore position')
    remaining = set(positions)
    bands = {name: {'groups': 0, 'blocks': 0, 'tiles': Counter()}
             for name, _, _ in HEIGHT_BANDS}
    while remaining:
        stack = [remaining.pop()]
        group = []
        while stack:
            point = stack.pop()
            group.append(point)
            for direction in DIRECTIONS:
                neighbor = tuple(point[i] + direction[i] for i in range(3))
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    stack.append(neighbor)
        air = [point for point in group
               if 'minecraft:air' in positions[point]['neighbours']]
        for name, low, high in HEIGHT_BANDS:
            exposed = [point for point in air if low <= point[1] <= high]
            if not exposed:
                continue
            anchor = min(exposed, key=lambda point: (point[0], point[2], point[1]))
            tile = ((anchor[0] - origin_x) // tile_size,
                    (anchor[2] - origin_z) // tile_size)
            bands[name]['groups'] += 1
            bands[name]['blocks'] += len(exposed)
            bands[name]['tiles'][tile] += 1
    return bands


def research_path(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT / 'data/research'):
        raise ValueError('scan must be inside data/research')
    return path


def summarize(plans, tile_size=64):
    totals = {name: {side: Counter() for side in ('vanilla', 'candidate')}
              for name, _, _ in HEIGHT_BANDS}
    tiles = {name: {} for name, _, _ in HEIGHT_BANDS}
    completed = missing = 0
    exposed_positions = Counter()
    for plan_path in plans:
        pack, results, reference = load_plan(plan_path)
        status = inspect_results(pack, results, reference)
        areas = json.loads(reference.read_text())['areas']
        completed += len(status['completed'])
        missing += len(status['missing'])
        for index in status['completed']:
            row = json.loads((results / f'area-{index:02d}.json').read_text())
            area = areas[index]
            if row['reference_world_scan'] != area['scan_file']:
                raise ValueError('result uses the wrong Vanilla scan')
            if row['full_height'].get('vanilla_source') != 'reference_assuming_no_upper_diamonds':
                raise ValueError('unexpected Vanilla upper-height source')
            vanilla = json.loads(research_path(row['reference_world_scan']).read_text())
            candidate = json.loads((research_path(row['candidate_world']) / 'ore_scan.json').read_text())
            if vanilla['chunks'] != candidate['chunks'] or vanilla['biomes'] != candidate['biomes']:
                raise ValueError('Vanilla and candidate region or sampled biomes differ')
            if len(candidate['upperDiamondOre']) != row['candidate_upper_diamonds_17_to_40']:
                raise ValueError('upper ore count differs from saved result')
            origin_x, origin_z = row['chunk_x'] * 16, row['chunk_z'] * 16
            width = row['chunks_per_side'] * 16
            if analyze(vanilla, origin_x, origin_z, width)['deposits']['air_adjacent'] != row['vanilla']['deposits']['air_adjacent']:
                raise ValueError('Vanilla group count differs from saved result')
            if analyze_full_height(candidate, origin_x, origin_z, width)['deposits']['air_adjacent'] != row['full_height']['candidate']['deposits']['air_adjacent']:
                raise ValueError('candidate group count differs from saved result')
            exposed_positions.update(compare_exposed_positions(vanilla, candidate))
            for side, scan in (('vanilla', vanilla), ('candidate', candidate)):
                measured = measure_scan(scan, origin_x, origin_z, tile_size)
                for name, data in measured.items():
                    totals[name][side]['groups'] += data['groups']
                    totals[name][side]['blocks'] += data['blocks']
                    for tile, count in data['tiles'].items():
                        key = (str(plan_path), index, *tile)
                        tiles[name].setdefault(key, Counter())[side] += count
    output = {'completed': completed, 'missing': missing,
              'tile_size': tile_size, 'vanilla_upper_17_to_40_assumed_empty': True,
              'exposed_positions': dict(exposed_positions),
              'note': ('A group can count in multiple height bands when it has air-facing blocks in each. '
                       'One deterministic air-facing block assigns it to one tile per band; tiles are not caves.'),
              'bands': {}}
    for name, _, _ in HEIGHT_BANDS:
        vanilla = totals[name]['vanilla']
        candidate = totals[name]['candidate']
        tile_counts = list(tiles[name].values())
        output['bands'][name] = {
            'groups': {'vanilla': vanilla['groups'], 'candidate': candidate['groups'],
                       'percent_of_vanilla': ratio(candidate['groups'], vanilla['groups'])},
            'air_exposed_blocks': {'vanilla': vanilla['blocks'], 'candidate': candidate['blocks']},
            'local_tiles': {'candidate_gt_vanilla': sum(c['candidate'] > c['vanilla'] for c in tile_counts),
                            'max_vanilla': max((c['vanilla'] for c in tile_counts), default=0),
                            'max_candidate': max((c['candidate'] for c in tile_counts), default=0),
                            'max_candidate_with_vanilla': [
                                {'candidate': count['candidate'], 'vanilla': count['vanilla'],
                                 'area': key[0], 'index': key[1], 'tile_x': key[2], 'tile_z': key[3]}
                                for key, count in sorted(tiles[name].items(),
                                                         key=lambda item: (-item[1]['candidate'], item[0]))[:3]]}}
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, action='append', required=True)
    parser.add_argument('--tile-size', type=int, default=64)
    args = parser.parse_args()
    print(json.dumps(summarize(args.plan, args.tile_size), ensure_ascii=False, separators=(',', ':')))


if __name__ == '__main__':
    main()
