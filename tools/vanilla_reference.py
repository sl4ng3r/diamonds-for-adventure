#!/usr/bin/env python3
"""Read-only ore classification and isolated vanilla reference world creation."""
import argparse
import json
from pathlib import Path

FLUIDS={'minecraft:water','minecraft:flowing_water','minecraft:lava','minecraft:flowing_lava'}
DIRECTIONS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))

def analyze(scan, origin_x, origin_z, width):
    def counts(ores):
        values={'total':len(ores),'air':0,'fluid_only':0,'buried':0,'air_and_fluid':0,'water_adjacent':0,'lava_adjacent':0}
        for ore in ores:
            air='minecraft:air' in ore['neighbours']
            fluid=any(n in FLUIDS for n in ore['neighbours'])
            values['air' if air else 'fluid_only' if fluid else 'buried'] += 1
            if air and fluid: values['air_and_fluid'] += 1
            if any(n in ('minecraft:water','minecraft:flowing_water') for n in ore['neighbours']): values['water_adjacent'] += 1
            if any(n in ('minecraft:lava','minecraft:flowing_lava') for n in ore['neighbours']): values['lava_adjacent'] += 1
        return values
    ores=scan['ores']
    positions={(o['x'],o['y'],o['z']):o for o in ores}
    if len(positions)!=len(ores): raise ValueError('duplicate ore position')
    remaining=set(positions)
    deposits=[]
    while remaining:
        root=remaining.pop()
        stack=[root]; component=[root]
        while stack:
            x,y,z=stack.pop()
            for dx,dy,dz in DIRECTIONS:
                neighbor=(x+dx,y+dy,z+dz)
                if neighbor in remaining:
                    remaining.remove(neighbor); stack.append(neighbor); component.append(neighbor)
        deposits.append(component)
    boundary=lambda p: p[0] in (origin_x,origin_x+width-1) or p[2] in (origin_z,origin_z+width-1) or p[1] in (-64,16)
    return {'blocks':counts(ores),
            'below_zero':counts([o for o in ores if o['y']<0]),
            'y_minus57':counts([o for o in ores if o['y']==-57]),
            'tunnel_band':counts([o for o in ores if -59 <= o['y'] <= -55]),
            'deepslate_ore':counts([o for o in ores if o['type']=='minecraft:deepslate_diamond_ore']),
            'deposits':{'total':len(deposits),
                        'air_adjacent':sum(any('minecraft:air' in positions[p]['neighbours'] for p in group) for group in deposits),
                        'air_adjacent_sizes':sorted((len(group) for group in deposits if any('minecraft:air' in positions[p]['neighbours'] for p in group)),reverse=True),
                        'touching_scan_boundary':sum(any(boundary(p) for p in group) for group in deposits),
                        'air_adjacent_touching_boundary':sum(any(boundary(p) for p in group) and any('minecraft:air' in positions[p]['neighbours'] for p in group) for group in deposits),
                        'sizes':sorted((len(group) for group in deposits),reverse=True)},
            'sampled_biomes':scan.get('biomes',{})}

def aggregate(reports):
    for index,a in enumerate(reports):
        for b in reports[:index]:
            n,m=a['chunks_per_side'],b['chunks_per_side']
            if (a['seed']==b['seed'] and a['chunk_x']<b['chunk_x']+m and b['chunk_x']<a['chunk_x']+n
                and a['chunk_z']<b['chunk_z']+m and b['chunk_z']<a['chunk_z']+n):
                raise ValueError('overlapping sample regions for the same seed')
    categories=('blocks','below_zero','y_minus57','tunnel_band','deepslate_ore')
    totals={name:{key:sum(report[name][key] for report in reports) for key in reports[0][name]} if reports else {} for name in categories}
    totals['deposits']={name:sum(r['deposits'][name] for r in reports) for name in ('total','air_adjacent','touching_scan_boundary','air_adjacent_touching_boundary')}
    return {'regions':len(reports),'seeds':len({r['seed'] for r in reports}),
            'total_chunks':sum(r['chunks_per_side']**2 for r in reports),'totals':totals}

def main():
    from tools.compare_worlds import ROOT, eula_accepted, run
    parser=argparse.ArgumentParser(description='Create one isolated vanilla-only ore reference world')
    parser.add_argument('--seed',type=int,required=True)
    parser.add_argument('--chunk-x',type=int,default=0)
    parser.add_argument('--chunk-z',type=int,default=0)
    parser.add_argument('--chunks',type=int,choices=range(1,33),default=4)
    args=parser.parse_args()
    if not eula_accepted(ROOT/'.env'): parser.error('Explicit EULA=TRUE in .env required')
    print(f'Vanilla seed {args.seed}, chunk {args.chunk_x}/{args.chunk_z} startet',flush=True)
    result=run(args.seed,False,args.chunks,diagnose=True,chunk_x=args.chunk_x,chunk_z=args.chunk_z)
    scan_path=Path(result['world'])/'ore_scan.json'
    summary=analyze(json.loads(scan_path.read_text()),args.chunk_x*16,args.chunk_z*16,args.chunks*16)
    report={'seed':args.seed,'chunk_x':args.chunk_x,'chunk_z':args.chunk_z,'chunks_per_side':args.chunks,'world':result['world'],**summary}
    (Path(result['world'])/'vanilla_reference.json').write_text(json.dumps(report,indent=2)+'\n')
    print('VANILLA_REFERENCE '+json.dumps(report),flush=True)

if __name__=='__main__': main()
