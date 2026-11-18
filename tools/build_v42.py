"""Test late buried-ore thinning while keeping Vanilla's normal cave diamonds."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v41/behavior_pack'
PROTOTYPE = ROOT / 'prototype/behavior_pack'
TARGET = ROOT / 'experiments/balance-v42/behavior_pack'
THIN_FILES = (
    'feature_rules/thin_overworld.json',
    'features/scan_chunk.json',
    'features/select_ore.json',
    'features/thin_diamond.json',
    'features/thin_deepslate.json',
)


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    for name in THIN_FILES:
        shutil.copy2(PROTOTYPE / name, target / name)
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V42 Late Thinning Experiment'
    manifest['header']['description'] = (
        'Diagnose: Vanilla-Höhlenadern mit später Ausdünnung; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
