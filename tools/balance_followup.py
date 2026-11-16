#!/usr/bin/env python3
"""Run candidate-only full-height scans and print a compact, resumable checkpoint."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random

from tools.balance_batch import inspect_results, ratio, run_pending
from tools.balance_experiment import ROOT, pack_digest
from tools.holdout_uncertainty import percentile, report as uncertainty_report


HEIGHT_BANDS=(('-64..-48',-64,-48),('-47..-32',-47,-32),('-31..-16',-31,-16),
              ('-15..-1',-15,-1),('0..16',0,16),('17..40',17,40))


def exposed_by_height(ores):
    counts=Counter()
    for ore in ores:
        if 'minecraft:air' not in ore['neighbours']:
            continue
        for name,low,high in HEIGHT_BANDS:
            if low<=ore['y']<=high:
                counts[name]+=1
                break
        else:
            raise ValueError('air-exposed ore is outside the measured height range')
    return counts


def exposure_interval(areas, bootstrap_samples):
    rng=random.Random(0)
    estimates=[]
    for _ in range(bootstrap_samples):
        sample=[areas[rng.randrange(len(areas))] for _ in areas]
        vanilla=sum(area['air_exposed_blocks']['vanilla'] for area in sample)
        candidate=sum(area['air_exposed_blocks']['candidate'] for area in sample)
        if vanilla:
            estimates.append(100*candidate/vanilla)
    return [round(value,1) if value is not None else None
            for value in (percentile(estimates,0.025),percentile(estimates,0.975))]


def summarize_rows(rows, root=ROOT):
    if not rows:
        raise ValueError('no completed areas')
    root=root.resolve()
    totals={'vanilla':0,'candidate':0}
    exposed={'vanilla':0,'candidate':0}
    exposed_heights={side:Counter() for side in exposed}
    heights=Counter()
    areas=[]
    for row in rows:
        full=row['full_height']
        if full.get('range')!=[-64,40] or full.get('vanilla_source')!='reference_assuming_no_upper_diamonds':
            raise ValueError('expected candidate-only full-height results using the frozen Vanilla reference')
        vanilla=full['vanilla_air_groups']
        candidate=full['candidate']['deposits']['air_adjacent']
        world=Path(row['candidate_world'])
        if world.is_absolute() or not (root/world).resolve().is_relative_to(root/'data/research'):
            raise ValueError('candidate world must be under data/research')
        scan=json.loads((root/world/'ore_scan.json').read_text())
        upper=scan['upperDiamondOre']
        if len(upper)!=row['candidate_upper_diamonds_17_to_40']:
            raise ValueError('upper ore count disagrees with raw scan')
        baseline=Path(row['reference_world_scan'])
        if baseline.is_absolute() or not (root/baseline).resolve().is_relative_to(root/'data/research'):
            raise ValueError('Vanilla scan must be under data/research')
        vanilla_scan=json.loads((root/baseline).read_text())
        area_exposed={}
        for side,ores in (('vanilla',vanilla_scan['ores']),
                          ('candidate',scan['ores']+upper)):
            profile=exposed_by_height(ores)
            exposed_heights[side].update(profile)
            exposed[side]+=sum(profile.values())
            area_exposed[side]=sum(profile.values())
        heights.update(ore['y'] for ore in upper)
        totals['vanilla']+=vanilla
        totals['candidate']+=candidate
        areas.append({'index':row['index'],'vanilla':vanilla,'candidate':candidate,
                      'percent_of_vanilla':ratio(candidate,vanilla),
                      'air_exposed_blocks':{**area_exposed,
                          'percent_of_vanilla':ratio(area_exposed['candidate'],area_exposed['vanilla'])}})
    totals['percent_of_vanilla']=ratio(totals['candidate'],totals['vanilla'])
    exposed['percent_of_vanilla']=ratio(exposed['candidate'],exposed['vanilla'])
    by_height={name:{'vanilla':exposed_heights['vanilla'][name],
                     'candidate':exposed_heights['candidate'][name],
                     'percent_of_vanilla':ratio(exposed_heights['candidate'][name],
                                                exposed_heights['vanilla'][name])}
               for name,_,_ in HEIGHT_BANDS}
    return {'groups':totals,'areas':areas,'upper_blocks':sum(heights.values()),
            'upper_heights':{str(y):heights[y] for y in sorted(heights)},
            'highest_upper_y':max(heights,default=None),
            'air_exposed_blocks':exposed,'air_exposed_by_height':by_height}


def load_plan(path, root=ROOT):
    root=root.resolve()
    plan=json.loads(path.read_text())
    def local_path(value):
        item=Path(value)
        if item.is_absolute() or '..' in item.parts:
            raise ValueError('plan paths must be relative to the project')
        result=(root/item).resolve()
        if not result.is_relative_to(root):
            raise ValueError('plan path leaves project')
        return result
    pack=local_path(plan['pack'])
    reference=local_path(plan['reference'])
    results=local_path(plan['results'])
    if pack_digest(pack)!=plan['pack_sha256']:
        raise ValueError('plan pack hash mismatch')
    if hashlib.sha256(reference.read_bytes()).hexdigest()!=plan['reference_sha256']:
        raise ValueError('plan reference hash mismatch')
    data=json.loads(reference.read_text())
    if data['server_version']!=plan['server_version'] or plan['indexes']!=list(range(len(data['areas']))):
        raise ValueError('plan server version or area indexes mismatch')
    fields=('seed','chunk_x','chunk_z','chunks_per_side')
    expected=[{key:area[key] for key in fields} for area in data['areas']]
    if plan['areas']!=expected:
        raise ValueError('plan area metadata mismatch')
    return pack,results,reference


def checkpoint(pack, results, reference, bootstrap_samples=10000):
    status=inspect_results(pack,results,reference)
    output={'completed':len(status['completed']),'total':status['total'],
            'missing':status['missing'],'pack_sha256':status['pack_sha256'],
            'reference_sha256':status['reference_sha256']}
    if status['completed']:
        rows=[json.loads((results/f'area-{index:02d}.json').read_text()) for index in status['completed']]
        output.update(summarize_rows(rows))
        if not status['missing']:
            metric=uncertainty_report(results,bootstrap_samples)['metrics']['full_height_air_groups']
            output['area_bootstrap_95_percent']=tuple(round(metric['cluster_bootstrap_percentiles'][key],1)
                                                     for key in ('p2_5','p97_5'))
            output['air_exposed_area_bootstrap_95_percent']=exposure_interval(output['areas'],bootstrap_samples)
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('run','status'))
    parser.add_argument('--plan',type=Path,help='frozen pack, reference, and region selection')
    parser.add_argument('--pack',type=Path)
    parser.add_argument('--results',type=Path)
    parser.add_argument('--reference',type=Path)
    parser.add_argument('--limit',type=int,help='maximum number of missing candidate areas to scan')
    parser.add_argument('--bootstrap-samples',type=int,default=10000)
    args=parser.parse_args()
    if args.bootstrap_samples<1:
        parser.error('--bootstrap-samples must be positive')
    if args.command=='status' and args.limit is not None:
        parser.error('--limit applies only to run')
    if args.plan:
        if any((args.pack,args.results,args.reference)):
            parser.error('--plan cannot be combined with --pack, --results, or --reference')
        pack,results,reference=load_plan(args.plan)
    else:
        if not all((args.pack,args.results,args.reference)):
            parser.error('provide --plan or all of --pack, --results, and --reference')
        pack,results,reference=args.pack.resolve(),args.results,args.reference
    if args.command=='run':
        run_pending(pack,results,reference,args.limit,
                    full_height=True,reference_upper_empty=True)
    print(json.dumps(checkpoint(pack,results,reference,args.bootstrap_samples),
                     ensure_ascii=False,separators=(',',':')))


if __name__=='__main__':
    main()
