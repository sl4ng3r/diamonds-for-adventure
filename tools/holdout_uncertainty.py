#!/usr/bin/env python3
"""Report deterministic seed/area-cluster uncertainty for a holdout scan."""
import argparse
import json
import random
from pathlib import Path


def ratio(numerator, denominator):
    return 100.0 * numerator / denominator if denominator else None


def percentile(values, fraction):
    ordered=sorted(values)
    if not ordered:
        return None
    position=(len(ordered)-1)*fraction
    lower=int(position)
    upper=min(lower+1,len(ordered)-1)
    weight=position-lower
    return ordered[lower]*(1-weight)+ordered[upper]*weight


def load_areas(results):
    areas=[json.loads(path.read_text()) for path in sorted(results.glob('area-*.json'))]
    if not areas:
        raise ValueError('no area results found')
    seeds={area.get('seed') for area in areas}
    if None in seeds:
        raise ValueError('every area must contain a seed')
    return areas


def area_metric(area, name):
    if name == 'air_groups':
        return area['vanilla']['deposits']['air_adjacent'], area['candidate']['deposits']['air_adjacent']
    if name == 'y_minus57':
        return area['vanilla']['y_minus57']['buried'], area['candidate']['y_minus57']['buried']
    if name == 'tunnel_contacts':
        return area['tunnel_contacts']['vanilla'], area['tunnel_contacts']['candidate']
    raise ValueError(name)


def report(results, bootstrap_samples=10000):
    areas=load_areas(results)
    metrics={}
    for name in ('air_groups','y_minus57','tunnel_contacts'):
        vanilla=sum(area_metric(area,name)[0] for area in areas)
        candidate=sum(area_metric(area,name)[1] for area in areas)
        rng=random.Random(0)
        bootstrap=[]
        for _ in range(bootstrap_samples):
            sample=[areas[rng.randrange(len(areas))] for _ in areas]
            b=sum(area_metric(area,name)[0] for area in sample)
            c=sum(area_metric(area,name)[1] for area in sample)
            if b:
                bootstrap.append(ratio(c,b))
        metrics[name]={
            'vanilla':vanilla,
            'candidate':candidate,
            'percent_of_vanilla':ratio(candidate,vanilla),
            'cluster_bootstrap_percentiles':{
                'p2_5':percentile(bootstrap,0.025),
                'p50':percentile(bootstrap,0.5),
                'p97_5':percentile(bootstrap,0.975),
            },
        }
    return {
        'areas':len(areas),
        'seeds':sorted({area['seed'] for area in areas}),
        'unit':'area/seed; resampling preserves each complete area as one unit',
        'bootstrap_samples':bootstrap_samples,
        'random_seed':0,
        'metrics':metrics,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--bootstrap-samples',type=int,default=10000)
    args=parser.parse_args()
    if args.bootstrap_samples < 1:
        parser.error('--bootstrap-samples must be positive')
    output=report(args.results,args.bootstrap_samples)
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,ensure_ascii=False))


if __name__ == '__main__':
    main()
