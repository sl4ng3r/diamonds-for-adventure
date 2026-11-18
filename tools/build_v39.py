"""Build V39 with an intermediate narrow deep cave placement setting."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v37/behavior_pack'
TARGET = ROOT / 'experiments/balance-v39/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    rule_path = target / 'feature_rules/cave_deep_extra2.json'
    rule = json.loads(rule_path.read_text())
    if rule['minecraft:feature_rules']['distribution']['scatter_chance'] != 40:
        raise ValueError('unexpected V37 deep rule')
    rule['minecraft:feature_rules']['distribution']['scatter_chance'] = 30
    rule_path.write_text(json.dumps(rule, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V39 Spatial Balance Experiment'
    manifest['header']['description'] = (
        'Forschungsvariante mit abgeschwächter schmaler Tiefenregel; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
