"""Build V37 with floor/ceiling veins embedded behind their air-facing ore."""

import json
from pathlib import Path
import shutil


ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'experiments/balance-v36/behavior_pack'
TARGET=ROOT/'experiments/balance-v37/behavior_pack'
WEIGHTS=((1,1),(2,1),(3,25),(4,64),(5,10))
SIDES=(('east',1,0),('west',-1,0),('north',0,-1),('south',0,1))


def write_json(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def scatter(identifier,x,y,z):
    return {'format_version':'1.21.40',
            'minecraft:scatter_feature':{
                'description':{'identifier':identifier},
                'places_feature':'cavediamonds:cave_select',
                'distribution':{'iterations':1,'x':x,'y':y,'z':z}}}


def build_pack(target=TARGET):
    target=Path(target)
    shutil.copytree(SOURCE,target)
    manifest_path=target/'manifest.json'
    manifest=json.loads(manifest_path.read_text())
    manifest['header']['name']='Cave Diamonds – V37 Embedded Vein Experiment'
    write_json(manifest_path,manifest)

    for surface,step in (('floor',-1),('ceiling',1)):
        choice_id=f'cavediamonds:cave_{surface}_vein_choice'
        for suffix in ('','_upper'):
            snap_path=target/f'features/cave_snap_{surface}{suffix}.json'
            snap=json.loads(snap_path.read_text())
            snap['minecraft:snap_to_surface_feature']['feature_to_snap']=choice_id
            write_json(snap_path,snap)

        for depth in (1,2,3):
            name=f'cave_{surface}_inward_{depth}'
            write_json(target/f'features/{name}.json',
                       scatter(f'cavediamonds:{name}',0,step*depth,0))
        side_features=[]
        for direction,x,z in SIDES:
            name=f'cave_{surface}_side_{direction}'
            write_json(target/f'features/{name}.json',
                       scatter(f'cavediamonds:{name}',x,step,z))
            side_features.append([f'cavediamonds:{name}',1])
        write_json(target/f'features/cave_{surface}_side_choice.json',{
            'format_version':'1.21.40',
            'minecraft:weighted_random_feature':{
                'description':{'identifier':f'cavediamonds:cave_{surface}_side_choice'},
                'features':side_features,
            },
        })
        for n,_ in WEIGHTS:
            features=['cavediamonds:cave_select']
            if n>=2: features.append(f'cavediamonds:cave_{surface}_inward_1')
            if n>=3: features.append(f'cavediamonds:cave_{surface}_inward_2')
            if n>=4: features.append(f'cavediamonds:cave_{surface}_side_choice')
            if n>=5: features.append(f'cavediamonds:cave_{surface}_inward_3')
            write_json(target/f'features/cave_{surface}_vein_n{n}.json',{
                'format_version':'1.21.40',
                'minecraft:aggregate_feature':{
                    'description':{'identifier':f'cavediamonds:cave_{surface}_vein_n{n}'},
                    'features':features,'early_out':'none',
                },
            })
        write_json(target/f'features/cave_{surface}_vein_choice.json',{
            'format_version':'1.21.40',
            'minecraft:weighted_random_feature':{
                'description':{'identifier':choice_id},
                'features':[[f'cavediamonds:cave_{surface}_vein_n{n}',weight]
                            for n,weight in WEIGHTS],
            },
        })
    return target


def main(): print(build_pack())


if __name__=='__main__': main()
