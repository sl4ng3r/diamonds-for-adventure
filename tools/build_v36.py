"""Build V36 with a surface anchor and a small ore-feature blob per vein."""

import json
from pathlib import Path
import shutil


ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'experiments/balance-v35/behavior_pack'
TARGET=ROOT/'experiments/balance-v36/behavior_pack'
VEIN_WEIGHTS=((1,1),(2,1),(3,25),(4,64),(5,10))


def write_json(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def build_pack(target=TARGET):
    target=Path(target)
    shutil.copytree(SOURCE,target)
    manifest_path=target/'manifest.json'
    manifest=json.loads(manifest_path.read_text())
    manifest['header']['name']='Cave Diamonds – V36 Surface Anchor Experiment'
    write_json(manifest_path,manifest)
    write_json(target/'features/cave_vein_choice.json',{
        'format_version':'1.21.40',
        'minecraft:weighted_random_feature':{
            'description':{'identifier':'cavediamonds:cave_vein_choice'},
            'features':[[f'cavediamonds:cave_surface_vein_n{n}',weight]
                        for n,weight in VEIN_WEIGHTS],
        },
    })
    for n,_ in VEIN_WEIGHTS:
        features=['cavediamonds:cave_select']
        if n>1: features.append(f'cavediamonds:cave_ore_n{n-1}')
        write_json(target/f'features/cave_surface_vein_n{n}.json',{
            'format_version':'1.21.40',
            'minecraft:aggregate_feature':{
                'description':{'identifier':f'cavediamonds:cave_surface_vein_n{n}'},
                'features':features,
                'early_out':'none',
            },
        })
    return target


def main(): print(build_pack())


if __name__=='__main__': main()
