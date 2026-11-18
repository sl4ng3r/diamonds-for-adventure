"""Preserve Vanilla buried diamonds above Y=-20."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v44/behavior_pack'
TARGET = ROOT / 'experiments/balance-v45/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    (target / 'features/diamond_ore_buried_feature.json').unlink()

    scan_path = target / 'features/scan_chunk.json'
    scan = json.loads(scan_path.read_text())
    distribution = scan['minecraft:scatter_feature']['distribution']
    if distribution['y']['extent'] != [0, 80] or distribution['iterations'] != 16 * 16 * 81:
        raise ValueError('unexpected V44 thinning range')
    distribution['y']['extent'] = [0, 44]
    distribution['iterations'] = 16 * 16 * 45
    scan_path.write_text(json.dumps(scan, ensure_ascii=False, indent=2) + '\n')

    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V45 Deep Tunnel Experiment'
    manifest['header']['description'] = (
        'Forschungsvariante: Vanilla-Grabfunde oberhalb von Y=-20 erhalten; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
