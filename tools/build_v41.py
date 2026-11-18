"""Build a diagnostic pack that keeps Vanilla's normal cave diamond features."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v37/behavior_pack'
TARGET = ROOT / 'experiments/balance-v41/behavior_pack'
REMOVED = (
    'features/diamond_ore_feature.json',
    'features/diamond_ore_large_feature.json',
    'feature_rules/cave_rule.json',
    'feature_rules/cave_deep_extra.json',
    'feature_rules/cave_deep_extra2.json',
    'feature_rules/cave_mid_rule.json',
    'feature_rules/sparse_buried_rule.json',
)


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    for name in REMOVED:
        (target / name).unlink()
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V41 Vanilla Cave Baseline'
    manifest['header']['description'] = (
        'Diagnose: Vanilla-Normaladern und obere Zusatzregel; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
