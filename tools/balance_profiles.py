#!/usr/bin/env python3
"""Measure candidate and baseline height bands and approximate cave group sizes."""
import argparse
from collections import Counter
import json
from pathlib import Path
from tools.balance_experiment import ROOT, REFERENCE, summarize
from tools.vanilla_reference import FLUIDS

BANDS=(('-64..-48',-64,-48),('-47..-32',-47,-32),('-31..-16',-31,-16),('-15..-1',-15,-1),('0..16',0,16))

def height_profile(scan):
    result={name:{'total':0,'buried':0} for name,_,_ in BANDS}
    for ore in scan['ores']:
        for name,low,high in BANDS:
            if low<=ore['y']<=high:
                result[name]['total']+=1
                if 'minecraft:air' not in ore['neighbours'] and not any(n in FLUIDS for n in ore['neighbours']): result[name]['buried']+=1
                break
    return result

def exposure_profile(scan):
    result={'air_exposed':0,'floor':0,'ceiling':0,'wall':0,'only_floor':0,'only_ceiling':0,'only_wall':0,
            'air_by_height':{name:0 for name,_,_ in BANDS}}
    for ore in scan['ores']:
        neighbours=ore['neighbours']
        if 'minecraft:air' not in neighbours: continue
        result['air_exposed']+=1
        floor=neighbours[2]=='minecraft:air'
        ceiling=neighbours[3]=='minecraft:air'
        wall=any(neighbours[i]=='minecraft:air' for i in (0,1,4,5))
        for key,hit in (('floor',floor),('ceiling',ceiling),('wall',wall)):
            if hit: result[key]+=1
        if floor and not ceiling and not wall: result['only_floor']+=1
        if ceiling and not floor and not wall: result['only_ceiling']+=1
        if wall and not floor and not ceiling: result['only_wall']+=1
        for name,low,high in BANDS:
            if low<=ore['y']<=high:
                result['air_by_height'][name]+=1
                break
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--results',type=Path,required=True)
    parser.add_argument('--reference',type=Path,default=REFERENCE)
    args=parser.parse_args()
    # Validate fingerprints and duplicate regions before aggregating.
    verified=summarize(args.results,args.reference)
    result={name:{'vanilla':Counter(),'candidate':Counter()} for name,_,_ in BANDS}
    sizes={'vanilla':Counter(),'candidate':Counter()}
    for path in sorted(args.results.glob('area-*.json')):
        area=json.loads(path.read_text())
        for name,scan_path in [('vanilla',ROOT/area['reference_world_scan']),('candidate',ROOT/area['candidate_world']/'ore_scan.json')]:
            profile=height_profile(json.loads(scan_path.read_text()))
            for band in profile: result[band][name].update(profile[band])
            sizes[name].update(area[name]['deposits']['air_adjacent_sizes'])
    print(json.dumps({'areas':verified['areas'],'bands':result,'air_group_sizes':sizes},indent=2))

if __name__=='__main__': main()
