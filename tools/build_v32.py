"""Build V32 by setting V30's regular cave wrapper chance to 30."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v30/behavior_pack'
TARGET = ROOT / 'experiments/balance-v32/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    wrapper_path = target / 'features/cave_regular_chance.json'
    wrapper = json.loads(wrapper_path.read_text())
    wrapper['minecraft:scatter_feature']['distribution']['scatter_chance'] = 30
    wrapper_path.write_text(json.dumps(wrapper, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V32 Exposure Calibration'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
