"""Build V34 by lowering only V33's mid-height cave chance."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v33/behavior_pack'
TARGET = ROOT / 'experiments/balance-v34/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    chance_path = target / 'features/cave_mid_chance.json'
    chance = json.loads(chance_path.read_text())
    chance['minecraft:scatter_feature']['distribution']['scatter_chance'] = 45
    chance_path.write_text(json.dumps(chance, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V34 Exposure Calibration'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
