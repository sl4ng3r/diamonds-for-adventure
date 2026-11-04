#!/usr/bin/env python3
"""Summarize diagnostic scans without making assumptions about accessible caves."""
import json
import sys
from pathlib import Path

def compare_block_counts(before, after):
    changes={}
    a,b=before['blockCounts'],after['blockCounts']
    if set(a) != set(b): raise ValueError('chunk coverage differs')
    for chunk in a:
        delta={block:b[chunk].get(block,0)-a[chunk].get(block,0) for block in set(a[chunk])|set(b[chunk])}
        delta={block:value for block,value in delta.items() if value}
        if delta: changes[chunk]=delta
    return changes


def summarize(scan):
    def empty():
        return {'total': 0, 'exposed': 0, 'buried': 0}

    result = {'edge': empty(), 'interior': empty(), 'ore_biomes': {},
              'sampled_biomes': scan.get('biomes', {})}
    seen = set()
    for ore in scan['ores']:
        pos = ore['x'], ore['y'], ore['z']
        if pos in seen:
            raise ValueError(f'duplicate ore position: {pos}')
        seen.add(pos)
        edge = ore['x'] % 16 in (0, 15) or ore['z'] % 16 in (0, 15)
        groups = (result['edge' if edge else 'interior'],
                  result['ore_biomes'].setdefault(ore.get('biome', 'unknown'), empty()))
        for group in groups:
            group['total'] += 1
            group['exposed' if ore['exposed'] else 'buried'] += 1
    return result


if __name__ == '__main__':
    for name in sys.argv[1:]:
        path = Path(name)
        print(json.dumps({'path': str(path), **summarize(json.loads(path.read_text()))}))
