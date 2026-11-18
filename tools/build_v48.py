"""Try sparser, larger buried diamond veins above Y=-20."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v47/behavior_pack'
TARGET = ROOT / 'experiments/balance-v48/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    feature_path = target / 'features/sparse_buried.json'
    feature = json.loads(feature_path.read_text())
    body = feature['minecraft:ore_feature']
    if body['count'] != 5:
        raise ValueError('unexpected V47 upper buried size')
    body['count'] = 8
    feature_path.write_text(json.dumps(feature, ensure_ascii=False, indent=2) + '\n')
    rule_path = target / 'feature_rules/upper_buried_rule.json'
    rule = json.loads(rule_path.read_text())
    rule['minecraft:feature_rules']['distribution']['scatter_chance'] = 65
    rule_path.write_text(json.dumps(rule, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V48 Buried Group Balance'
    manifest['header']['description'] = (
        'Forschungsvariante: seltenere vergrabene Adern oberhalb von Y=-20; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
